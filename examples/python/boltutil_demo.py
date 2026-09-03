import hashlib
import hmac
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError

API_BASE = os.getenv("BOLT_API_BASE", "https://api.boltutil.com")
API_KEY = os.getenv("BOLT_API_KEY", "YOUR_API_KEY")
WEBHOOK_SECRET = os.getenv("BOLT_WEBHOOK_SECRET", "YOUR_WEBHOOK_SECRET")
NOTIFY_URL = os.getenv("BOLT_NOTIFY_URL", "https://merchant.example.com/webhooks/boltutil")
RETURN_URL = os.getenv("BOLT_RETURN_URL", "https://merchant.example.com/orders/return")


def hmac_sha256_hex(payload: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def sign_body(raw_body: str, timestamp: str) -> str:
    return hmac_sha256_hex(f"{timestamp}.{raw_body}", WEBHOOK_SECRET)


def create_order(network: str = "TRC20") -> None:
    external_order_id = f"INV-{int(time.time() * 1000)}"
    payload = {
        "amount": 25.0,
        "externalOrderId": external_order_id,
        "network": network,
        "currency": "USDT",
        "orderDesc": "BoltUtil demo order",
        "notifyUrl": NOTIFY_URL,
        "returnUrl": f"{RETURN_URL}?order={external_order_id}",
        "expiredMinutes": 30,
        "metadata": {
            "customerId": "CUS_1001",
            "source": "python-demo",
        },
    }
    raw_body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    timestamp = str(int(time.time() * 1000))
    signature = sign_body(raw_body, timestamp)

    request = Request(
        f"{API_BASE}/api/v1/order/create",
        data=raw_body.encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Bolt-Key": API_KEY,
            "X-Bolt-Timestamp": timestamp,
            "X-Bolt-Signature": signature,
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            print("HTTP", response.status)
            print(response.read().decode("utf-8"))
    except HTTPError as error:
        print("HTTP", error.code)
        print(error.read().decode("utf-8"))


def verify_webhook(raw_body: str, timestamp: str, signature: str) -> bool:
    if not timestamp or not signature:
        return False
    if abs(int(time.time() * 1000) - int(timestamp)) > 5 * 60 * 1000:
        return False
    expected = sign_body(raw_body, timestamp)
    return hmac.compare_digest(expected.lower(), signature.lower())


class BoltUtilWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/webhooks/boltutil":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")
        timestamp = self.headers.get("X-Bolt-Webhook-Timestamp", "")
        signature = self.headers.get("X-Bolt-Webhook-Signature", "")

        if not verify_webhook(raw_body, timestamp, signature):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"invalid_signature"}')
            return

        event = json.loads(raw_body)
        print("Verified BoltUtil webhook:", event)

        # TODO: update your local order by event["externalOrderId"].
        # Only fulfill when status is CONFIRMED or COMPLETED, according to your business rules.

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"SUCCESS"}')


def start_webhook_server(port: int = 3000) -> None:
    server = HTTPServer(("0.0.0.0", port), BoltUtilWebhookHandler)
    print(f"BoltUtil webhook demo listening on http://localhost:{port}/webhooks/boltutil")
    server.serve_forever()


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "create":
        create_order(sys.argv[2] if len(sys.argv) > 2 else "TRC20")
    elif command == "webhook":
        start_webhook_server(int(os.getenv("PORT", "3000")))
    else:
        print("Usage:")
        print("  python3 boltutil_demo.py create TRC20")
        print("  python3 boltutil_demo.py create ERC20")
        print("  python3 boltutil_demo.py create BEP20")
        print("  python3 boltutil_demo.py create POLYGON")
        print("  python3 boltutil_demo.py create SOLANA")
        print("  python3 boltutil_demo.py webhook")
