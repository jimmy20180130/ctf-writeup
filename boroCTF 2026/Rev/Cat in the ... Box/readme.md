# Cat in the ... Box?

## Description

We love cats over here at boroCTF. We feel like we have a hidden connection to them.

## Solution Walkthrough

Analyzing with IDA, I discovered that the `connect` function uses curl to retrieve unknown data.

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

Therefore, I wrote a Python script to retrieve the URL. Since I was too lazy to figure out how `main` calculates `(&off_4020)[v6]`, I simply used brute force. I eventually found out that it goes to `https://files.catbox.moe/ymweyc.txt` to get the flag.

## Flag

```text
boroCTF{lEts_gO_B3y0nd_b1nar1e$}
```
