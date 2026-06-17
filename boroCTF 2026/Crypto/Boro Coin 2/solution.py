import hashlib

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

d = int("1b7ba9dafeb7c7a30fd8043a656c3ab89509db070dbd48b593d8e266b56ca22d",16)
r = int("2cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec7",16)

old_s = int("4b2f38c18c2a933f81112350ae048f0162feaaed599f827180944ea3203570de",16)
old_msg = "Suspect:FranklinGothic:21.68"
new_msg = "Suspect:Boro_Confiscation_Committee:32.35"


def sha256_int(msg: str) -> int:
    return int.from_bytes(hashlib.sha256(msg.encode()).digest(), "big")


def der_int(x: int) -> bytes:
    b = x.to_bytes((x.bit_length() + 7) // 8 or 1, "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return b"\x02" + bytes([len(b)]) + b


def der_sig(r: int, s: int) -> str:
    body = der_int(r) + der_int(s)
    return (b"\x30" + bytes([len(body)]) + body).hex()

old_z = sha256_int(old_msg)

k = ((old_z + r * d) * pow(old_s, -1, N)) % N

new_z = sha256_int(new_msg)

new_s = ((new_z + r * d) * pow(k, -1, N)) % N

if new_s > N // 2:
    new_s = N - new_s

sig = der_sig(r, new_s)

print("message:", new_msg)
print("flag:", f"boroCTF{{{sig}}}")