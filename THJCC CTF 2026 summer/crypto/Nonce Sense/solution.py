from hashlib import sha256
from pwn import remote

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

io = remote("chal.thjcc.org", 12001)
io.recvline()
sig1 = io.recvline().decode().split()
sig2 = io.recvline().decode().split()
target = bytes.fromhex(io.recvline().decode().split()[1])

m1, r, s1 = bytes.fromhex(sig1[1]), int(sig1[2], 16), int(sig1[3], 16)
m2, r2, s2 = bytes.fromhex(sig2[1]), int(sig2[2], 16), int(sig2[3], 16)

H = lambda m: int.from_bytes(sha256(m).digest(), "big")
z1, z2 = H(m1), H(m2)

k = (z1 - z2) * pow(s1 - s2, -1, N) % N
d = (s1 * k - z1) * pow(r, -1, N) % N
s = (H(target) + d * r) * pow(k, -1, N) % N

io.sendline(f"{r:x} {s:x}".encode())
print(io.recvall().decode(), end="")
