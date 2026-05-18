const http = require("http");
const crypto = require("crypto");

const API_BASE = process.env.BOLT_API_BASE || "https://api.boltutil.com";
const API_KEY = process.env.BOLT_API_KEY || "YOUR_API_KEY";
const WEBHOOK_SECRET = process.env.BOLT_WEBHOOK_SECRET || "YOUR_WEBHOOK_SECRET";
const NOTIFY_URL = process.env.BOLT_NOTIFY_URL || "https://merchant.example.com/webhooks/boltutil";
const RETURN_URL = process.env.BOLT_RETURN_URL || "https://merchant.example.com/orders/return";

function hmacSha256Hex(payload, secret) {
  return crypto.createHmac("sha256", secret).update(payload, "utf8").digest("hex");
}

function timingSafeEqualHex(a, b) {
  const left = Buffer.from(String(a || "").toLowerCase(), "utf8");
  const right = Buffer.from(String(b || "").toLowerCase(), "utf8");
  return left.length === right.length && crypto.timingSafeEqual(left, right);
}

function signBody(rawBody, timestamp) {
  return hmacSha256Hex(`${timestamp}.${rawBody}`, WEBHOOK_SECRET);
}

async function createOrder(network = "TRC20") {
  const externalOrderId = `INV-${Date.now()}`;
  const body = JSON.stringify({
    amount: 25.0,
    externalOrderId,
    network,
    currency: "USDT",
    orderDesc: "BoltUtil demo order",
    notifyUrl: NOTIFY_URL,
    returnUrl: `${RETURN_URL}?order=${externalOrderId}`,
    expiredMinutes: 30,
    metadata: {
      customerId: "CUS_1001",
      source: "node-demo"
    }
  });

  const timestamp = Date.now().toString();
  const signature = signBody(body, timestamp);

  const response = await fetch(`${API_BASE}/api/v1/order/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Bolt-Key": API_KEY,
      "X-Bolt-Timestamp": timestamp,
      "X-Bolt-Signature": signature
    },
    body
  });

  const text = await response.text();
  console.log("HTTP", response.status);
  console.log(text);
}

function verifyWebhook(rawBody, timestamp, signature) {
  if (!timestamp || !signature) return false;
  if (Math.abs(Date.now() - Number(timestamp)) > 5 * 60 * 1000) return false;

  const expected = signBody(rawBody, timestamp);
  return timingSafeEqualHex(expected, signature);
}

function startWebhookServer(port = 3000) {
  const server = http.createServer((req, res) => {
    if (req.method !== "POST" || req.url !== "/webhooks/boltutil") {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "not_found" }));
      return;
    }

    let rawBody = "";
    req.setEncoding("utf8");
    req.on("data", chunk => {
      rawBody += chunk;
    });
    req.on("end", () => {
      const timestamp = req.headers["x-bolt-webhook-timestamp"];
      const signature = req.headers["x-bolt-webhook-signature"];

      if (!verifyWebhook(rawBody, timestamp, signature)) {
        res.writeHead(401, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "invalid_signature" }));
        return;
      }

      const event = JSON.parse(rawBody);
      console.log("Verified BoltUtil webhook:", event);

      // TODO: update your local order by event.externalOrderId.
      // Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ status: "SUCCESS" }));
    });
  });

  server.listen(port, () => {
    console.log(`BoltUtil webhook demo listening on http://localhost:${port}/webhooks/boltutil`);
  });
}

const command = process.argv[2];
if (command === "create") {
  createOrder(process.argv[3] || "TRC20").catch(err => {
    console.error(err);
    process.exit(1);
  });
} else if (command === "webhook") {
  startWebhookServer(Number(process.env.PORT || 3000));
} else {
  console.log("Usage:");
  console.log("  node boltutil-demo.js create TRC20");
  console.log("  node boltutil-demo.js create ERC20");
  console.log("  node boltutil-demo.js create BEP20");
  console.log("  node boltutil-demo.js webhook");
}

