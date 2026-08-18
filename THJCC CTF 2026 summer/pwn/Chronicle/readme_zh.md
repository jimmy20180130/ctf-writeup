# Chronicle

## 題目描述

你被要求審查一個 Redis ledger module。服務會將短暫的 ledger annotation排程，並提供封存與還原功能。請取得服務內的 flag。

```text
redis-cli -h chal.thjcc.org -p 6379
```

## 解題思路

題目附了 module 原始碼。module 註冊四個指令，ACL 只開這四個跟唯讀的 Redis 指令，寫入指令、`EVAL`、`CONFIG`、`MODULE`、`DEBUG` 全部被擋

```text
CHRONICLE.NEW <delay_ms> <label> <annotation>   建立一筆排程，回傳 id
CHRONICLE.SHOW <id>                             回傳 id / state / label / ticket / delay / result
CHRONICLE.EXPORT <id>                           匯出成一段 binary archive
CHRONICLE.IMPORT <archive>                      從 archive 還原成一筆新排程
```

flag 在 module 載入時就從 `/tmp/.chronicle-anchor` 讀進一個 static buffer，keyspace 裡沒有

```c
static char recovery_value[RESULT_CAPACITY];

static int load_recovery_value(void) {
    FILE *stream = fopen("/tmp/.chronicle-anchor", "rb");
    ...
}
```

只有 `materialize_anchor` 會把它搬出來，而它搬去的 `task->result` 正好是 `SHOW` 回傳的第 6 個欄位

```c
static void materialize_anchor(RedisModuleCtx *ctx, ChronicleTask *task) {
    if (recovery_value_length != 0) {
        memcpy(task->result, recovery_value, recovery_value_length);
    }
    task->result[recovery_value_length] = '\0';
    task->state = CHRONICLE_COMPLETE;
}

static ChronicleCompletion completion_for_kind(uint32_t kind) {
    if (kind == CHRONICLE_RECOVERY) return materialize_anchor;
    return commit_annotation;
}
```

但 `command_new` 跟 `command_import` 都寫死 `allocate_task(delay_ms, CHRONICLE_NOTE)`，正常流程拿到的一定是 `commit_annotation`。目標是把某個 task 的 `completion` 直接改成 `materialize_anchor`，等 timer 到期再 `SHOW`

`completion` 就在 task struct 裡，`note` 的正後面

```c
struct ChronicleTask {
    uint64_t id;                          //   0
    uint64_t delay_ms;                    //   8
    uint32_t state;                       //  16
    uint32_t kind;                        //  20
    uint32_t note_length;                 //  24
    uint32_t label_length;                //  28
    uint64_t ticket;                      //  32
    char label[LABEL_CAPACITY];           //  40
    unsigned char note[NOTE_CAPACITY];    //  72
    ChronicleCompletion completion;       // 152
    char result[RESULT_CAPACITY];         // 160
    unsigned char workspace[WORKSPACE_CAPACITY];  // 288
    ChronicleTask *next;                  // 480
    RedisModuleTimerID timer_id;          // 488
};
```

`ticket` 是拿 `completion` 跟一個只跟 `id` 有關的 salt 做 xor，而 `SHOW` 把 `id` 跟 `ticket` 兩個都原封不動印出來

```c
static uint64_t ticket_for(const ChronicleTask *task) {
    uint64_t salt = rotate_left(task->id * 0x9e3779b97f4a7c15ULL, 17U);
    return ((uint64_t)(uintptr_t)task->completion) ^ salt;
}
```

一次 `NEW` 加一次 `SHOW` 就能反推 `&commit_annotation`，`.so` 的 ASLR 破功

寫入的洞在 `command_import`

```c
    if ((uint8_t)body_length > NOTE_CAPACITY) {
        return RedisModule_ReplyWithError(ctx, "ERR annotation is too large");
    }
    ...
    task->note_length = (uint32_t)body_length;
    memcpy(task->note, cursor, (size_t)body_length);
```

檢查把 `body_length` 截成 8 bits，`memcpy` 卻用完整的 64 bits。取 `body_length = 256` 時 `(uint8_t)256 == 0`，檢查過關，實際往 80 bytes 的 `note` 搬 256 bytes，剛好蓋掉後面的 `completion`

256 bytes 從 offset 72 寫到 328，落在 `result` / `workspace` 裡面就停了，碰不到 480 的 `next` 跟 488 的 `timer_id`，鏈結串列跟 timer 都完好

archive 沒有簽章，`seal` 只是 FNV-1a-32，自己算得出來，所以整包可以自己造

Exploit:

1. `NEW` 一筆再 `SHOW`，用 `ticket ^ rotl64(id * 0x9e3779b97f4a7c15, 17)` 算出 `&commit_annotation`
2. `delta = materialize_anchor - commit_annotation` 是同一份 `.so` 內的編譯期常數，用題目附的 `Dockerfile` 自己 build 一次即可得知
3. 手工組一包 archive：`'CHRN'` + `01 01 00 00` + `delay_ms`(u32 LE，10..86400000) + label_len + label + uvarint `note_len`（256 編成 `80 02`，且必須等於後面剩下的 byte 數）+ body + FNV-1a-32 seal
4. `IMPORT` 送進去，等 delay 到期，`SHOW` 回傳的第 6 個欄位就是 flag

## Flag

```text
THJCC{D0_y0u_KN0W_7h15_15_@_PWN_ch@ll3nge_WH17CH_m4d3_BY_@1???}
```
