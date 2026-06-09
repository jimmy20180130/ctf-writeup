# Bandaids Help me Heal

## 題目描述

This progam is supposed to print the flag for me but for some reason it's got a security system attached to it

## 解題思路

用 ida 打開他可以看到 main 函式，前面會有一個 while 迴圈，每執行一輪就會等待 1,000,000,000 微秒也就是 1000 秒

這個迴圈乍看之下會無限循環，但是因為 char 是一個 byte，assembly 是對一個 byte 做遞減，因此它會從 0xff 一直減到 0x01，下一次變成 0x00 後跳出迴圈。所以這個迴圈總共跑了 255 次

至於 v4，他在每次迴圈都會跟 v5 做 xor，整體下來他就是把 1~255 全部 xor，所以最後是 0，而 0 跟 0x5A xor 的結果就是 0x5A，所以只要跑夠久就能跑完迴圈得到 flag

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned __int8 v4; // [rsp+Eh] [rbp-2h]
  char v5; // [rsp+Fh] [rbp-1h]

  v5 = -1;
  v4 = 0;
  puts("Initializing secure wait system...");
  while ( v5 )
  {
    v4 ^= v5;
    usleep(1000000000u);
    --v5;
  }
  if ( (v4 ^ 0x5A) != 0x5A )
  {
    puts("Integrity check failed.");
    exit(1);
  }
  puts("Access granted.");
  decrypt_and_print_flag(90, argv);
  return 0;
}
```

至於解密 flag 的邏輯，`v2` 以及 `v2` 後方連續的 stack memory 被當成 encrypted flag buffer 使用。程式先寫入幾段常數，其中 `*(_QWORD *)((char *)v3 + 6)` 會從 `v3` 的 offset 6 開始覆蓋 8 bytes。最後程式對從 `&v2` 開始的 22 bytes 全部 xor `a1`，也就是 xor 0x5A，得到 flag

```c
int __fastcall decrypt_and_print_flag(char a1)
{
  __int64 v2; // [rsp+10h] [rbp-20h] BYREF
  _QWORD v3[2]; // [rsp+18h] [rbp-18h]
  int v4; // [rsp+28h] [rbp-8h]
  int i; // [rsp+2Ch] [rbp-4h]

  v2 = 0x38213C2E39363B3ELL;
  v3[0] = 0x3B2A0523283B3433LL;
  *(_QWORD *)((char *)v3 + 6) = 0x273E3F32392E3B2ALL;
  v4 = 22;
  for ( i = 0; i < v4; ++i )
    *((_BYTE *)&v3[-1] + i) ^= a1;
  return printf("Flag: %s\n", (const char *)&v2);
}
```

由上述可知有兩個解法

### 第一種

按照 `decrypt_and_print_flag` 的邏輯寫一個腳本來解密 flag，可參考 solution.py

### 第二種

也可以把 `usleep()` patch 掉，先在 ida 的 IDA View-A 裡面找到 `call _usleep`

![alt text](image.png)

再切換到 Hex View-1

![alt text](image-1.png)

把這五個 bytes 改成 NOP `90 90 90 90 90`，好了以後執行也能得到 flag (`chall_patched` 是改完的檔案)

```text
┌──(kali㉿kali)-[~/Desktop]
└─$ ./chall_patched          
Initializing secure wait system...
Access granted.
Flag: dalctf{binary_patched}
```

## Flag

```text
dalctf{binary_patched}
```
