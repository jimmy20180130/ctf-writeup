#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Optional, Tuple

P = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
A = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
B = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
N = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
GX = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
GY = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)

Point = Optional[Tuple[int, int]]

key_text = "D4mn_br0_H0n3y_p07_7yp3_5h1d_V1T"


def sm3(data: bytes) -> bytes:
    return hashlib.new("sm3", data).digest()


def inv_mod(x: int, mod: int = P) -> int:
    return pow(x % mod, -1, mod)


def curve(point: Point) -> bool:
    if point is None:
        return False

    x, y = point

    return (
        0 <= x < P
        and 0 <= y < P
        and (y * y - (x * x * x + A * x + B)) % P == 0
    )


def point_add(p1: Point, p2: Point) -> Point:
    if p1 is None:
        return p2

    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and (y1 + y2) % P == 0:
        return None

    if p1 == p2:
        lam = (3 * x1 * x1 + A) * inv_mod(2 * y1) % P
    else:
        lam = (y2 - y1) * inv_mod(x2 - x1) % P

    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P

    return x3, y3


def scalar_mul(k: int, point: Point) -> Point:
    result: Point = None
    current = point

    while k:
        if k & 1:
            result = point_add(result, current)

        current = point_add(current, current)
        k >>= 1

    return result


def kdf_sm3(z: bytes, length: int) -> bytes:
    out = bytearray()
    ct = 1

    while len(out) < length:
        out.extend(sm3(z + ct.to_bytes(4, "big")))
        ct += 1

    return bytes(out[:length])


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def readct(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").strip()
    text = re.sub(r"\s+", "", text)
    return bytes.fromhex(text)


def decrypt_sm2(ciphertext: bytes, private_key: int) -> bytes:
    c1 = ciphertext[:64]
    c2 = ciphertext[64:-32]
    c3 = ciphertext[-32:]

    x1 = int.from_bytes(c1[:32], "big")
    y1 = int.from_bytes(c1[32:], "big")
    point_c1 = (x1, y1)

    shared = scalar_mul(private_key, point_c1)

    if shared is None:
        raise ValueError("Invalid shared point")

    x2, y2 = shared

    x2_bytes = x2.to_bytes(32, "big")
    y2_bytes = y2.to_bytes(32, "big")

    mask = kdf_sm3(x2_bytes + y2_bytes, len(c2))
    plaintext = xor_bytes(c2, mask)

    return plaintext


def ascii_hex(data: bytes) -> bool:
    try:
        text = data.decode("ascii").strip()
    except UnicodeDecodeError:
        return False

    return (
        len(text) > 0
        and len(text) % 2 == 0
        and all(ch in "0123456789abcdefABCDEF" for ch in text)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("challenge", type=Path)
    args = parser.parse_args()

    plain_out = Path("cc01_plain.hex")
    image_out = Path("cc01.png")

    key_bytes = key_text.encode("ascii")
    private_key = int.from_bytes(key_bytes, "big")

    ciphertext = readct(args.challenge)
    plaintext = decrypt_sm2(ciphertext, private_key)

    plain_out.write_bytes(plaintext)

    if ascii_hex(plaintext):
        decoded = bytes.fromhex(plaintext.decode("ascii").strip())
        image_out.write_bytes(decoded)
        print(f"{image_out}")


if __name__ == "__main__":
    main()