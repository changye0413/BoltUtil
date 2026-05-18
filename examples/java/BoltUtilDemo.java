import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.Locale;

public class BoltUtilDemo {
    private static final String API_BASE = env("BOLT_API_BASE", "https://api.boltutil.com");
    private static final String API_KEY = env("BOLT_API_KEY", "YOUR_API_KEY");
    private static final String WEBHOOK_SECRET = env("BOLT_WEBHOOK_SECRET", "YOUR_WEBHOOK_SECRET");
    private static final String NOTIFY_URL = env("BOLT_NOTIFY_URL", "https://merchant.example.com/webhooks/boltutil");
    private static final String RETURN_URL = env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return");

    private static String env(String key, String fallback) {
        String value = System.getenv(key);
        return value == null || value.isBlank() ? fallback : value;
    }

    private static String hmacSha256Hex(String payload, String secret) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        byte[] bytes = mac.doFinal(payload.getBytes(StandardCharsets.UTF_8));

        StringBuilder hex = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            hex.append(String.format("%02x", b));
        }
        return hex.toString();
    }

    private static String signBody(String rawBody, String timestamp) throws Exception {
        return hmacSha256Hex(timestamp + "." + rawBody, WEBHOOK_SECRET);
    }

    private static void createOrder(String network) throws Exception {
        String externalOrderId = "INV-" + Instant.now().toEpochMilli();
        String rawBody = "{"
                + "\"amount\":25.0,"
                + "\"externalOrderId\":\"" + externalOrderId + "\","
                + "\"network\":\"" + network + "\","
                + "\"currency\":\"USDT\","
                + "\"orderDesc\":\"BoltUtil demo order\","
                + "\"notifyUrl\":\"" + NOTIFY_URL + "\","
                + "\"returnUrl\":\"" + RETURN_URL + "?order=" + externalOrderId + "\","
                + "\"expiredMinutes\":30,"
                + "\"metadata\":{\"customerId\":\"CUS_1001\",\"source\":\"java-demo\"}"
                + "}";

        String timestamp = String.valueOf(Instant.now().toEpochMilli());
        String signature = signBody(rawBody, timestamp);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_BASE + "/api/v1/order/create"))
                .header("Content-Type", "application/json")
                .header("X-Bolt-Key", API_KEY)
                .header("X-Bolt-Timestamp", timestamp)
                .header("X-Bolt-Signature", signature)
                .POST(HttpRequest.BodyPublishers.ofString(rawBody, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> response = HttpClient.newHttpClient()
                .send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("HTTP " + response.statusCode());
        System.out.println(response.body());
    }

    private static boolean verifyWebhook(String rawBody, String timestamp, String signature) throws Exception {
        if (timestamp == null || timestamp.isBlank() || signature == null || signature.isBlank()) {
            return false;
        }

        long ts = Long.parseLong(timestamp);
        if (Math.abs(Instant.now().toEpochMilli() - ts) > 5 * 60 * 1000) {
            return false;
        }

        String expected = signBody(rawBody, timestamp).toLowerCase(Locale.ROOT);
        String received = signature.toLowerCase(Locale.ROOT);
        return MessageDigest.isEqual(
                expected.getBytes(StandardCharsets.UTF_8),
                received.getBytes(StandardCharsets.UTF_8)
        );
    }

    private static void startWebhookServer(int port) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/webhooks/boltutil", BoltUtilDemo::handleWebhook);
        server.start();
        System.out.println("BoltUtil webhook demo listening on http://localhost:" + port + "/webhooks/boltutil");
    }

    private static void handleWebhook(HttpExchange exchange) throws IOException {
        if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
            sendJson(exchange, 404, "{\"error\":\"not_found\"}");
            return;
        }

        String rawBody = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        String timestamp = exchange.getRequestHeaders().getFirst("X-Bolt-Webhook-Timestamp");
        String signature = exchange.getRequestHeaders().getFirst("X-Bolt-Webhook-Signature");

        try {
            if (!verifyWebhook(rawBody, timestamp, signature)) {
                sendJson(exchange, 401, "{\"error\":\"invalid_signature\"}");
                return;
            }
        } catch (Exception e) {
            sendJson(exchange, 401, "{\"error\":\"invalid_signature\"}");
            return;
        }

        System.out.println("Verified BoltUtil webhook: " + rawBody);
        // TODO: update your local order by externalOrderId from the JSON body.
        // Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

        sendJson(exchange, 200, "{\"status\":\"SUCCESS\"}");
    }

    private static void sendJson(HttpExchange exchange, int statusCode, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream output = exchange.getResponseBody()) {
            output.write(bytes);
        }
    }

    public static void main(String[] args) throws Exception {
        String command = args.length > 0 ? args[0] : "";
        if ("create".equals(command)) {
            createOrder(args.length > 1 ? args[1] : "TRC20");
        } else if ("webhook".equals(command)) {
            startWebhookServer(Integer.parseInt(env("PORT", "3000")));
        } else {
            System.out.println("Usage:");
            System.out.println("  javac BoltUtilDemo.java && java BoltUtilDemo create TRC20");
            System.out.println("  javac BoltUtilDemo.java && java BoltUtilDemo create ERC20");
            System.out.println("  javac BoltUtilDemo.java && java BoltUtilDemo create BEP20");
            System.out.println("  javac BoltUtilDemo.java && java BoltUtilDemo webhook");
        }
    }
}

