import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = bytes.fromhex("9e1b8a5f8ed44e4711c0f4768c13f5a336bc4a6deeea307720a87b9fca44f02d")

ct = base64.b64decode("baCIJCXuBcIOJ23q0FS8GDaSN5/71aIqY156ju5Z6oc=")
iv = base64.b64decode("fcSvIZ1LMw72z34mvr0O5A==")

dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
pt = dec.update(ct) + dec.finalize()

pad = pt[-1]
print(pt[:-pad].decode())