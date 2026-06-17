# Cat in the ... Box?

## 題目描述

We love cats over here at boroCTF. We feel like we have a hidden connection to them.

## 解題思路

用 ida 分析分析可以發現在 connect 這個函式裡面是使用 curl 來取得不知道是什麼的資料

```c
FILE *__fastcall connect(const char *a1)
{
  char v1; // bl
  char v2; // bl
  unsigned __int64 i; // [rsp+18h] [rbp-2A8h]
  unsigned __int64 j; // [rsp+18h] [rbp-2A8h]
  char src[128]; // [rsp+20h] [rbp-2A0h] BYREF
  char v7[128]; // [rsp+A0h] [rbp-220h] BYREF
  char v8[128]; // [rsp+120h] [rbp-1A0h] BYREF
  char command[8]; // [rsp+1A0h] [rbp-120h] BYREF
  unsigned __int64 v41; // [rsp+2A8h] [rbp-18h]

  v41 = __readfsqword(40u);
  for ( i = 0; i <= 24; ++i )
  {
    v1 = byte_2010[i];
    v7[i] = a1[i % strlen(a1)] ^ v1;
  }
  v7[25] = 0;
  for ( j = 0; j <= 3; ++j )
  {
    v2 = byte_2029[j];
    v8[j] = a1[j % strlen(a1)] ^ v2;
  }
  v8[4] = 0;
  tmpnam(src);
  strncpy(filename, src, 0x7Fu);
  byte_425F = 0;
  *(_QWORD *)command = 0;
  snprintf(command, 0x100u, "curl -s -o \"%s\" \"%s%s%s\"", filename, v7, a1, v8);
  system(command);
  return fopen(filename, "r");
}
```

所以就寫了個 python 腳本來取得網址，因為我懶得看 main 它是怎麼算 `(&off_4020)[v6]` 的，所以我就乾脆直接 bruteforce，最後得知他會去 `https://files.catbox.moe/ymweyc.txt` 拿 flag

## Flag

```text
boroCTF{lEts_gO_B3y0nd_b1nar1e$}
```
