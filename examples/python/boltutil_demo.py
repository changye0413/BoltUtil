"""BoltUtil 商户接入示例 / Merchant demo (Python 3.10+).
只使用 POST /api/v1/order/create；不是 WordPress /payments 接口。
流程：服务端建单 → 保存付款信息 → checkoutUrl → 验签回调 → 数据库事务入账。
示例不连接数据库、不发货；接入生产前必须实现 handle_verified_event 内的步骤。
密钥只能存储在服务端环境变量，不能放到浏览器或提交进 Git。
"""
import hashlib
import hmac
import json
import os
import re
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

SECRET = os.getenv('BOLT_WEBHOOK_SECRET', '')
MAX_BODY = 64 * 1024  # Demo 上限，可按业务调整；不是平台全局限制。


def require_secret():
    if not SECRET or SECRET.startswith(('YOUR_', 'whsec_xxx')):
        raise ValueError('Set BOLT_WEBHOOK_SECRET')


def sign_body(body: bytes, timestamp: str) -> str:
    # 毫秒时间戳 + 点 + 原始 UTF-8 字节。签名后必须发送同一份 body。
    return hmac.new(SECRET.encode(), timestamp.encode() + b'.' + body, hashlib.sha256).hexdigest()


def verify_webhook(body: bytes, timestamp: str, signature: str) -> bool:
    if not re.fullmatch(r'[0-9]{13}', timestamp) or not re.fullmatch(r'[a-fA-F0-9]{64}', signature):
        return False
    if abs(int(time.time() * 1000) - int(timestamp)) > 300000:
        return False
    return hmac.compare_digest(sign_body(body, timestamp), signature.lower())


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # 禁止把签名和密钥转发到跳转目标。


def create_order(network='TRC20', currency='USDT', amount='1.00'):
    require_secret()
    key = os.getenv('BOLT_API_KEY', '')
    if not key or key.startswith(('YOUR_', 'bt_live_xxx')):
        raise ValueError('Set BOLT_API_KEY')
    network, currency = network.upper(), currency.upper()
    if network not in ('TRC20', 'ERC20', 'BEP20', 'POLYGON', 'SOLANA', 'BASE') or currency not in ('USDT', 'USDC') or (network == 'TRC20' and currency == 'USDC'):
        raise ValueError('Unsupported network/currency pair')
    # 金额保留十进制文本，不使用 float；最少 1，最多 18 位整数、6 位小数。
    if not re.fullmatch(r'[1-9][0-9]{0,17}(\.[0-9]{1,6})?', amount):
        raise ValueError('Amount must be >= 1, max 6 decimals')
    external_id = os.getenv('BOLT_EXTERNAL_ORDER_ID') or 'INV-' + str(uuid.uuid4())
    if not re.fullmatch(r'[A-Za-z0-9_-]{6,64}', external_id):
        raise ValueError('Invalid externalOrderId')
    notify = os.getenv('BOLT_NOTIFY_URL', '')
    if not notify.startswith('https://'):
        raise ValueError('Set a public HTTPS BOLT_NOTIFY_URL')
    url = urlsplit(os.getenv('BOLT_RETURN_URL', 'https://merchant.example.com/orders/return'))
    query = dict(parse_qsl(url.query, keep_blank_values=True))
    query['order'] = external_id  # 保留 URL 原有参数与 fragment。
    payload = dict(externalOrderId=external_id, network=network, currency=currency,
                   notifyUrl=notify, returnUrl=urlunsplit(url._replace(query=urlencode(query))),
                   expiredMinutes=30, orderDesc='BoltUtil demo order', metadata={'source': 'python-demo'})
    # amount 严格正则校验后作为 JSON 数字拼入，其余字符串统一 JSON 转义。
    # 这样不会经过 float 丢失精度，也符合文档 amount:number 的格式。
    body = ('{"amount":' + amount + ',' + json.dumps(payload, ensure_ascii=False, separators=(',', ':'))[1:]).encode()
    timestamp = str(int(time.time() * 1000))
    request = Request(os.getenv('BOLT_API_BASE', 'https://api.boltutil.com').rstrip('/') + '/api/v1/order/create',
                      data=body, method='POST', headers={'Content-Type': 'application/json',
                      'X-Bolt-Key': key, 'X-Bolt-Timestamp': timestamp, 'X-Bolt-Signature': sign_body(body, timestamp)})
    print('externalOrderId:', external_id, flush=True)  # 超时后按此订单号查询，不盲目新建。
    with build_opener(NoRedirect()).open(request, timeout=20) as response:
        result = json.load(response)
    if result.get('code') != 200:
        raise ValueError('Create failed: ' + json.dumps(result))
    # 保存 data.payment 的 amount/network/currency/address；付款金额可能包含匹配偏移。
    print(json.dumps(result, ensure_ascii=False, indent=2))


def handle_verified_event(event):
    if not isinstance(event, dict) or not isinstance(event.get('externalOrderId'), str) or not isinstance(event.get('status'), str):
        return 400
    # TODO 生产：用当前商户 + externalOrderId 查本地订单，核对币种、网络、地址与返回的精确金额。
    # amount/paidAmount 用 decimal.Decimal 比较；少付人工接受不能自动当足额付款。
    # 仅 CONFIRMED/COMPLETED 可处理付款；前者是链上确认，后者是回调送达，不是两笔付款。
    # eventId 在重试时稳定（旧事件可能没有）。数据库唯一约束 + 事务/持久队列保证每单只履约一次。
    # 不能以 returnUrl 或 metadata 里的身份作为付款凭证；不要在回调中同步发邮件。
    # 持久化成功/已处理的重复事件返回 2xx，失败返回 5xx；此处默认 503，避免丢通知。
    print('Verified webhook received (no fulfillment performed)', flush=True)
    return 204 if os.getenv('BOLT_DEMO_ACK') == '1' else 503  # 仅联调时显式开启。


class BoltUtilWebhookHandler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(15)  # 防止慢请求无限占用线程。

    def reply(self, status):
        self.send_response(status)
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_POST(self):
        if self.path != '/webhooks/boltutil':
            self.reply(404)
            return
        # 此标准库示例不支持 chunked；应由反向代理规范化为 Content-Length。
        length = self.headers.get('Content-Length', '')
        if self.headers.get('Transfer-Encoding') or not re.fullmatch(r'[0-9]{1,9}', length):
            self.reply(400)
            return
        if int(length) > MAX_BODY:
            self.reply(413)
            return
        try:
            body = self.rfile.read(int(length))
            if len(body) != int(length):
                self.reply(400)
                return
            if not verify_webhook(body, self.headers.get('X-Bolt-Webhook-Timestamp', ''), self.headers.get('X-Bolt-Webhook-Signature', '')):
                self.reply(401)
                return
            self.reply(handle_verified_event(json.loads(body.decode('utf-8'))))
        except (ValueError, UnicodeError, OSError):
            self.reply(400)


def start_webhook_server():
    require_secret()
    server = ThreadingHTTPServer((os.getenv('BOLT_LISTEN_HOST', '127.0.0.1'), int(os.getenv('PORT', '3000'))), BoltUtilWebhookHandler)
    print('Webhook listener ready; use HTTPS reverse proxy', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    try:
        command = sys.argv[1] if len(sys.argv) > 1 else ''
        if command == 'create':
            create_order(*sys.argv[2:5])
        elif command == 'webhook':
            start_webhook_server()
        else:
            print('python3 boltutil_demo.py create POLYGON USDC 1.09 | webhook')
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
