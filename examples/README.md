# BoltUtil merchant API examples / 商户开发示例

These six server-side demos use **`POST /api/v1/order/create`**. They do not use the WordPress `/payments` API. Code contains detailed Chinese comments; the protocol and commands below are shared by all languages.

这些示例用于服务端建单与回调验签联调，不含您的数据库、持久去重、发货或邮件任务。默认回调返回 **503**，防止未保存订单就误确认通知；只有在本地联调时才设置 `BOLT_DEMO_ACK=1`，此时验签并校验基本 JSON 结构后返回 **204**，不代表完成业务入账。

## 1. Configure / 配置

Get the merchant API key and the **active Webhook secret from the same merchant account**. This API signs requests with the Webhook secret; do not substitute WordPress/scoped integration credentials.

密钥只放服务端，不写入代码、浏览器或 Git。下列值是占位符，请自行替换。`.env.example` 不会被 Demo 自动加载；在终端 export，或由应用的配置系统注入。

```bash
export BOLT_API_BASE='https://api.boltutil.com'
export BOLT_API_KEY='bt_live_REPLACE_WITH_YOUR_KEY'
export BOLT_WEBHOOK_SECRET='REPLACE_WITH_YOUR_ACTIVE_WEBHOOK_SECRET'
export BOLT_NOTIFY_URL='https://merchant.example.com/webhooks/boltutil'
export BOLT_RETURN_URL='https://merchant.example.com/orders/return'
# Optional: use a stable local business order ID, 6–64 characters: A–Z a–z 0–9 _ -.
# Production must save this ID before sending; reuse/query it after a timeout.
export BOLT_EXTERNAL_ORDER_ID='SHOP_ORDER_20261016_001'
# Local webhook listener, behind a public HTTPS reverse proxy/tunnel:
export BOLT_LISTEN_HOST='127.0.0.1'
export PORT='3000'
# LOCAL TEST ONLY: acknowledge without database fulfillment. Omit in production.
# export BOLT_DEMO_ACK='1'
```

`notifyUrl` must be public HTTPS and meet the platform's URL policy. Loopback HTTP is only used for the local listener and mock tests. Keep TLS certificate validation enabled. API requests time out after 20 seconds and do not follow redirects with credentials. Production receivers also need proxy-level body/time/connection limits; language built-in demo servers are not a production web stack.

## 2. Run / 运行

Every language accepts `create [NETWORK] [CURRENCY] [AMOUNT]`, defaults **TRC20 USDT 1.00**. `webhook` starts the local receiver (PHP uses its built-in server command). API requests with real credentials create real payment orders; this repository does not include a sandbox account.

| Runtime | Create a Polygon USDC order | Receive webhooks |
|---|---|---|
| Node.js 22+ (prefer maintained LTS) | `node examples/node/boltutil-demo.js create POLYGON USDC 1.09` | `node examples/node/boltutil-demo.js webhook` |
| Python 3.10+ | `python3 examples/python/boltutil_demo.py create POLYGON USDC 1.09` | `python3 examples/python/boltutil_demo.py webhook` |
| 64-bit PHP 8.2+ with cURL | `php examples/php/boltutil_demo.php create POLYGON USDC 1.09` | `php -S 127.0.0.1:3000 examples/php/boltutil_demo.php` |
| Go 1.22+ | `go run examples/go/boltutil_demo.go create POLYGON USDC 1.09` | `go run examples/go/boltutil_demo.go webhook` |
| Java 11+ with Maven | See below | See below |
| .NET 8 SDK | `dotnet run --project examples/csharp -- create POLYGON USDC 1.09` | `dotnet run --project examples/csharp -- webhook` |

Java uses Gson for safe serialization, strict JSON parsing and `BigDecimal` amounts. Build first; the old bare `javac BoltUtilDemo.java` command no longer applies:

```bash
cd examples/java
mvn package dependency:copy-dependencies
java -cp 'target/classes:target/dependency/*' BoltUtilDemo create POLYGON USDC 1.09
java -cp 'target/classes:target/dependency/*' BoltUtilDemo webhook
# Windows uses ; instead of : in the Java classpath.
```

### Network/currency matrix

| Network value | USDT | USDC |
|---|---|---|
| `TRC20` | Tether USDT | Not supported |
| `ERC20` | Tether USDT | Native USDC |
| `BEP20` | Configured BNB-chain USDT | Binance-Peg USDC |
| `POLYGON` | Configured Polygon USDT | Native USDC |
| `SOLANA` | Tether USDT | Native USDC |
| `BASE` | Configured bridged USDT | Native USDC |

The merchant must activate the service, enable that network/asset and configure an active receiving wallet. This table does not guarantee every route is enabled for your account. Check the returned asset/network and exact token representation before paying; never transfer a different bridged variant.

## 3. Request signing / 建单与签名

All demos submit this shape (exact JSON property order/whitespace may differ):

```json
{
  "amount": 1.09,
  "externalOrderId": "SHOP_ORDER_20261016_001",
  "network": "POLYGON",
  "currency": "USDC",
  "notifyUrl": "https://merchant.example.com/webhooks/boltutil",
  "returnUrl": "https://merchant.example.com/orders/return?order=SHOP_ORDER_20261016_001",
  "expiredMinutes": 30,
  "orderDesc": "BoltUtil demo order",
  "metadata": {"source": "merchant-demo"}
}
```

