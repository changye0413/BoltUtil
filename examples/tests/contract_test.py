#!/usr/bin/env python3
"""Cross-language contract tests: loopback only, synthetic keys, no real orders.
运行前安装选定语言的运行时。Java/C# 会自动构建；PHP 必须有 cURL。
可用 NODE/PHP_COMMAND/JAVA/DOTNET 环境变量指定命令（允许带参数，例如 PHP WASM CLI）。
"""
import argparse
import contextlib
import hashlib
import hmac
import http.client
import json
import os
from pathlib import Path
import queue
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
SECRET = 'contract-test-only-not-a-real-credential'
KEY = 'bt_live_contract_test_only'
CAPTURE = queue.Queue()
MODE = 'success'
ENV = dict(os.environ, BOLT_API_KEY=KEY, BOLT_WEBHOOK_SECRET=SECRET,
           BOLT_NOTIFY_URL='https://merchant.example.com/webhooks/boltutil',
           BOLT_RETURN_URL='https://merchant.example.com/return?campaign=dev&note=%22hello%22#receipt',
           BOLT_EXTERNAL_ORDER_ID='TEST_ORDER_001', BOLT_LISTEN_HOST='127.0.0.1', BOLT_DEMO_ACK='1')


def signature(body, timestamp):
    return hmac.new(SECRET.encode(), timestamp.encode() + b'.' + body, hashlib.sha256).hexdigest()


class MockAPI(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        try:
            body = self.rfile.read(int(self.headers['Content-Length']))
            ts = self.headers['X-Bolt-Timestamp']
            assert self.path == '/api/v1/order/create'
            assert self.headers['X-Bolt-Key'] == KEY
            assert abs(int(ts) - int(time.time() * 1000)) < 300000
            assert hmac.compare_digest(signature(body, ts), self.headers['X-Bolt-Signature'])
            # parse_float=Decimal checks that JSON numeric money keeps all input digits.
            item = json.loads(body, parse_float=Decimal)
            assert isinstance(item['amount'], (Decimal, int))
            assert item['externalOrderId'] == 'TEST_ORDER_001'
            assert item['expiredMinutes'] == 30
            assert item['notifyUrl'] == ENV['BOLT_NOTIFY_URL']
            returned = urlsplit(item['returnUrl'])
            assert returned.fragment == 'receipt'
            assert parse_qs(returned.query) == {'campaign': ['dev'], 'note': ['"hello"'], 'order': ['TEST_ORDER_001']}
            CAPTURE.put(item)
            if MODE == 'redirect':
                self.send_response(307)
                self.send_header('Location', '/do-not-follow')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            code = 200 if MODE == 'success' else 400
            data = {'code': code, 'message': 'success' if code == 200 else 'DUPLICATE_EXTERNAL_ID',
                    'data': {'checkoutUrl': 'https://merchant.example.com/mock-checkout',
                             'payment': {'amount': '1.091', 'currency': item['currency'], 'network': item['network']}}}
            result = json.dumps(data).encode()
            self.send_response(200)
        except Exception as error:
            CAPTURE.put(error)
            result = str(error).encode()
            self.send_response(400)
        self.send_header('Content-Length', str(len(result)))
        self.end_headers()
        self.wfile.write(result)


def run(cmd, env=None, expected=0):
    p = subprocess.run(cmd, cwd=ROOT, env=env or ENV, capture_output=True, text=True, timeout=90)
    if (p.returncode == 0) != (expected == 0):
        raise AssertionError(f'{cmd}: exit {p.returncode}\n{p.stdout}\n{p.stderr}')
    return p


def commands(language, build):
    if language == 'node':
        return shlex.split(os.getenv('NODE', 'node')) + [str(ROOT / 'node/boltutil-demo.js')]
    if language == 'python':
        return [sys.executable, str(ROOT / 'python/boltutil_demo.py')]
    if language == 'go':
        run(['go', 'build', '-o', str(build / 'go-demo'), str(ROOT / 'go/boltutil_demo.go')])
        return [str(build / 'go-demo')]
    if language == 'java':
        run(['mvn', '-q', '-f', str(ROOT / 'java/pom.xml'), 'package', 'dependency:copy-dependencies'])
        return shlex.split(os.getenv('JAVA', 'java')) + ['-cp', str(ROOT / 'java/target/classes') + os.pathsep + str(ROOT / 'java/target/dependency/*'), 'BoltUtilDemo']
    if language == 'csharp':
        dotnet = shlex.split(os.getenv('DOTNET', 'dotnet'))
        run(dotnet + ['build', str(ROOT / 'csharp/BoltUtilDemo.csproj'), '--nologo'])
        return dotnet + [str(ROOT / 'csharp/bin/Debug/net8.0/BoltUtilDemo.dll')]
    return shlex.split(os.getenv('PHP_COMMAND', 'php')) + [str(ROOT / 'php/boltutil_demo.php')]


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


@contextlib.contextmanager
def receiver(language, cmd, ack):
    port = free_port()
    env = dict(ENV, PORT=str(port), BOLT_DEMO_ACK=ack)
    launch = cmd + ['webhook']
    if language == 'php':
        launch = cmd[:-1] + ['-S', f'127.0.0.1:{port}', cmd[-1]]
    with tempfile.TemporaryFile() as output:
        p = subprocess.Popen(launch, env=env, cwd=ROOT, stdout=output, stderr=output)
        try:
            for _ in range(150):
                if p.poll() is not None:
                    output.seek(0)
                    raise AssertionError(output.read().decode())
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.2):
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise AssertionError('Receiver startup timed out')
            yield port
        finally:
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill(); p.wait()


