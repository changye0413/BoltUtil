# BoltUtil API Examples

This folder contains minimal merchant-side examples for integrating BoltUtil.

Each language demo includes:

- Create a USDT payment order.
- Sign merchant API requests with HMAC-SHA256.
- Receive BoltUtil payment webhooks.
- Verify webhook signatures before fulfilling an order.

## API Basics

Base URL:

```text
https://api.boltutil.com
```

Create order endpoint:

```text
POST /api/v1/order/create
```

Merchant API headers:

```text
X-Bolt-Key: YOUR_API_KEY
X-Bolt-Timestamp: 1770643296609
X-Bolt-Signature: hmac_sha256_hex(timestamp + "." + raw_json_body, WEBHOOK_SECRET)
Content-Type: application/json
```

Webhook headers sent by BoltUtil:

```text
X-Bolt-Webhook-Timestamp: 1770643296609
X-Bolt-Webhook-Signature: hmac_sha256_hex(timestamp + "." + raw_webhook_body, WEBHOOK_SECRET)
Content-Type: application/json
```

Your webhook endpoint must return:

```json
{ "status": "SUCCESS" }
```

## Environment Variables

Set these before running any demo:

```bash
export BOLT_API_BASE="https://api.boltutil.com"
export BOLT_API_KEY="bt_live_xxx"
export BOLT_WEBHOOK_SECRET="whsec_xxx"
export BOLT_NOTIFY_URL="https://merchant.example.com/webhooks/boltutil"
export BOLT_RETURN_URL="https://merchant.example.com/orders/return"
```

## Supported Networks

Use one of:

```text
TRC20
ERC20
BEP20
```

## Important Security Notes

- Keep `BOLT_API_KEY` and `BOLT_WEBHOOK_SECRET` only on your server.
- Never generate signatures in browser code or mobile app code.
- Verify every webhook signature before updating balances, shipping goods, or activating subscriptions.
- Use the raw request body exactly as received when verifying webhook signatures.
- Reject webhooks with timestamps older than 5 minutes.

## Examples

| Language | File |
|---|---|
| Node.js | `node/boltutil-demo.js` |
| Python | `python/boltutil_demo.py` |
| PHP | `php/boltutil_demo.php` |
| Go | `go/boltutil_demo.go` |
| Java | `java/BoltUtilDemo.java` |
| C# | `csharp/BoltUtilDemo.cs` |

## Run Commands

Node.js 18+:

```bash
cd examples/node
node boltutil-demo.js create TRC20
node boltutil-demo.js webhook
```

Python 3:

```bash
cd examples/python
python3 boltutil_demo.py create TRC20
python3 boltutil_demo.py webhook
```

PHP with cURL extension:

```bash
cd examples/php
php boltutil_demo.php create TRC20
php -S 0.0.0.0:3000 boltutil_demo.php
```

Go:

```bash
cd examples/go
go run boltutil_demo.go create TRC20
go run boltutil_demo.go webhook
```

Java 11+:

```bash
cd examples/java
javac BoltUtilDemo.java
java BoltUtilDemo create TRC20
java BoltUtilDemo webhook
```

.NET 8:

```bash
cd examples/csharp
dotnet run -- create TRC20
dotnet run -- webhook
```

## Typical Flow

1. Your backend creates an order with `POST /api/v1/order/create`.
2. Show `checkoutUrl`, payment address, QR data, network, and exact amount to the customer.
3. Customer transfers USDT on TRC20, ERC20, or BEP20.
4. BoltUtil monitors the chain and sends a signed webhook after confirmation.
5. Your backend verifies the webhook signature and marks the local order as paid.
