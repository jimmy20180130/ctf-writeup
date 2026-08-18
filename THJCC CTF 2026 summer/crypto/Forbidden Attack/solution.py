from pwn import remote

from forbidden_attack import forge_tag, recover_possible_auth_keys

io = remote("chal.thjcc.org", 12002)
msgs = []
for _ in range(3):
    f = io.recvline_startswith(b"MSG").split()
    msgs.append(tuple(bytes.fromhex(x.decode()) for x in f[1:4]))
target = bytes.fromhex(io.recvline_startswith(b"TARGET").split()[1].decode())

ks = max((bytes(a ^ b for a, b in zip(pt, ct)) for pt, ct, _ in msgs), key=len)
target_ct = bytes(a ^ b for a, b in zip(target, ks))

(c1, t1), (c2, t2), (c3, t3) = [(c, t) for _, c, t in msgs]
h = next(h for h in recover_possible_auth_keys(b"", c1, t1, b"", c2, t2)
         if forge_tag(h, b"", c1, t1, b"", c3) == t3)
tag = forge_tag(h, b"", c1, t1, b"", target_ct)

io.sendline(f"{target_ct.hex()} {tag.hex()}".encode())
print(io.recvall(timeout=5).decode().strip())