def post(port, body, timestamp=None, sig=None, path='/webhooks/boltutil'):
    timestamp = timestamp or str(int(time.time() * 1000))
    headers = {'X-Bolt-Webhook-Timestamp': timestamp, 'X-Bolt-Webhook-Signature': sig if sig is not None else signature(body, timestamp)}
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
    try:
        conn.request('POST', path, body=body, headers=headers)
        response = conn.getresponse(); response.read()
        return response.status
    finally:
        conn.close()


def check(language, cmd):
    global MODE
    count = 0
    for network in ('TRC20', 'ERC20', 'BEP20', 'POLYGON', 'SOLANA', 'BASE'):
        for currency in ('USDT', 'USDC'):
            if (network, currency) == ('TRC20', 'USDC'):
                continue
            result = run(cmd + ['create', network, currency, '1.09'])
            captured = CAPTURE.get(timeout=5)
            assert not isinstance(captured, Exception), captured
            assert (captured['network'], captured['currency'], captured['amount']) == (network, currency, Decimal('1.09'))
            assert 'mock-checkout' in result.stdout
            count += 1
    run(cmd + ['create', 'BASE', 'USDC', '999999999999999999.123456'])
    assert CAPTURE.get(timeout=5)['amount'] == Decimal('999999999999999999.123456')
    count += 1
    for args in [('TRC20', 'USDC', '1'), ('UNKNOWN', 'USDT', '1'), ('BASE', 'DAI', '1'),
                 ('BASE', 'USDC', '0.99'), ('BASE', 'USDC', '1.1234567'), ('BASE', 'USDC', '1e3'), ('BASE', 'USDC', '1\n')]:
        run(cmd + ['create', *args], expected=1)
        assert CAPTURE.empty(), 'Invalid input reached API'
        count += 1
    for mode in ('business_error', 'redirect'):
        MODE = mode
        run(cmd + ['create', 'BASE', 'USDC', '1'], expected=1)
        assert isinstance(CAPTURE.get(timeout=5), dict)
        assert CAPTURE.empty(), 'Unexpected redirect or retry'
        count += 1
    MODE = 'success'
    # UTF-8, spaces and a newline ensure raw bytes (not reserialized JSON) are signed.
    body = '{ "eventId":"evt_mock", "externalOrderId":"TEST_ORDER_001", "status":"CONFIRMED", "metadata":{"note":"测试付款"}}\n'.encode()
    with receiver(language, cmd, '1') as port:
        assert post(port, body) == 204
        assert post(port, body) == 204  # transport replay ACK; no fake database dedup claim.
        assert post(port, body.replace(b'CONFIRMED', b'COMPLETED')) == 204
        assert post(port, body, path='/wrong') == 404
        assert post(port, body, sig='f' * 64) == 401
        original_ts = str(int(time.time() * 1000))
        assert post(port, body + b' ', original_ts, signature(body, original_ts)) == 401
        for ts in ('NaN', '0', '-9223372036854775808', str(int(time.time() * 1000) - 301000), str(int(time.time() * 1000) + 301000)):
            assert post(port, body, ts) == 401
        for invalid in (b'{broken', b'null', b'[]', b'{}', b'{}{}'):
            assert post(port, invalid) == 400, (language, invalid)
        oversize_status = post(port, b'x' * 65537)
        assert oversize_status == 413, (language, 'oversize', oversize_status)
        assert post(port, body) == 204  # receiver remains alive after invalid requests.
        count += 18
    with receiver(language, cmd, '0') as port:
        assert post(port, body) == 503
        count += 1
    print(f'PASS {language}: {count} contract checks', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--languages', nargs='+', choices=['node', 'python', 'go', 'java', 'csharp', 'php'], default=['node', 'python', 'go', 'java', 'csharp', 'php'])
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', 0), MockAPI)
    ENV['BOLT_API_BASE'] = f'http://127.0.0.1:{server.server_port}'
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory(prefix='boltutil-contract-') as build:
            for language in args.languages:
                check(language, commands(language, Path(build)))
    finally:
        server.shutdown(); server.server_close()


if __name__ == '__main__':
    main()
