<?php

$apiBase = getenv('BOLT_API_BASE') ?: 'https://api.boltutil.com';
$apiKey = getenv('BOLT_API_KEY') ?: 'YOUR_API_KEY';
$webhookSecret = getenv('BOLT_WEBHOOK_SECRET') ?: 'YOUR_WEBHOOK_SECRET';
$notifyUrl = getenv('BOLT_NOTIFY_URL') ?: 'https://merchant.example.com/webhooks/boltutil';
$returnUrl = getenv('BOLT_RETURN_URL') ?: 'https://merchant.example.com/orders/return';

function hmac_sha256_hex(string $payload, string $secret): string
{
    return hash_hmac('sha256', $payload, $secret);
}

function sign_body(string $rawBody, string $timestamp, string $secret): string
{
    return hmac_sha256_hex($timestamp . '.' . $rawBody, $secret);
}

function create_order(string $network): void
{
    global $apiBase, $apiKey, $webhookSecret, $notifyUrl, $returnUrl;

    $externalOrderId = 'INV-' . (int) floor(microtime(true) * 1000);
    $payload = [
        'amount' => 25.0,
        'externalOrderId' => $externalOrderId,
        'network' => $network,
        'currency' => 'USDT',
        'orderDesc' => 'BoltUtil demo order',
        'notifyUrl' => $notifyUrl,
        'returnUrl' => $returnUrl . '?order=' . rawurlencode($externalOrderId),
        'expiredMinutes' => 30,
        'metadata' => [
            'customerId' => 'CUS_1001',
            'source' => 'php-demo',
        ],
    ];

    $rawBody = json_encode($payload, JSON_UNESCAPED_SLASHES);
    $timestamp = (string) (int) floor(microtime(true) * 1000);
    $signature = sign_body($rawBody, $timestamp, $webhookSecret);

    $ch = curl_init($apiBase . '/api/v1/order/create');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'X-Bolt-Key: ' . $apiKey,
            'X-Bolt-Timestamp: ' . $timestamp,
            'X-Bolt-Signature: ' . $signature,
        ],
        CURLOPT_POSTFIELDS => $rawBody,
        CURLOPT_TIMEOUT => 20,
    ]);

    $response = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($response === false) {
        fwrite(STDERR, curl_error($ch) . PHP_EOL);
        curl_close($ch);
        exit(1);
    }
    curl_close($ch);

    echo "HTTP {$status}\n";
    echo $response . "\n";
}

function verify_webhook(string $rawBody, string $timestamp, string $signature): bool
{
    global $webhookSecret;

    if ($timestamp === '' || $signature === '') {
        return false;
    }

    if (abs((int) floor(microtime(true) * 1000) - (int) $timestamp) > 5 * 60 * 1000) {
        return false;
    }

    $expected = sign_body($rawBody, $timestamp, $webhookSecret);
    return hash_equals(strtolower($expected), strtolower($signature));
}

function handle_webhook_request(): void
{
    $rawBody = file_get_contents('php://input');
    $timestamp = $_SERVER['HTTP_X_BOLT_WEBHOOK_TIMESTAMP'] ?? '';
    $signature = $_SERVER['HTTP_X_BOLT_WEBHOOK_SIGNATURE'] ?? '';

    header('Content-Type: application/json');

    if (!verify_webhook($rawBody, $timestamp, $signature)) {
        http_response_code(401);
        echo json_encode(['error' => 'invalid_signature']);
        return;
    }

    $event = json_decode($rawBody, true);
    error_log('Verified BoltUtil webhook: ' . json_encode($event));

    // TODO: update your local order by $event['externalOrderId'].
    // Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

    echo json_encode(['status' => 'SUCCESS']);
}

$command = $argv[1] ?? '';
if ($command === 'create') {
    create_order($argv[2] ?? 'TRC20');
} elseif ($command === 'webhook') {
    echo "Run with PHP built-in server:\n";
    echo "php -S 0.0.0.0:3000 boltutil_demo.php\n";
    echo "Then configure notifyUrl as https://your-domain/webhooks/boltutil via a public HTTPS tunnel.\n";
} elseif (PHP_SAPI !== 'cli'
    && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST'
    && parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) === '/webhooks/boltutil') {
    handle_webhook_request();
} else {
    echo "Usage:\n";
    echo "  php boltutil_demo.php create TRC20\n";
    echo "  php boltutil_demo.php create ERC20\n";
    echo "  php boltutil_demo.php create BEP20\n";
    echo "  php boltutil_demo.php create POLYGON\n";
    echo "  php boltutil_demo.php create SOLANA\n";
    echo "  php -S 0.0.0.0:3000 boltutil_demo.php\n";
}
