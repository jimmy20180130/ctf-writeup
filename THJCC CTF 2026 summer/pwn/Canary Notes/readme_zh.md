# Canary Notes

## 題目描述

Welcome to the Canary message board! Here you can leave anything you want to say, and we'll encrypt it using a randomly generated token.

nc chal.thjcc.org 11038

## 解題思路

用 ida 打開

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  _BYTE s[8]; // [rsp+0h] [rbp-10h] BYREF
  __int64 v5; // [rsp+8h] [rbp-8h]

  setbuf(stream: stdin, buf: nullptr);
  setbuf(stream: stdout, buf: nullptr);
  setbuf(stream: stderr, buf: nullptr);
  qword_404090 = sub_4011A6();
  v5 = qword_404090;
  memset(s, c: 0, n: sizeof(s));
  puts(s: "Welcome to Canary Notes");
  puts(s: "leave a note:");
  __isoc99_scanf(a1: "%s", s);
  sub_40125C(a1: v5, a2: s);
  puts(s: "leave another note:");
  __isoc99_scanf(a1: "%s", s);
  sub_40125C(a1: v5, a2: s);
  if ( v5 != qword_404090 )
  {
    puts(s: "tampered.");
    _exit(status: 1);
  }
  puts(s: "thanks!");
  return 0;
}
```

`sub_40125C()` 就是 receipt，直接把 canary 跟 buffer 內容 XOR 起來印出來

```c
int __fastcall sub_40125C(__int64 a1, _QWORD *a2)
{
  return printf(format: "receipt: 0x%016lx\n", a1 ^ *a2);
}
```

`sub_4011A6()` 是 canary 產生器，`getrandom` 之後每個 byte 都做 `% 0x5E + 33`

```c
__int64 sub_4011A6()
{
  __int64 v1; // [rsp+8h] [rbp-18h] BYREF
  __int64 *v2; // [rsp+10h] [rbp-10h]
  int i; // [rsp+1Ch] [rbp-4h]

  v2 = &v1;
  if ( getrandom(a1: &v1, a2: 8, a3: 0) != 8 )
  {
    perror(s: "getrandom");
    _exit(status: 1);
  }
  for ( i = 0; i <= 7; ++i )
    *((_BYTE *)v2 + i) = *((_BYTE *)v2 + i) % 0x5Eu + 33;
  return v1;
}
```

`sub_401246()` 是 win func

```c
int sub_401246()
{
  return system(command: "/bin/sh");
}
```

Exploit:

1. 第一次只送 `A`，`s` 被 `memset` 過所以 qword 就是 `0x41`，receipt 印的 `canary ^ 0x41` 再 XOR 回去就是 canary
2. canary 全是可列印字元，可以原封不動用 `scanf("%s")` 寫回去，通過檢查
3. 第二次 `scanf` 溢位，蓋掉 canary、saved rbp、return address，ret 到 win
4. return address 填 `0x401247`（跳過 `push rbp`）修 stack 對齊，不然會 segfault

## Flag

```text
THJCC{y0u_k1ll3d_c4n4ry_y0u_b4d_b4d}
```
