from pwn import *

elf = ELF("./slot_machine")
rop = ROP(elf)

ret = rop.find_gadget(["ret"])[0]
print(hex(ret))