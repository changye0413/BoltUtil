using System;
using System.Net;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

public static class BoltUtilDemo
{
    private static readonly string ApiBase = Env("BOLT_API_BASE", "https://api.boltutil.com");
    private static readonly string ApiKey = Env("BOLT_API_KEY", "YOUR_API_KEY");
    private static readonly string WebhookSecret = Env("BOLT_WEBHOOK_SECRET", "YOUR_WEBHOOK_SECRET");
    private static readonly string NotifyUrl = Env("BOLT_NOTIFY_URL", "https://merchant.example.com/webhooks/boltutil");
    private static readonly string ReturnUrl = Env("BOLT_RETURN_URL", "https://merchant.example.com/orders/return");

    private static string Env(string key, string fallback)
    {
        var value = Environment.GetEnvironmentVariable(key);
        return string.IsNullOrWhiteSpace(value) ? fallback : value;
    }

    private static string HmacSha256Hex(string payload, string secret)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
        var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(payload));
        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    private static string SignBody(string rawBody, string timestamp)
    {
        return HmacSha256Hex($"{timestamp}.{rawBody}", WebhookSecret);
    }

    private static async Task CreateOrder(string network)
    {
        var externalOrderId = $"INV-{DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()}";
        var rawBody = "{"
            + "\"amount\":25.0,"
            + $"\"externalOrderId\":\"{externalOrderId}\","
            + $"\"network\":\"{network}\","
            + "\"currency\":\"USDT\","
            + "\"orderDesc\":\"BoltUtil demo order\","
            + $"\"notifyUrl\":\"{NotifyUrl}\","
            + $"\"returnUrl\":\"{ReturnUrl}?order={externalOrderId}\","
            + "\"expiredMinutes\":30,"
            + "\"metadata\":{\"customerId\":\"CUS_1001\",\"source\":\"csharp-demo\"}"
            + "}";

        var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds().ToString();
        var signature = SignBody(rawBody, timestamp);

        using var client = new HttpClient();
        using var request = new HttpRequestMessage(HttpMethod.Post, $"{ApiBase}/api/v1/order/create");
        request.Content = new StringContent(rawBody, Encoding.UTF8, "application/json");
        request.Headers.Add("X-Bolt-Key", ApiKey);
        request.Headers.Add("X-Bolt-Timestamp", timestamp);
        request.Headers.Add("X-Bolt-Signature", signature);

        using var response = await client.SendAsync(request);
        Console.WriteLine($"HTTP {(int)response.StatusCode}");
        Console.WriteLine(await response.Content.ReadAsStringAsync());
    }

    private static bool VerifyWebhook(string rawBody, string timestamp, string signature)
    {
        if (string.IsNullOrWhiteSpace(timestamp) || string.IsNullOrWhiteSpace(signature))
        {
            return false;
        }

        if (!long.TryParse(timestamp, out var ts))
        {
            return false;
        }

        var now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
        if (Math.Abs(now - ts) > 5 * 60 * 1000)
        {
            return false;
        }

        var expected = SignBody(rawBody, timestamp).ToLowerInvariant();
        var received = signature.ToLowerInvariant();
        return CryptographicOperations.FixedTimeEquals(
            Encoding.UTF8.GetBytes(expected),
            Encoding.UTF8.GetBytes(received)
        );
    }

    private static async Task StartWebhookServer(int port)
    {
        using var listener = new HttpListener();
        listener.Prefixes.Add($"http://0.0.0.0:{port}/webhooks/boltutil/");
        listener.Start();
        Console.WriteLine($"BoltUtil webhook demo listening on http://localhost:{port}/webhooks/boltutil");

        while (true)
        {
            var context = await listener.GetContextAsync();
            _ = Task.Run(async () => await HandleWebhook(context));
        }
    }

    private static async Task HandleWebhook(HttpListenerContext context)
    {
        if (context.Request.HttpMethod != "POST")
        {
            await SendJson(context, 404, "{\"error\":\"not_found\"}");
            return;
        }

        using var reader = new System.IO.StreamReader(context.Request.InputStream, Encoding.UTF8);
        var rawBody = await reader.ReadToEndAsync();
        var timestamp = context.Request.Headers["X-Bolt-Webhook-Timestamp"] ?? "";
        var signature = context.Request.Headers["X-Bolt-Webhook-Signature"] ?? "";

        if (!VerifyWebhook(rawBody, timestamp, signature))
        {
            await SendJson(context, 401, "{\"error\":\"invalid_signature\"}");
            return;
        }

        Console.WriteLine("Verified BoltUtil webhook:");
        Console.WriteLine(rawBody);
        // TODO: update your local order by externalOrderId from the JSON body.
        // Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

        await SendJson(context, 200, "{\"status\":\"SUCCESS\"}");
    }

    private static async Task SendJson(HttpListenerContext context, int statusCode, string body)
    {
        var bytes = Encoding.UTF8.GetBytes(body);
        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/json";
        context.Response.ContentLength64 = bytes.Length;
        await context.Response.OutputStream.WriteAsync(bytes, 0, bytes.Length);
        context.Response.Close();
    }

    public static async Task Main(string[] args)
    {
        var command = args.Length > 0 ? args[0] : "";
        if (command == "create")
        {
            await CreateOrder(args.Length > 1 ? args[1] : "TRC20");
        }
        else if (command == "webhook")
        {
            await StartWebhookServer(int.Parse(Env("PORT", "3000")));
        }
        else
        {
            Console.WriteLine("Usage:");
            Console.WriteLine("  dotnet run -- create TRC20");
            Console.WriteLine("  dotnet run -- create ERC20");
            Console.WriteLine("  dotnet run -- create BEP20");
            Console.WriteLine("  dotnet run -- create POLYGON");
            Console.WriteLine("  dotnet run -- create SOLANA");
            Console.WriteLine("  dotnet run -- webhook");
        }
    }
}
