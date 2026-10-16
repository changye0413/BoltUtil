using System.Globalization;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;

/// <summary>
/// BoltUtil 商户接入示例 / Merchant demo (.NET 8).
/// 只使用 POST /api/v1/order/create，不调用 WordPress /payments。
/// 建单 → 保存付款信息 → checkoutUrl → 验签回调 → 数据库事务入账。
/// 无数据库/发货实现；见 HandleVerifiedEvent 的生产改造步骤。密钥只存服务端环境变量。
/// </summary>
public static class BoltUtilDemo
{
    private const int MaxBody = 65536; // Demo 上限，不是平台全局限额。
    private static readonly string Secret = Env("BOLT_WEBHOOK_SECRET", "");
    private static string Env(string key, string fallback) => Environment.GetEnvironmentVariable(key) is { Length: > 0 } v ? v : fallback;
    private static void RequireSecret()
    {
        if (Secret.Length == 0 || Regex.IsMatch(Secret, "^(YOUR_|whsec_xxx)")) throw new Exception("Set BOLT_WEBHOOK_SECRET");
    }
    // 毫秒 timestamp + 点 + 原始 UTF-8 body。签名与发送复用同一份字节，不二次序列化。
    public static string SignBody(byte[] body, string timestamp)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(Secret));
        var prefix = Encoding.UTF8.GetBytes(timestamp + ".");
        return Convert.ToHexString(hmac.ComputeHash(prefix.Concat(body).ToArray())).ToLowerInvariant();
    }
    public static bool VerifyWebhook(byte[] body, string timestamp, string signature)
    {
        if (!Regex.IsMatch(timestamp, "\\A[0-9]{13}\\z") || !Regex.IsMatch(signature, "\\A[a-fA-F0-9]{64}\\z")) return false;
        var ts = long.Parse(timestamp, CultureInfo.InvariantCulture);
        var now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
        if (ts < now - 300000 || ts > now + 300000) return false;
        return CryptographicOperations.FixedTimeEquals(Convert.FromHexString(SignBody(body, timestamp)), Convert.FromHexString(signature));
    }
    private static async Task CreateOrder(string network, string currency, string amount)
    {
        RequireSecret();
        var key = Env("BOLT_API_KEY", "");
        if (key.Length == 0 || Regex.IsMatch(key, "^(YOUR_|bt_live_xxx)")) throw new Exception("Set BOLT_API_KEY");
        network = network.ToUpperInvariant(); currency = currency.ToUpperInvariant();
        if (!new[] { "TRC20", "ERC20", "BEP20", "POLYGON", "SOLANA", "BASE" }.Contains(network)
            || !new[] { "USDT", "USDC" }.Contains(currency) || (network == "TRC20" && currency == "USDC")) throw new Exception("Unsupported network/currency pair");
        // decimal 而非 double；最少 1，最多 18 位整数、6 位小数，序列化为精确 JSON number。
        if (!Regex.IsMatch(amount, "\\A[1-9][0-9]{0,17}(\\.[0-9]{1,6})?\\z")) throw new Exception("Amount must be >= 1, max 6 decimals");
        var id = Env("BOLT_EXTERNAL_ORDER_ID", "INV-" + Guid.NewGuid());
        if (!Regex.IsMatch(id, "\\A[A-Za-z0-9_-]{6,64}\\z")) throw new Exception("Invalid externalOrderId");
        var notify = Env("BOLT_NOTIFY_URL", "");
        if (!notify.StartsWith("https://", StringComparison.Ordinal)) throw new Exception("Set a public HTTPS BOLT_NOTIFY_URL");
        var parts = Env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return").Split('#', 2);
        var returnUrl = parts[0] + (parts[0].Contains('?') ? "&" : "?") + "order=" + Uri.EscapeDataString(id) + (parts.Length > 1 ? "#" + parts[1] : "");
        var body = JsonSerializer.SerializeToUtf8Bytes(new { amount = decimal.Parse(amount, CultureInfo.InvariantCulture), externalOrderId = id,
            network, currency, notifyUrl = notify, returnUrl, expiredMinutes = 30, orderDesc = "BoltUtil demo order", metadata = new { source = "csharp-demo" } });
        var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds().ToString(CultureInfo.InvariantCulture);
        using var handler = new HttpClientHandler { AllowAutoRedirect = false, UseCookies = false }; // 不转发认证头到跳转目标。
        using var client = new HttpClient(handler) { Timeout = TimeSpan.FromSeconds(20) };
        using var request = new HttpRequestMessage(HttpMethod.Post, Env("BOLT_API_BASE", "https://api.boltutil.com").TrimEnd('/') + "/api/v1/order/create");
        request.Content = new ByteArrayContent(body); request.Content.Headers.ContentType = new("application/json");
        request.Headers.Add("X-Bolt-Key", key); request.Headers.Add("X-Bolt-Timestamp", timestamp); request.Headers.Add("X-Bolt-Signature", SignBody(body, timestamp));
        Console.WriteLine("externalOrderId: " + id); // 超时后查询此订单号，不盲目新建。
        using var response = await client.SendAsync(request);
        var text = await response.Content.ReadAsStringAsync();
        using var result = JsonDocument.Parse(text);
        if (!response.IsSuccessStatusCode || !result.RootElement.TryGetProperty("code", out var code) || code.GetInt32() != 200) throw new Exception("Create failed: " + text);
        // 保存 data.payment.amount/network/currency/address；必须展示返回金额（可能带匹配偏移）。
        Console.WriteLine(text);
    }
    private static int HandleVerifiedEvent(JsonElement item)
    {
        if (item.ValueKind != JsonValueKind.Object || !item.TryGetProperty("externalOrderId", out var id) || id.ValueKind != JsonValueKind.String
            || !item.TryGetProperty("status", out var status) || status.ValueKind != JsonValueKind.String) return 400;
        // TODO：当前商户 + externalOrderId 查库；核对网络、币种、地址、返回付款金额，金额用 decimal。
        // 少付人工接受需要单独业务授权。仅 CONFIRMED/COMPLETED 可处理付款（确认/回调送达），不是两笔付款。
        // eventId 重试稳定（旧事件可能没有），数据库唯一约束 + 事务/持久队列保证每单只履约一次。
        // returnUrl、metadata 不是付款凭证。持久化后返回 2xx，失败 5xx，邮件用异步任务。
        // 本例无数据库，默认 503；显式 BOLT_DEMO_ACK=1 仅供联调，不可直接用于生产履约。
        Console.WriteLine("Verified webhook received (no fulfillment performed)");
        return Env("BOLT_DEMO_ACK", "") == "1" ? 204 : 503;
    }
    private static async Task HandleWebhook(HttpListenerContext ctx)
    {
        int status;
        try
        {
            if (ctx.Request.HttpMethod != "POST" || ctx.Request.RawUrl != "/webhooks/boltutil") { Reply(ctx, 404); return; }
            using var body = new MemoryStream(); var buffer = new byte[4096];
            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(15));
            int count;
            while ((count = await ctx.Request.InputStream.ReadAsync(buffer.AsMemory(), timeout.Token)) > 0)
            {
                if (body.Length + count > MaxBody) { Reply(ctx, 413); return; }
                body.Write(buffer, 0, count);
            }
            var bytes = body.ToArray();
            if (!VerifyWebhook(bytes, ctx.Request.Headers["X-Bolt-Webhook-Timestamp"] ?? "", ctx.Request.Headers["X-Bolt-Webhook-Signature"] ?? "")) { Reply(ctx, 401); return; }
            using var item = JsonDocument.Parse(bytes); // 验签后才解析，不输出完整个人信息。
            status = HandleVerifiedEvent(item.RootElement);
        }
        catch (JsonException) { status = 400; }
        catch (Exception) { status = 503; }
        Reply(ctx, status);
    }
    private static void Reply(HttpListenerContext ctx, int status)
    {
        ctx.Response.StatusCode = status; ctx.Response.ContentLength64 = 0; ctx.Response.Close();
    }
    public static async Task Main(string[] args)
    {
        try
        {
            if (args.FirstOrDefault() == "create") await CreateOrder(args.ElementAtOrDefault(1) ?? "TRC20", args.ElementAtOrDefault(2) ?? "USDT", args.ElementAtOrDefault(3) ?? "1.00");
            else if (args.FirstOrDefault() == "webhook")
            {
                RequireSecret(); using var listener = new HttpListener();
                // 监听根路径，再精确匹配回调路径，修复原先前缀多余斜杠导致路由不匹配。
                listener.Prefixes.Add($"http://{Env("BOLT_LISTEN_HOST", "127.0.0.1")}:{Env("PORT", "3000")}/"); listener.Start();
                Console.WriteLine("Webhook listener ready; use HTTPS reverse proxy");
                while (true) { var ctx = await listener.GetContextAsync(); _ = HandleWebhook(ctx); }
            }
            else Console.WriteLine("dotnet run -- create POLYGON USDC 1.09 | webhook");
        }
        catch (Exception e) { Console.Error.WriteLine(e.Message); Environment.ExitCode = 1; }
    }
}