- `amount`: base minimum **1.00** (the selected route may require more), maximum 18 integer digits and 6 decimal places. Demos take decimal text, serialize it as an exact JSON **number**, never calculate money with binary floats.
- `externalOrderId`: unique within the merchant, 6–64 allowed characters. Demos generate a random ID if not configured. Production must use and save a stable local order ID; do not generate a fresh one on every retry.
- `expiredMinutes`: 30 in demos; API range 15–60, with account-plan restrictions (free orders use a fixed 30 minutes).
- `metadata`: optional, maximum 10 keys; keep personal data out of sample requests/logs.
- URL length: maximum 255 characters. Return URLs retain existing query parameters/fragments. Never treat a browser return/redirect as payment proof.

Headers:

```text
Content-Type: application/json
X-Bolt-Key: <merchant API key>
X-Bolt-Timestamp: <current Unix milliseconds, 13 digits>
X-Bolt-Signature: <hex HMAC-SHA256>

signature = HMAC_SHA256_HEX(active_webhook_secret, timestamp + "." + exact_raw_UTF8_body)
```

Serialize once, sign those bytes, send exactly those bytes. Do not reformat JSON, change spaces or use a Unix timestamp in seconds. Keep the machine clock synchronized. Both HTTP status and response `code` must indicate success (`code: 200`); an HTTP 200 response can contain a business error.

The response envelope contains `data.checkoutUrl`, `data.orderToken`, `data.merchantExternalId`, `data.payment` and `data.time`. Save the response alongside your local order. **Use `data.payment.amount`, `currency`, `network` and `address` returned by BoltUtil**; the actual payable amount can include a decimal offset for matching. Do not round it or replace it with the original request amount.

A timeout does not prove order creation failed. Query **`POST /api/v1/order/status`** with the same merchant credentials/signing rule and `{"externalOrderId":"..."}` before retrying. `DUPLICATE_EXTERNAL_ID` is not a new payable order. Do not assume `/order/create` provides the idempotency contract of the separate WordPress API.

## 4. Webhook verification and fulfillment / 回调与履约

`/order/create` sends a **flat** JSON callback. It is not the WordPress `{type,data}` envelope. Typical relevant fields:

```json
{
  "eventId": "evt_demo_stable_id",
  "externalOrderId": "SHOP_ORDER_20261016_001",
  "status": "CONFIRMED",
  "network": "POLYGON",
  "currency": "USDC",
  "amount": "1.091",
  "paidAmount": "1.091",
  "shortfallAmount": "0",
  "settlementType": "EXACT",
  "manuallyAccepted": false,
  "destinationAddress": "<merchant receiving address>",
  "txHash": "<transaction hash>",
  "metadata": {"source": "merchant-demo"}
}
```

The amount above illustrates an offset, not a fixed fee or guaranteed offset. Other fields include confirmations and payment/confirmation/completion times; values can depend on status.

Headers are **`X-Bolt-Webhook-Timestamp`** and **`X-Bolt-Webhook-Signature`**, using the same HMAC formula over the received raw bytes. The demos reject timestamps outside ±5 minutes, malformed timestamp/signature values and request bodies over **64 KiB** (a demo limit, not an advertised platform maximum).

Production implementation checklist (also annotated inside every language's callback handler):

1. Read a bounded raw body, verify timestamp and constant-time HMAC, then parse JSON.
2. Find the order by **your authenticated merchant context + externalOrderId**, not an identity supplied in metadata. Match saved network, currency, receiving address and exact returned payable amount using decimal arithmetic.
3. Only accept a confirmed payment state. `CONFIRMED` means chain confirmation; `COMPLETED` means the callback has been delivered. The initial callback can contain `CONFIRMED`: do not wait exclusively for `COMPLETED`, and do not fulfill twice when a later callback changes this status.
4. Interpret `paidAmount`, `shortfallAmount`, `settlementType` and `manuallyAccepted`. A manually accepted underpayment is not proof of full payment; apply an explicit business policy.
5. Use a durable inbox/unique constraint for stable `eventId` (older events may omit it) and a transaction/unique order fulfillment record. Handle legacy events by local order identity and transaction evidence. Time-window checks alone do **not** prevent replay within five minutes.
6. Commit the order change or enqueue to a **durable** job queue before returning any HTTP **2xx**. For an already persisted duplicate, return 2xx again. For temporary persistence failures, return 5xx so delivery can retry. Handle fulfillment and email asynchronously and idempotently.

**Any HTTP 2xx acknowledges delivery**; `204 No Content` is sufficient. `{"status":"SUCCESS"}` is not required. Do not ACK first and then perform work that can be lost on a crash. `BOLT_DEMO_ACK=1` deliberately skips database fulfillment and is exclusively for transport/signature testing; remove it when implementing the production handler.

## 5. Local contract tests / 本地协议测试

```bash
# Select installed runtimes, or use all six. No real API keys or real orders are used.
python3 examples/tests/contract_test.py --languages node python go java csharp php
```

The harness uses only a loopback mock API and a synthetic Webhook secret. It checks all 11 supported network/asset pairs, exact decimal serialization, raw-body signatures, response failures, invalid inputs, return URL handling, invalid/replayed timestamps, malformed JSON, body limits and the default no-fulfillment acknowledgement policy. These tests are protocol checks, **not** a live payment/chain/Webhook end-to-end certification.

## References

- [Developer documentation](https://boltutil.com/zh/developer-docs)
- [Create order](https://boltutil.com/zh/docs/create-order)
- [Webhook signatures](https://boltutil.com/zh/docs/webhook-signature)
- [Public OpenAPI](../openapi.yaml) and [Postman collection](../postman/BoltUtil.postman_collection.json)
