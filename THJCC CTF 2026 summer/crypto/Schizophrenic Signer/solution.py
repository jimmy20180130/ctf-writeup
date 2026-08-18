import re
from fractions import Fraction
from pwn import remote

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

dot = lambda x, y: x[0] * y[0] + x[1] * y[1]

def gauss(u, v):
    while True:
        if dot(u, u) > dot(v, v):
            u, v = v, u
        n = round(Fraction(dot(u, v), dot(u, u)))
        if n == 0:
            return u, v
        v = [v[0] - n * u[0], v[1] - n * u[1]]

io = remote("chal.thjcc.org", 11451)
data = io.recvuntil(b"Private Key (d) in hex: ").decode()
a = int(re.search(r"a = (0x\w+)", data).group(1), 16)
b = int(re.search(r"b = (0x\w+)", data).group(1), 16)
nums = [int(x, 16) for x in re.findall(r"[hrs] = (0x\w+)", data)]

# k_i = u_i*d + v_i (mod q)
uv = [(r * pow(s, -1, q) % q, h * pow(s, -1, q) % q)
      for h, r, s in zip(nums[::3], nums[1::3], nums[2::3])]
(u0, v0), (u1, v1), (u2, v2) = uv[0], uv[1], uv[2]

# a*k_0 + b = m*p + k_1，模 q 化簡（p ≡ p-q）得 m = c*d + e
inv_delta = pow(p - q, -1, q)
c = inv_delta * (a * u0 - u1) % q
e = inv_delta * (a * v0 + b - v1) % q
inv_c = pow(c, -1, q)

# 反解 d = (m-e)/c 代回 k_0，得 k_0 = (A*m + B) mod q
A = u0 * inv_c % q
B = (v0 - A * e) % q

# a*k_0 + b - m*p = k_1 ∈ [0,q)  →  (L*m + C) mod a*q < q
M, L, C = a * q, a * A - p, a * B + b
w = q // a                       # 把 m 軸拉到跟餘數同量級
e1, e2 = gauss([w, L], [0, M])
det = e1[0] * e2[1] - e1[1] * e2[0]
hx, hy = w * a // 2, q // 2      # 盒子半寬：m 軸寬 a，餘數軸寬 q
cx, cy = hx, hy - C              # 盒子中心
n1 = round(Fraction(cx * e2[1] - cy * e2[0], det))
n2 = round(Fraction(cy * e1[0] - cx * e1[1], det))
r1 = (hx * abs(e2[1]) + hy * abs(e2[0])) // abs(det) + 1
r2 = (hx * abs(e1[1]) + hy * abs(e1[0])) // abs(det) + 1


def candidates():
    for d1 in range(-r1, r1 + 1):
        for d2 in range(-r2, r2 + 1):
            m = ((n1 + d1) * e1[0] + (n2 + d2) * e2[0]) // w
            if 0 <= m < a and (L * m + C) % M < q:
                d = (m - e) * inv_c % q
                if (a * ((u1 * d + v1) % q) + b) % p == (u2 * d + v2) % q:
                    yield d


io.sendline(hex(next(candidates())).encode())
io.interactive()
