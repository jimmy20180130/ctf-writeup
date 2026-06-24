import base64, hashlib
import zlib
from Crypto.Cipher import ARC4

A = base64.b64decode(
    "T6ucYf2aZ4VlxcLDROZCxEa7QzrlwjhGYeVmHR/9eDF906DzUJAh0pLR81CT0SOTId6SYZM1Ujx8ZHxktuWOvv5yzh6+Er7Gcp5erk6ecneOxSuXcwFngllVab1ZeVVpPue3VZJtN3bRFM4="
)

B = bytes.fromhex(
    "74fe70772ea8ac1fe4150f1bbb65ec29c5da9438bd670c8bc351695209152d8fc77c415ffc1a3a5f605db8c4"
)

C = base64.b64decode("ycPpCTiLimLndIK7wt3mhLFH0CSDx/Q=")

def xor_bruteforce(data):
    for i in range(256):
        key = bytes([i]) * len(data)
        decrypted = bytes(a ^ b for a, b in zip(data, key))

        try:
            # zlib decompression
            decompressed = zlib.decompress(decrypted)
            return decompressed
        except Exception:
            continue

    return None

# {"mx":"MIND-FLAYER-OTC","proc":"ot_kernel_helper.exe","queue":"macrodata_refiner","wl":"kelp-and-lanterns"}
print(xor_bruteforce(A).decode())

def rc4_decrypt(data, key):
    cipher = ARC4.new(key.encode('utf-8'))
    decrypted = cipher.decrypt(data)
    return decrypted

# OTC_SESSION=otc://macrodata/7f9e3a1dcb8a4f2b
print(rc4_decrypt(B, 'MIND-FLAYER-OTC:kelp-and-lanterns').decode())

# XOR with repeating SHA1(wellness:mutex) bytes
def xor_with_sha1(data, key):
    sha1_hash = hashlib.sha1(key.encode('utf-8')).digest()
    stream = sha1_hash * ((len(data) // len(sha1_hash)) + 1)
    decrypted = bytes(a ^ b for a, b in zip(data, stream))
    return decrypted

print(xor_with_sha1(C, 'kelp-and-lanterns:MIND-FLAYER-OTC').decode())
