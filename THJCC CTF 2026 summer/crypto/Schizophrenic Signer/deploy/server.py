import os
import random
import hashlib

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
q = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
G_x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
G_y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

def add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 != y2: return None
    if x1 == x2:
        l = (3 * x1 * x1) * pow(2 * y1, -1, p) % p
    else:
        l = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (l * l - x1 - x2) % p
    y3 = (l * (x1 - x3) - y1) % p
    return (x3, y3)

def mul(pt, n):
    res = None
    curr = pt
    n = n % q
    while n:
        if n & 1: res = add(res, curr)
        curr = add(curr, curr)
        n >>= 1
    return res

G = (G_x, G_y)

def gen_keypair():
    d = random.randint(1, q - 1)
    return d, mul(G, d)

class DualGenerator:
    def __init__(self, seed):
        self.state = seed
        self.a = random.randint(2**252, 2**253 - 1)
        self.b = random.randint(1, p - 1)

    def next_nonce(self):
        self.state = (self.a * self.state + self.b) % p
        return self.state % q

def main():
    d, pub = gen_keypair()
    print("Welcome to the Schizophrenic Signer!")
    print(f"Public Key: ({hex(pub[0])}, {hex(pub[1])})")

    seed = random.randint(1, p - 1)
    gen = DualGenerator(seed)

    print(f"Generator params: a = {hex(gen.a)}, b = {hex(gen.b)}")

    signatures = []
    for i in range(85):
        msg = f"Message {i}".encode()
        h = int(hashlib.sha256(msg).hexdigest(), 16)

        k = gen.next_nonce()
        R = mul(G, k)
        r = R[0] % q
        s = (h + d * r) * pow(k, -1, q) % q

        signatures.append((h, r, s))

    print("Here are your signatures:")
    for h, r, s in signatures:
        print(f"h = {hex(h)}\nr = {hex(r)}\ns = {hex(s)}")

    flag = os.environ.get("FLAG")

    print("Can you find the private key?")
    try:
        ans = int(input("Private Key (d) in hex: "), 16)
        if ans == d:
            print(f"Incredible! Here is your flag: {flag}")
        else:
            print("Wrong.")
    except:
        print("Invalid input.")

if __name__ == "__main__":
    main()
