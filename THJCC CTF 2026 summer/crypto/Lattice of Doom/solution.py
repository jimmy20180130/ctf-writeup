import hashlib
import json
from Crypto.Cipher import AES
import ecdsa_lib
from lattice_attack import recover_private_key

_to_pubkey = ecdsa_lib.privkey_to_pubkey
ecdsa_lib.privkey_to_pubkey = lambda k, curve: _to_pubkey(int(k), curve)

with open("output.json", "r" ,encoding="utf-8") as f:
    data = f.read()

data = json.loads(data)

sigs = [{"r": int(sig["r"], 16),
         "s": int(sig["s"], 16),
         "hash": int.from_bytes(hashlib.sha256(bytes.fromhex(sig["msg"])).digest(), "big"),
         "kp": 0} for sig in data["signatures"]]
Q = [int(data["Qx"], 16), int(data["Qy"], 16)]

d = int(recover_private_key(sigs, None, Q, "SECP256K1", "MSB", 24, True))
print("d =", hex(d))

ct = bytes.fromhex(data["flag_enc"])
key = hashlib.sha256(b"wallet-v1|" + d.to_bytes(32, "big")).digest()[:16]
pt = AES.new(key, AES.MODE_CBC, ct[:16]).decrypt(ct[16:])
print(pt[:pt.index(b"}") + 1].decode())
