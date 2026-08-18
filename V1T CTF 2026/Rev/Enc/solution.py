#!/usr/bin/env python3
from pathlib import Path
from struct import pack
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

SEED_1 = bytes.fromhex(
    "926c3b1ec823f9414596ac39cbedb742"
    "f6b3e9a9411517da358c4f93ff630841"
    "bd3aea9a1010941ab48117ca1faa7c85"
)
SEED_2 = bytes.fromhex(
    "ba6168403341c29303bbe73e9b9c5ee1"
    "636ccc4e63d7e3fcbcc24a96de1569a8"
    "d588ffe4caf4541165281f7aada9eaf6"
    "6ff2b3c527232a1fce8a56fa3ece728a"
    "769b3e816ec195fee556dc18"
)


def aes_cbc_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    enc = cipher.encryptor()
    return enc.update(data) + enc.finalize()


def aes_ecb_decrypt(data: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    dec = cipher.decryptor()
    return dec.update(data) + dec.finalize()


def main() -> None:
    here = Path(__file__).resolve().parent
    encrypted_file = here / "bin" / "flag.enc"
    if not encrypted_file.exists():
        encrypted_file = here / "flag.enc"

    #AES-CBC-PKCS7
    derived = aes_cbc_encrypt(SEED_2, SEED_1[16:], SEED_1[:16])

    aes_key = derived[:32]
    chacha_key = derived[32:64]
    nonce12 = derived[64:76]

    #ChaCha7539Engine
    chacha_nonce = pack("<I", 0) + nonce12
    cipher = Cipher(algorithms.ChaCha20(chacha_key, chacha_nonce), mode=None)
    intermediate = cipher.decryptor().update(encrypted_file.read_bytes())

    padded_png = aes_ecb_decrypt(intermediate, aes_key)
    unpadder = padding.PKCS7(128).unpadder()
    png = unpadder.update(padded_png) + unpadder.finalize()

    out = here / "flag.png"
    out.write_bytes(png)
    print(f"Wrote {out} ({len(png)} bytes)")
    print("PNG magic:", png[:8].hex())


if __name__ == "__main__":
    main()
