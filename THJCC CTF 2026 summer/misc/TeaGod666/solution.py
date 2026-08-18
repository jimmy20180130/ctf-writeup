import base64

key = b"teashop-666"
enc = base64.b64decode("D0cMHAwKHA8MFGIRBCYcDFlGGxQaFAEWBAEGDh1IFAwUFQEMGgZNXA9GV0UHEg4BDE1KD1lZWhsLBiwcChFyAAAAVklDHQcbFQ8MFHAVBhUcGhZQXlNEQB0GBFMJDBNCQ1hCWkUzHBwOBEgWV1AAABNTDgYCXkIWVBsKFV1KEg==")
plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(enc))

print(plain.decode())
open("decrypted.txt", "wb").write(plain)
