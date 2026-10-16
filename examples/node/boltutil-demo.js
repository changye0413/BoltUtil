/**
 * BoltUtil 商户接入示例 / Merchant integration demo (Node.js 22+).
 * 只使用 POST /api/v1/order/create；不是 WordPress /payments 接口。
 * 顺序：服务端建单 → 保存返回付款信息 → 跳转 checkoutUrl → 验签回调 → 事务入账。
 * 本文件演示协议，不连接您的数据库，不自动发货；生产改造点见 handleVerifiedEvent。
 * 密钥只从环境变量读取，不能放进前端、仓库、URL 或日志。
 */
const http = require('node:http');
const crypto = require('node:crypto');
const MAX_BODY = 64 * 1024; // Demo 的接收上限，不是 BoltUtil 全局 API 限额。
const SECRET = process.env.BOLT_WEBHOOK_SECRET || '';
const BASE = process.env.BOLT_API_BASE || 'https://api.boltutil.com';

function requireSecret() {
  if (!SECRET || /^(YOUR_|whsec_xxx)/.test(SECRET)) throw new Error('Set BOLT_WEBHOOK_SECRET');
}
// timestamp 必须是毫秒。签名与发送必须复用同一份 UTF-8 原始字节，不能二次序列化。
function signBody(body, timestamp) {
  return crypto.createHmac('sha256', SECRET).update(timestamp + '.').update(body).digest('hex');
}
function verifyWebhook(body, timestamp, signature) {
  if (typeof timestamp !== 'string' || !/^[0-9]{13}$(?![\s\S])/.test(timestamp)
      || typeof signature !== 'string' || !/^[a-fA-F0-9]{64}$(?![\s\S])/.test(signature)) return false;
  if (Math.abs(Date.now() - Number(timestamp)) > 300000) return false;
  return crypto.timingSafeEqual(Buffer.from(signBody(body, timestamp), 'hex'), Buffer.from(signature, 'hex'));
}
function orderInput(network, currency, amount) {
  network = network.toUpperCase(); currency = currency.toUpperCase();
  if (!['TRC20', 'ERC20', 'BEP20', 'POLYGON', 'SOLANA', 'BASE'].includes(network)
      || !['USDT', 'USDC'].includes(currency) || (network === 'TRC20' && currency === 'USDC')) {
    throw new Error('Unsupported network/currency pair (TRC20 supports USDT only)');
  }
  // 使用十进制文本；禁止浮点运算、指数记数、负数，最少 1，最多 18 位整数及 6 位小数。
  if (!/^[1-9][0-9]{0,17}(\.[0-9]{1,6})?$(?![\s\S])/.test(amount)) throw new Error('Amount must be >= 1, max 6 decimals');
  const externalOrderId = process.env.BOLT_EXTERNAL_ORDER_ID || 'INV-' + crypto.randomUUID();
  if (!/^[A-Za-z0-9_-]{6,64}$(?![\s\S])/.test(externalOrderId)) throw new Error('Invalid externalOrderId');
  return { network, currency, amount, externalOrderId };
}
async function createOrder(network = 'TRC20', currency = 'USDT', amount = '1.00') {
  requireSecret();
  const key = process.env.BOLT_API_KEY || '';
  if (!key || /^(YOUR_|bt_live_xxx)/.test(key)) throw new Error('Set BOLT_API_KEY');
  const input = orderInput(network, currency, amount);
  const notifyUrl = process.env.BOLT_NOTIFY_URL || '';
  if (!notifyUrl.startsWith('https://')) throw new Error('Set a public HTTPS BOLT_NOTIFY_URL');
  const returnUrl = new URL(process.env.BOLT_RETURN_URL || 'https://merchant.example.com/orders/return');
  returnUrl.searchParams.set('order', input.externalOrderId); // 保留原有 query 与 fragment。
  const body = JSON.stringify({ ...input, notifyUrl, returnUrl: returnUrl.href,
    expiredMinutes: 30, orderDesc: 'BoltUtil demo order', metadata: { source: 'node-demo' } })
    // amount 已经严格校验；输出精确 JSON number，不经过 JS Number 的浮点转换。
    .replace('"amount":"' + amount + '"', '"amount":' + amount);
  const timestamp = String(Date.now());
  console.log('externalOrderId:', input.externalOrderId); // 超时后用同一个订单号查询，不盲目创建新订单。
  const response = await fetch(BASE.replace(/\/$/, '') + '/api/v1/order/create', {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(20000),
    headers: { 'Content-Type': 'application/json', 'X-Bolt-Key': key,
      'X-Bolt-Timestamp': timestamp, 'X-Bolt-Signature': signBody(body, timestamp) }, body
  });
  const result = await response.json();
  if (!response.ok || result.code !== 200) throw new Error('Create failed: ' + JSON.stringify(result));
  // 存储 data.payment.amount/network/currency/address 及订单号；付款必须用返回金额（可能带匹配偏移）。
  console.log(JSON.stringify(result, null, 2));
}
function handleVerifiedEvent(event) {
  if (!event || typeof event !== 'object' || Array.isArray(event)
      || typeof event.externalOrderId !== 'string' || typeof event.status !== 'string') return 400;
  // TODO 生产：按“当前商户 + externalOrderId”查库，核对 network、currency、收款地址、返回付款金额。
  // amount/paidAmount 用 decimal 比较，不能 parseFloat；少付人工接受需单独业务授权。
  // 只在 CONFIRMED / COMPLETED 时进入付款处理。CONFIRMED=链上确认，COMPLETED=回调已送达。
  // eventId 是重试稳定标识（旧事件可能没有）；用唯一约束 + 事务/持久队列去重，同一订单只履约一次。
  // 浏览器 returnUrl、客户端钱包上报、签名有效本身均不代表已履约。不要信任 metadata 指定的商户身份。
  // 持久化成功（重复且已处理也算成功）再返回 2xx；失败返回 5xx，请勿在回调内同步发邮件。
  // 这里没有实现数据库。默认返回 503 防止误以为已经入账；显式开启 DEMO_ACK 仅用于联调。
  console.log('Verified webhook received (no fulfillment performed)');
  return process.env.BOLT_DEMO_ACK === '1' ? 204 : 503;
}
function startWebhookServer() {
  requireSecret();
  const server = http.createServer((req, res) => {
    const reply = (status) => { if (!res.writableEnded) { res.writeHead(status); res.end(); } };
    if (req.method !== 'POST' || req.url !== '/webhooks/boltutil') { reply(404); req.resume(); return; }
    const chunks = []; let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > MAX_BODY) { reply(413); return; }
      chunks.push(chunk);
    });
    req.on('error', () => reply(400));
    req.on('end', () => {
      if (size > MAX_BODY) return;
      const body = Buffer.concat(chunks);
      if (!verifyWebhook(body, req.headers['x-bolt-webhook-timestamp'], req.headers['x-bolt-webhook-signature'])) {
        reply(401); return;
      }
      try { reply(handleVerifiedEvent(JSON.parse(body.toString('utf8')))); }
      catch { reply(400); } // 已签名但无效的 JSON 也不能让服务崩溃。
    });
  });
  server.requestTimeout = 15000; server.headersTimeout = 10000;
  const host = process.env.BOLT_LISTEN_HOST || '127.0.0.1';
  server.listen(Number(process.env.PORT || 3000), host, () => console.log('Webhook listener ready; use HTTPS reverse proxy'));
}
if (require.main === module) {
  const [command, network, currency, amount] = process.argv.slice(2);
  if (command === 'create') createOrder(network, currency, amount).catch(e => { console.error(e.message); process.exitCode = 1; });
  else if (command === 'webhook') startWebhookServer();
  else console.log('node boltutil-demo.js create POLYGON USDC 1.09 | webhook');
}
module.exports = { signBody, verifyWebhook, orderInput };
