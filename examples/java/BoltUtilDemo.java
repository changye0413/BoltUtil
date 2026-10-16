import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.Strictness;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.OutputStream;
import java.io.IOException;
import java.math.BigDecimal;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/**
 * BoltUtil 商户接入示例 / Merchant demo (Java 11+, Maven).
 * 只调用 POST /api/v1/order/create，不调用 WordPress /payments。
 * 建单 → 保存付款信息 → checkoutUrl → 验签回调 → 数据库事务入账。
 * Gson 负责 JSON 转义和解析，BigDecimal 保存金额；不手写 JSON 拼接。
 * 不连接数据库、不自动发货；生产改造点见 handleVerifiedEvent。密钥只从服务端环境读取。
 */
public class BoltUtilDemo {
    private static final int MAX_BODY = 65536; // Demo 接收上限，不是平台全局限额。
    private static final Gson JSON = new GsonBuilder().setStrictness(Strictness.STRICT).create();
    private static final String SECRET = env("BOLT_WEBHOOK_SECRET", "");
    private static String env(String key, String fallback) {
        String value = System.getenv(key); return value == null || value.isEmpty() ? fallback : value;
    }
    private static void requireSecret() {
        if (SECRET.isEmpty() || SECRET.matches("^(YOUR_|whsec_xxx).*")) throw new IllegalArgumentException("Set BOLT_WEBHOOK_SECRET");
    }
    // 毫秒 timestamp + 点 + 原始 UTF-8 body；签名后发送同一份字节，不能再次序列化。
    public static String signBody(byte[] body, String timestamp) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(SECRET.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        mac.update((timestamp + ".").getBytes(StandardCharsets.UTF_8));
        StringBuilder hex = new StringBuilder();
        for (byte b : mac.doFinal(body)) hex.append(String.format("%02x", b));
        return hex.toString();
    }
    public static boolean verifyWebhook(byte[] body, String timestamp, String signature) throws Exception {
        if (timestamp == null || !timestamp.matches("[0-9]{13}") || signature == null || !signature.matches("[a-fA-F0-9]{64}")) return false;
        long ts = Long.parseLong(timestamp), now = System.currentTimeMillis();
        if (ts < now - 300000 || ts > now + 300000) return false;
        return MessageDigest.isEqual(signBody(body, timestamp).getBytes(StandardCharsets.US_ASCII),
                signature.toLowerCase(java.util.Locale.ROOT).getBytes(StandardCharsets.US_ASCII));
    }
    private static void createOrder(String network, String currency, String amount) throws Exception {
        requireSecret(); String key = env("BOLT_API_KEY", "");
        if (key.isEmpty() || key.matches("^(YOUR_|bt_live_xxx).*")) throw new IllegalArgumentException("Set BOLT_API_KEY");
        network = network.toUpperCase(java.util.Locale.ROOT); currency = currency.toUpperCase(java.util.Locale.ROOT);
        if (!Set.of("TRC20", "ERC20", "BEP20", "POLYGON", "SOLANA", "BASE").contains(network)
                || !Set.of("USDT", "USDC").contains(currency) || (network.equals("TRC20") && currency.equals("USDC"))) {
            throw new IllegalArgumentException("Unsupported network/currency pair");
        }
        // 最少 1，最多 18 位整数和 6 位小数。禁止 double 中转，避免财务金额精度丢失。
        if (!amount.matches("[1-9][0-9]{0,17}(\\.[0-9]{1,6})?")) throw new IllegalArgumentException("Amount must be >= 1, max 6 decimals");
        String id = env("BOLT_EXTERNAL_ORDER_ID", "INV-" + UUID.randomUUID());
        if (!id.matches("[A-Za-z0-9_-]{6,64}")) throw new IllegalArgumentException("Invalid externalOrderId");
        String notify = env("BOLT_NOTIFY_URL", "");
        if (!notify.startsWith("https://")) throw new IllegalArgumentException("Set a public HTTPS BOLT_NOTIFY_URL");
        String[] parts = env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return").split("#", 2);
        String returnUrl = parts[0] + (parts[0].contains("?") ? "&" : "?") + "order=" + URLEncoder.encode(id, StandardCharsets.UTF_8)
                + (parts.length > 1 ? "#" + parts[1] : "");
        byte[] body = JSON.toJson(Map.of("amount", new BigDecimal(amount), "externalOrderId", id, "network", network,
                "currency", currency, "notifyUrl", notify, "returnUrl", returnUrl, "expiredMinutes", 30,
                "orderDesc", "BoltUtil demo order", "metadata", Map.of("source", "java-demo"))).getBytes(StandardCharsets.UTF_8);
        String timestamp = Long.toString(System.currentTimeMillis());
        HttpRequest request = HttpRequest.newBuilder(URI.create(env("BOLT_API_BASE", "https://api.boltutil.com").replaceAll("/$", "") + "/api/v1/order/create"))
                .timeout(Duration.ofSeconds(20)).header("Content-Type", "application/json")
                .header("X-Bolt-Key", key).header("X-Bolt-Timestamp", timestamp).header("X-Bolt-Signature", signBody(body, timestamp))
                .POST(HttpRequest.BodyPublishers.ofByteArray(body)).build();
        // 禁止重定向认证头。超时后使用同一 externalOrderId 查询，不盲目新建订单。
        System.out.println("externalOrderId: " + id);
        HttpResponse<String> response = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10))
                .followRedirects(HttpClient.Redirect.NEVER).build().send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
        JsonObject result = JSON.fromJson(response.body(), JsonObject.class);
        if (response.statusCode() < 200 || response.statusCode() >= 300 || result == null || !result.has("code") || result.get("code").getAsInt() != 200) {
            throw new IOException("Create failed: HTTP " + response.statusCode() + ": " + response.body());
        }
        // 保存 data.payment.amount/network/currency/address；展示返回金额，可能含匹配偏移。
        System.out.println(response.body());
    }
    private static int handleVerifiedEvent(JsonObject event) {
        if (event == null || !event.has("externalOrderId") || !event.get("externalOrderId").isJsonPrimitive()
                || !event.getAsJsonPrimitive("externalOrderId").isString() || !event.has("status")
                || !event.get("status").isJsonPrimitive() || !event.getAsJsonPrimitive("status").isString()) return 400;
        // TODO：按当前商户 + externalOrderId 查本地订单，核对币种、网络、地址与返回的精确金额。
        // amount/paidAmount 用 BigDecimal 比较；少付人工接受需要单独业务授权。
        // 仅 CONFIRMED/COMPLETED 可处理付款（链上确认/回调送达），不是两笔付款。
        // eventId 在重试时稳定（旧事件可能没有），唯一约束 + 事务/持久队列实现每单只履约一次。
        // returnUrl、metadata 不是付款凭证；持久化后 ACK，失败返回 5xx，邮件异步处理。
        // 此处无数据库，默认 503；BOLT_DEMO_ACK=1 仅联调，避免直接复制导致丢失通知。
        System.out.println("Verified webhook received (no fulfillment performed)");
        return env("BOLT_DEMO_ACK", "").equals("1") ? 204 : 503;
    }
    private static void handleWebhook(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equals("POST") || !exchange.getRequestURI().toString().equals("/webhooks/boltutil")) { reply(exchange, 404); return; }
        // 只读上限 + 1，避免无上限 readAllBytes。生产仍需代理层限制连接数和读超时。
        byte[] body = exchange.getRequestBody().readNBytes(MAX_BODY + 1);
        if (body.length > MAX_BODY) { reply(exchange, 413); return; }
        try {
            if (!verifyWebhook(body, exchange.getRequestHeaders().getFirst("X-Bolt-Webhook-Timestamp"),
                    exchange.getRequestHeaders().getFirst("X-Bolt-Webhook-Signature"))) { reply(exchange, 401); return; }
            // 验签后才解析；严格 JSON 模式拒绝损坏或多份 JSON，不输出完整个人信息。
            reply(exchange, handleVerifiedEvent(JSON.fromJson(new String(body, StandardCharsets.UTF_8), JsonObject.class)));
        } catch (com.google.gson.JsonParseException | IllegalStateException e) { reply(exchange, 400); }
        catch (Exception e) { reply(exchange, 503); }
    }
    private static void reply(HttpExchange exchange, int status) throws IOException {
        exchange.sendResponseHeaders(status, -1); exchange.close();
    }
    public static void main(String[] args) throws Exception {
        String command = args.length > 0 ? args[0] : "";
        if (command.equals("create")) createOrder(args.length > 1 ? args[1] : "TRC20", args.length > 2 ? args[2] : "USDT", args.length > 3 ? args[3] : "1.00");
        else if (command.equals("webhook")) {
            requireSecret();
            HttpServer server = HttpServer.create(new InetSocketAddress(env("BOLT_LISTEN_HOST", "127.0.0.1"), Integer.parseInt(env("PORT", "3000"))), 16);
            server.createContext("/webhooks/boltutil", BoltUtilDemo::handleWebhook); server.start();
            System.out.println("Webhook listener ready; use HTTPS reverse proxy");
        } else System.out.println("java -cp 'target/classes:target/dependency/*' BoltUtilDemo create POLYGON USDC 1.09 | webhook");
    }
}
