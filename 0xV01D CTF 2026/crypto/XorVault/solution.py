ct = bytes.fromhex("77af45fddbd008307ff605c6fb50b9581cfd65f5307be109")
key = bytes.fromhex("deadbeefcafebabe")

def ror(x, n):
    return ((x >> n) | ((x << (8 - n)) & 0xff)) & 0xff

pt = bytearray()

for i, c in enumerate(ct):
    x = c ^ i          # reverse d[i] ^= i
    x = ror(x, 3)      # reverse rol 3
    x ^= key[i % 8]    # reverse XOR key
    pt.append(x)

print(pt.decode())