# Do you know the way?

## 題目描述

Any symbols to help me find the flag?

## 解題思路

題目給的是一個 ELF 執行檔，一開始先用 `file` 檢查，可以發現它被 UPX pack 過，因此先進行 unpack，完成後，再打開 IDA 進行分析。

先看 `main`，程式會讀入使用者輸入，並檢查長度是否為 `0x2c`，也就是 44 bytes。

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned int v4; // eax
  int v5; // eax
  unsigned __int64 i; // [rsp+8h] [rbp-78h]
  char v7[48]; // [rsp+10h] [rbp-70h] BYREF
  char s[56]; // [rsp+40h] [rbp-40h] BYREF
  unsigned __int64 v9; // [rsp+78h] [rbp-8h]

  v9 = __readfsqword(0x28u);
  puts("Do you know the way? Are there any symbols around to help you?");
  if ( fgets(s, 48, stdin) && strcspn(s, "\n") == 44 )
  {
    v4 = time(0);
    srand(v4);
    v5 = rand();
    for ( i = 0; i <= 0x2B; ++i )
    {
      v7[i] = s[i];
      if ( i == v5 % 44 )
        return 0;
    }
    return f_0(v7);
  }
  else
  {
    puts("Wrong");
    return 0;
  }
}
```

這邊可以觀察到 flag 長度為 44，並且程式會用 `rand() % 44` 隨機選一個 index，當 `i` 等於該 index 時直接 `return 0`，也就是說，正常執行程式時幾乎不會真的跑到 `f_0(v7)`，所以這題要用靜態分析來得到 flag

接著分析 `f_0`，可以看到它只檢查第 0 個字元：

```c
__int64 __fastcall f_0(_BYTE *a1)
{
  if ( (unsigned __int8)rol8(*a1 ^ 0x31u, 1) == 0xAA )
    return f_1(a1);
  puts("Wrong");
  return 0;
}
```

成功後會呼叫 `f_1`，失敗則輸出 `Wrong`。

再看 `f_1`，它只檢查第 1 個字元：

```c
__int64 __fastcall f_1(__int64 a1)
{
  if ( ((unsigned __int8)ror8((unsigned __int8)(*(_BYTE *)(a1 + 1) + 104), 2) ^ 0xB4) == 0xC6 )
    return f_2(a1);
  puts("Wrong");
  return 0;
}
```

因此整個檢查流程其實是 `f_0` 逐漸檢查到 `f_43`，每個函式都只處理一個字元，而且運算都只是簡單的 `add`、`sub`、`xor`、`rol8`、`ror8` 之類的 byte operation。

所以可以不用手動逆完 44 個函式，直接對每個 `f_i` 爆破 printable characters

先用 `objdump` dump assembly，接著寫 script 自動抓 f_0 到 f_43，對每個位置測試 0x20 ~ 0x7e，只要模擬該函式中的簡單運算，最後看 cmp al, dl 是否成立即可

## Flag

```text
dalctf{symb0ls_4r3_4lw4ys_3xtr3m3ly_h3lpfu1}
```
