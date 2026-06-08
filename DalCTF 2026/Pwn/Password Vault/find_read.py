from pwn import *

elf = ELF("./vault")
print(hex(elf.symbols["read_master_key"]))