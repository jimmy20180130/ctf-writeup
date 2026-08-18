# déjà vu

## 題目描述

nc chal.thjcc.org 9004

## 解題思路

用 ida 打開，`main()` 是一個選單，`qword_220A0` 是 8 格 slots、`qword_210A0` 是 512 格 channels

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  ...
  v3 = sub_3020(a1: 0x80000000LL);          // seccomp_init(SCMP_ACT_KILL_PROCESS)
  if ( v3 == 0 )
    sub_2509(a1: "seccomp");
  v6 = v3;
  v7 = &unk_11280;
  do
  {
    if ( (int)sub_3890(a1: v6, a2: 2147418112, a3: *v7, a4: 0, ...) < 0 )   // seccomp_rule_add
      sub_2509(a1: "seccomp");
    ++v7;
  }
  while ( &unk_112AC != (_UNKNOWN *)v7 );
  if ( (int)sub_33C0(a1: v6) < 0 )          // seccomp_load
    sub_2509(a1: "seccomp");
  sub_3100(a1: v6);                         // seccomp_release
  while ( 1 )
  {
    puts(s: "1) compose      2) discard");
    puts(s: "3) subscribe    4) unsubscribe");
    puts(s: "5) replay       6) amend");
    puts(s: "7) list         0) quit");
    __printf_chk(a1: 1, a2: "> ");
    switch ( sub_25BE() )
    {
      case 1LL:                             // compose
        v8 = sub_2610();
        if ( qword_220A0[v8] != 0 )
          sub_2509(a1: "slot busy");
        __printf_chk(a1: 1, a2: "length> ");
        v9 = sub_25BE();
        if ( v9 - 16 > 0x7F0 )
          sub_2509(a1: "bad length");
        v26 = malloc(size: v9);
        v10 = malloc(size: 0x38u);
        v11 = v10;
        if ( v26 == nullptr || v10 == nullptr )
          sub_2509(a1: "out of memory");
        *v10 = 0; v10[1] = 0; v10[2] = 0; v10[3] = 0; v10[6] = 0;
        v10[4] = v26;                       // body
        v10[5] = v9;                        // length
        *((_BYTE *)v10 + 48) = 1;           // refs = 1
        __printf_chk(a1: 1, a2: "subject> ");
        sub_252E(a1: v11, a2: 32);
        __printf_chk(a1: 1, a2: "body> ");
        sub_26BE(a1: v11[4], a2: v11[5]);
        qword_220A0[v8] = v11;
        puts(s: "composed.");
        break;
      case 2LL:                             // discard
        v12 = sub_2610();
        v13 = (void *)qword_220A0[v12];
        if ( v13 == nullptr )
          sub_2509(a1: "empty slot");
        qword_220A0[v12] = 0;
        sub_2739(ptr: v13);
        puts(s: "discarded.");
        break;
      case 3LL:                             // subscribe
        v14 = sub_2610();
        v15 = sub_2666();
        v16 = qword_220A0[v14];
        if ( v16 == 0 )
          sub_2509(a1: "empty slot");
        if ( qword_210A0[v15] != 0 )
          sub_2509(a1: "channel busy");
        qword_210A0[v15] = v16;
        ++*(_BYTE *)(v16 + 48);
        puts(s: "subscribed.");
        break;
      case 5LL:                             // replay
        v19 = qword_210A0[sub_2666()];
        if ( v19 == 0 )
          sub_2509(a1: "channel idle");
        write(fd: 1, buf: *(const void **)(v19 + 32), n: *(_QWORD *)(v19 + 40));
        puts(s: "");
        break;
      case 6LL:                             // amend
        v20 = qword_210A0[sub_2666()];
        if ( v20 == 0 )
          sub_2509(a1: "channel idle");
        __printf_chk(a1: 1, a2: "body> ");
        sub_26BE(a1: *(_QWORD *)(v20 + 32), a2: *(_QWORD *)(v20 + 40));
        puts(s: "amended.");
        break;
      ...
    }
  }
}
```

`sub_2739()` 是 unref，refs 減到 0 才 free

```c
unsigned __int64 __fastcall sub_2739(void *ptr)
{
  char v1; // al

  v1 = *((_BYTE *)ptr + 48) - 1;
  *((_BYTE *)ptr + 48) = v1;
  if ( v1 == 0 )
  {
    free(ptr: *((void **)ptr + 4));
    free(ptr);
  }
  ...
}
```

`sub_2666()` 是 channel 讀取，上限 0x1FF，也就是有 512 格

```c
unsigned __int64 sub_2666()
{
  unsigned __int64 result; // rax

  __printf_chk(a1: 1, a2: "channel> ");
  result = sub_25BE();
  if ( result > 0x1FF )
    sub_2509(a1: "no such channel");
  return result;
}
```

`refs` 是 `uint8_t` 但 channel 有 512 格，訂閱滿 256 次就把 refs 溢位回 1，`discard` 一次物件就被 free 掉，但 256 個 channel 還全部指著它。

Exploit:

1. `compose`（refs = 1）-> `subscribe 0..255`（refs = 1 + 256 = 1）-> `discard`（refs = 0，物件被 free）
2. `replay` / `amend` 走的是 `channels` 不檢查 `slots`，於是拿到 UAF 讀 + 寫
3. `replay` 讀出 tcache 裡 safe-linking 過的 `next`（`encoded = real_next ^ (chunk_addr >> 12)`），free 掉的 body 固定在 `heap + 0x2050`、`next` 指向 `heap + 0x1ac0`，兩個未知數只差一個 heap base，迭代幾次就收斂（`solve_heap()`）
4. `compose` 一個 `length = 0x38` 的 body 從同一個 tcache bin 拿回那塊記憶體，在裡面排出假的 `Message`：`b'X' * 0x20 + p64(addr) + p64(length) + b'\x01' + b'\0' * 7`，`channels[0]` 還指著同一個位址，`replay(0)` / `amend(0)` 就成了任意讀寫
5. `heap + 0x1370` 是 libc 指標，減 `0x21ace0` 得 libc base；`libc + 0x222200` 是 environ，拿到 stack 位址；從 `environ - 0x400` 讀 `0x800` bytes 下來掃 `p64(libc + 0x29d90)`，命中處就是 `main` 的返回位址
6. `amend` 把 ROP chain 寫到那個返回位址，選 `0` 讓 `main` 正常返回，chain 就跑起來

seccomp 的白名單在 `unk_11280`，只有 `read / write / open / openat / close / lseek / fstat / newfstatat / brk / exit / exit_group`，`execve` 被擋掉，所以 chain 自己組 syscall 讀 flag（遠端 flag 在 `/flag`）

## Flag

```text
THJCC{s0_wh1ch_AI_d1d_y0u_us3_t0_s0lv3_th1s???}
```
