# Avatar Studio

## 題目描述

Check if there's anything strange. http://chal.thjcc.org:12021/

## 解題思路

網站本身很單純，填個名字就會拿到一個 `session` cookie，然後可以上傳頭貼，flag 在 `/admin`，而 `/admin` 要 `role == "admin"`。

先掃一下常見路徑，發現 `/.git/HEAD` 有東西，所以直接拿 [git dumper](https://github.com/arthaud/git-dumper)

可以看到 app.py 裡面 JWT 相關的實作

```py
def load_key(kid: str) -> bytes:
    if "\x00" in kid:
        abort(400)
    if kid.startswith("/"):
        abort(400)
    path = os.path.join(KEY_DIR, kid)
    with open(path, "rb") as f:
        return f.read()


def jwt_verify(token: str) -> dict:
    ...
    kid = header.get("kid", "")
    key = load_key(kid)

    seg = h_b64 + "." + p_b64
    expected = hmac.new(key, seg.encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, b64url_decode(s_b64)):
        abort(401)
    return payload

def jwt_sign(payload: dict, kid: str) -> str:
    header = {"alg": "HS256", "typ": "JWT", "kid": kid}
    seg = b64url(json.dumps(header, separators=(",", ":")).encode()) + "." + \
          b64url(json.dumps(payload, separators=(",", ":")).encode())
    key = load_key(kid)
    sig = hmac.new(key, seg.encode(), hashlib.sha256).digest()
    return seg + "." + b64url(sig)
```

他只擋了 null byte 跟開頭的 `/`，`../` 完全沒過濾，所以可以指定一個知道內容的檔案當作 key，這裡選了 `requirements.txt`

```text
b'Flask==3.0.3\ngunicorn==22.0.0\n'
```

所以就 `kid = "../requirements.txt"`，`role=admin` 然後去 `/admin` 就有 flag 了

## Flag

```text
THJCC{local_test_flag_not_the_real_one}
```
