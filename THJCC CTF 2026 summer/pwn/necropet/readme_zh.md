# necropet

## 題目描述

I'm so sorry for your loss...but you still need to register the detail of the deceased pet in the necropet intake ledger. What? Why is there a cook function? Because the admin is Linguini xD

nc chal.thjcc.org 1024

## 解題思路

`main` 每讀一行就用空白 `strsep` 切出第一段，跟 `commands` 裡 9 個名字逐一 `strcmp`，match 就 `call [entry + 0x10]`，行內剩下那段字串當唯一參數傳進去

```c
      v5 = 0;
      while ( strcmp(s1: v4, s2: &commands[24 * v5]) != 0 )
      {
        if ( ++v5 == 9 )
        {
          puts(s: "unknown command");
          goto LABEL_2;
        }
      }
      v7 = stringp;
      if ( stringp == nullptr )
        v7 = "";
      (*(void (__fastcall **)(char *))&commands[24 * v5 + 16])(a1: v7);
```

`commands` 在 `0x5020`、一格 24 bytes（`name[16]` + `fn`），而 `.data` 從 `0x5000` 才開始，這張表是可寫的。只要能寫到 `commands`，把某格的 `fn` 換成 `system`，那格指令就等於 `system(input)`

`h_admit` 決定了一隻寵物的 struct

```c
      v12 = v5 + 40;                                       // v5 = note_cap
      v7 = malloc(size: v5 + 40);
      v8 = v7;
      ...
        __memset_chk(a1: v7, a2: 0, a3: v12);
        __snprintf_chk(a1: v8, a2: 24, a3: 2, a4: 24, a5: "stray-%02lu", v3);
        v8[4] = v5;                                        // +0x20 note_cap
        v8[3] = species_book[v4];                          // +0x18 -> .rodata "cat"/"dog"/...
        if ( v6 != 0 )
          read_exact(ptr: v8 + 5, n: v6);                  // +0x28 note
        v9 = &kennels[3 * v3];
        v9[1] = v12;                                       // total = note_cap + 40
        *v9 = v8;                                          // ptr
        *((_DWORD *)v9 + 4) = ++v10;                       // case_id
```

`note_cap` 收 `0x20` 到 `0x4f0`，chunk 大小可以從 `0x50` 開到 `0x510`，跨得過 tcache 的 `0x410` 上限

漏洞在 `h_release`

```c
  free(ptr: *v2);
  *v2 = nullptr;      // kennels[slot].ptr
  v2[1] = nullptr;    // kennels[slot].total
```

它只清 `ptr` 跟 `total`，`case_id` 沒清，`select` 記在 `desk` / `desk_len` 的那份也沒清。而 `show` / `revise` 的有效性檢查只比對 `case_id`

```c
  if ( desk == nullptr
    || (unsigned int)qword_5130 > 0xF                                               // slot
    || LODWORD(kennels[3 * (unsigned int)qword_5130 + 2]) != HIDWORD(qword_5130) )  // case_id
  {
    return puts(s: "nothing selected");
  }
```

所以 `select N` 之後再 `release N`，`desk` 還指著已 free 的 chunk 且檢查照樣過。`show` 從 `desk` hexdump `desk_len` bytes，`revise <len>` 在 `len <= desk_len` 時 `read_exact(desk, len)`，一組 UAF 讀寫

Exploit:

1. `admit` 一隻再 `select`，`show` 印出來的 `+0x18` 是 `species` 指標，`- 0x31ec` 得 PIE
2. `note_cap = 0x4d0` 的 chunk 是 `0x4f8`，`release` 後進 unsorted bin，`show` 讀 `fd`，`- 0x203b20` 得 libc base（Ubuntu 24.04 / glibc 2.39）
3. `release` 一個空 bin 的 `0x50` chunk，safe-linking 存的 `next` 是 `NULL ^ (chunk >> 12)`，`show` 直接讀出 heap key
4. `select 2` → `release 3` → `release 2`，`0x50` tcache 是 head → 2 → 3，`revise 8` 把 chunk 2 的 `next` 改成 `heap ^ (pie + 0x5020)`
5. 兩次 `admit`，第一次拿走 chunk 2，第二次配到 `commands` 上
6. 第二次 `admit(6, 0x20, 0x20, p64(system) + b'aaa\x00'.ljust(16, b'\x00') + p64(system))`，寫出來的內容剛好排成一格 `{ "aaa", system }`

```text
commands+0x00   "stray-06"        <- snprintf 的 name，也就是 entry0 的名字
commands+0x10   0                 <- entry0 的 fn，被 memset 清掉了
commands+0x18   &"cat"            <- species 指標，entry1 的名字變成一串 pointer bytes
commands+0x20   0x20              <- note_cap，還是 entry1 名字的一部分
commands+0x28   system            <- note[0:8]   = entry1 的 fn
commands+0x30   "aaa"             <- note[8:24]  = entry2 的名字
commands+0x40   system            <- note[24:32] = entry2 的 fn
```

後面六格沒被碰到，`main` 的迴圈照常跑，送 `aaa cat /home/necropet/thisisratratratrat_puipui.txt`，`strsep` 切出 `aaa` 對到那格，flag 就出來了

## Flag

```text
THJCC{Tell_me,_Linguini,_about_your_interests...D0_u_1ik3_anima1s?The_u5ua1,_d0gs,_cats,_h0r535,_guinea_pigs...RATS~~}
```
