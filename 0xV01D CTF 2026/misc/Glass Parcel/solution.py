with open('polyglot/payload.bin', 'rb') as f:
    payload = f.read()

# xor with 0x42
payload = bytes([b ^ 0x42 for b in payload])
# to text
payload = payload.decode('utf-8')
print(payload)