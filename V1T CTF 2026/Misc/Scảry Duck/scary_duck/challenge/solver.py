#hack

import base64

KEY = b"DEMOKEY!"


def reverse_layer(func):
    def wrapper(data):
        return func(data)[::-1]
    return wrapper

#exploit

def xor_layer(func):
    def wrapper(data):
        out = func(data)
        return bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(out))
    return wrapper

#bypass


def base64_layer(func):
    def wrapper(data):
        return base64.b64encode(func(data))
    return wrapper

#RCE


@base64_layer
@xor_layer
@reverse_layer
def encode(data: bytes) -> bytes:
    return data

#malware

DEMO_PLAINTEXT = b'hello_duck'
DEMO_CIPHERTEXT = b'LyY4KxQqNU0hLQ=='
assert encode(DEMO_PLAINTEXT) == DEMO_CIPHERTEXT, "environment mismatch"
print("[+] Self-test passed - encode() behaves exactly as described.")

#reverse shell


with open("flag.enc", "rb") as f:
    FLAG_CIPHERTEXT = f.read().strip()

# flag.enc = encode(FLAG) but encode() was called with a DIFFERENT 8-byte KEY

