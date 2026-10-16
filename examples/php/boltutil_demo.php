<?php
/**
 * BoltUtil 商户接入示例 / Merchant demo (64-bit PHP 8.2+, cURL).
 * 只调用 POST /api/v1/order/create，不调用 WordPress /payments。
 * 建单 → 保存付款信息 → checkoutUrl → 验签回调 → 数据库事务入账。
 * 不包含数据库/发货实现；生产改造见 handle_verified_event。密钥只存在服务端环境变量。
 */
const MAX_BODY = 65536; // Demo 接收上限，不是平台全局 API 限额。
function secret(): string { return getenv('BOLT_WEBHOOK_SECRET') ?: ''; }
function require_secret(): void {
    if (secret() === '' || preg_match('/^(YOUR_|whsec_xxx)/', secret())) {
        throw new RuntimeException('Set BOLT_WEBHOOK_SECRET');
    }
}
function sign_body(string $body, string $timestamp): string {
    // 毫秒时间戳 + 点 + 原始 UTF-8 body。不能验签前先 decode 再 encode。
    return hash_hmac('sha256', $timestamp . '.' . $body, secret());
}
function verify_webhook(string $body, string $timestamp, string $signature): bool {
    if (!preg_match('/^[0-9]{13}$/D', $timestamp) || !preg_match('/^[a-fA-F0-9]{64}$/D', $signature)) return false;
    if (abs((int) floor(microtime(true) * 1000) - (int) $timestamp) > 300000) return false;
    return hash_equals(sign_body($body, $timestamp), strtolower($signature));
}
function create_order(string $network = 'TRC20', string $currency = 'USDT', string $amount = '1.00'): void {
    require_secret();
    $key = getenv('BOLT_API_KEY') ?: '';
    if ($key === '' || preg_match('/^(YOUR_|bt_live_xxx)/', $key)) throw new RuntimeException('Set BOLT_API_KEY');
    $network = strtoupper($network); $currency = strtoupper($currency);
    if (!in_array($network, ['TRC20', 'ERC20', 'BEP20', 'POLYGON', 'SOLANA', 'BASE'], true)
        || !in_array($currency, ['USDT', 'USDC'], true) || ($network === 'TRC20' && $currency === 'USDC')) {
        throw new RuntimeException('Unsupported network/currency pair');
    }
    // 保留十进制文本，不转 float；最少 1，最多 18 位整数、6 位小数。
    if (!preg_match('/^[1-9][0-9]{0,17}(\.[0-9]{1,6})?$/D', $amount)) throw new RuntimeException('Amount must be >= 1, max 6 decimals');
    $id = getenv('BOLT_EXTERNAL_ORDER_ID') ?: 'INV-' . bin2hex(random_bytes(16));
    if (!preg_match('/^[A-Za-z0-9_-]{6,64}$/D', $id)) throw new RuntimeException('Invalid externalOrderId');
    $notify = getenv('BOLT_NOTIFY_URL') ?: '';
    if (strpos($notify, 'https://') !== 0) throw new RuntimeException('Set a public HTTPS BOLT_NOTIFY_URL');
    $returnUrl = getenv('BOLT_RETURN_URL') ?: 'https://merchant.example.com/orders/return';
    // 在 fragment 前追加参数，保留已有 query；业务可直接配置固定 returnUrl 自行查单。
    $parts = explode('#', $returnUrl, 2);
    $returnUrl = $parts[0] . (strpos($parts[0], '?') === false ? '?' : '&') . 'order=' . rawurlencode($id)
        . (isset($parts[1]) ? '#' . $parts[1] : '');
    $payload = ['amount' => $amount, 'externalOrderId' => $id, 'network' => $network, 'currency' => $currency,
        'notifyUrl' => $notify, 'returnUrl' => $returnUrl, 'expiredMinutes' => 30,
        'orderDesc' => 'BoltUtil demo order', 'metadata' => ['source' => 'php-demo']];
    $body = json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
    // 仅替换已严格校验的 amount 为 JSON number，其余字符串都由 JSON 库安全转义。
    $body = str_replace('"amount":"' . $amount . '"', '"amount":' . $amount, $body);
    $timestamp = (string) (int) floor(microtime(true) * 1000);
    $ch = curl_init(rtrim(getenv('BOLT_API_BASE') ?: 'https://api.boltutil.com', '/') . '/api/v1/order/create');
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 10, CURLOPT_TIMEOUT => 20, CURLOPT_FOLLOWLOCATION => false,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'X-Bolt-Key: ' . $key,
            'X-Bolt-Timestamp: ' . $timestamp, 'X-Bolt-Signature: ' . sign_body($body, $timestamp)], CURLOPT_POSTFIELDS => $body]);
    echo 'externalOrderId: ' . $id . PHP_EOL; // 超时后按同一订单号查询，不能盲目新建。
    $response = curl_exec($ch); $status = curl_getinfo($ch, CURLINFO_HTTP_CODE); $error = curl_error($ch); curl_close($ch);
    if ($response === false) throw new RuntimeException($error);
    $result = json_decode($response, true, 512, JSON_THROW_ON_ERROR);
    if ($status < 200 || $status >= 300 || ($result['code'] ?? 0) !== 200) throw new RuntimeException('Create failed: ' . $response);
    // 保存 data.payment.amount/network/currency/address，向用户展示返回金额（可能有匹配偏移）。
    echo $response . PHP_EOL;
}
function handle_verified_event($event): int {
    if (!is_object($event) || !is_string($event->externalOrderId ?? null) || !is_string($event->status ?? null)) return 400;
    // TODO：按当前商户 + externalOrderId 查本地订单，核对网络、币种、地址与返回付款金额。
    // 金额使用 BCMath/十进制库，不能 float；少付人工接受需要单独业务授权。
    // 只处理 CONFIRMED/COMPLETED（链上确认/回调送达），不是两笔付款。
    // 用 eventId（旧事件可能没有）+ 数据库唯一约束/事务保证每单只履约一次。
    // 不信任浏览器 returnUrl 或 metadata 作为付款凭证；持久化后才 ACK，失败 5xx，邮件异步发送。
    // 本例默认 503 防止误 ACK；BOLT_DEMO_ACK=1 只用于联调，无生产入账逻辑。
    error_log('Verified webhook received (no fulfillment performed)');
    return getenv('BOLT_DEMO_ACK') === '1' ? 204 : 503;
}
function handle_webhook_request(): void {
    require_secret();
    // 声明长度已超限时尽早拒绝；即使没有 Content-Length，下面仍做有界读取。
    $declared = $_SERVER['CONTENT_LENGTH'] ?? '';
    if (ctype_digit((string) $declared) && (strlen((string) $declared) > 9 || (int) $declared > MAX_BODY)) {
        http_response_code(413); return;
    }
    // 最多读上限 + 1 字节，不仅依赖客户端声明的 Content-Length。
    $body = file_get_contents('php://input', false, null, 0, MAX_BODY + 1);
    if ($body === false) { http_response_code(400); return; }
    if (strlen($body) > MAX_BODY) { http_response_code(413); return; }
    if (!verify_webhook($body, $_SERVER['HTTP_X_BOLT_WEBHOOK_TIMESTAMP'] ?? '', $_SERVER['HTTP_X_BOLT_WEBHOOK_SIGNATURE'] ?? '')) {
        http_response_code(401); return;
    }
    try { $event = json_decode($body, false, 512, JSON_THROW_ON_ERROR); }
    catch (JsonException $e) { http_response_code(400); return; }
    http_response_code(handle_verified_event($event));
}
// 允许单元测试只加载函数，不启动 CLI 或 HTTP 处理。
if (!defined('BOLT_DEMO_LIBRARY')) {
    try {
        if (PHP_SAPI !== 'cli') {
            if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && ($_SERVER['REQUEST_URI'] ?? '') === '/webhooks/boltutil') handle_webhook_request();
            else http_response_code(404);
        } elseif (($argv[1] ?? '') === 'create') {
            create_order($argv[2] ?? 'TRC20', $argv[3] ?? 'USDT', $argv[4] ?? '1.00');
        } else {
            echo "php boltutil_demo.php create POLYGON USDC 1.09\nphp -S 127.0.0.1:3000 boltutil_demo.php\n";
        }
    } catch (Throwable $e) {
        error_log($e->getMessage());
        if (PHP_SAPI === 'cli') exit(1);
        http_response_code(503);
    }
}
