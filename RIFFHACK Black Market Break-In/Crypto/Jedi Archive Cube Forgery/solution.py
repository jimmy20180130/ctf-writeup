import base64
import json
import hashlib
from sympy import integer_nthroot

e = 3
n = int(
    "78856047350617698975795093954477579942887245429012592579638651585913327845657012243302001035248943416583473391993036239478060203350498173125207518085203968340404374571105398839059667285361321109694407806163861793863586528102684063127445946824062903818975762864325504657775443688264508759901857290992786685697"
)

DI_SHA256 = bytes.fromhex("3031300d060960864801650304020105000420")

def b64u(x):
    return base64.urlsafe_b64encode(x).rstrip(b"=").decode()

def iroot(x, k):
    r, exact = integer_nthroot(x, k)
    return int(r if exact else r + 1)

def forge(payload_obj):
    payload = json.dumps(payload_obj, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).digest()

    prefix = b"\x00\x01\xff\x00" + DI_SHA256 + digest
    block = prefix + b"\x00" * (128 - len(prefix))

    s = iroot(int.from_bytes(block, "big"), 3)
    sig = s.to_bytes(128, "big")

    forged = pow(int.from_bytes(sig, "big"), 3, n).to_bytes(128, "big")

    print("payload:", payload)
    print("decrypted signature starts:", forged[:80].hex())
    print("wanted prefix:", prefix.hex())
    print("prefix match length:", sum(a == b for a, b in zip(forged, prefix)))

    return b64u(payload) + "." + b64u(sig)

target = {
    "callsign": "123",
    "clearance": "transit",
    "dock": "annulus-gate",
    "manifest": "civilian",
    "role": "admiral",
    "sector": "outer-rim",
}

print(forge(target))