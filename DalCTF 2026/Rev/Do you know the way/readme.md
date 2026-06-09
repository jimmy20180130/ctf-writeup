# Do you know the way?

## Description

Any symbols to help me find the flag?

## Solution Walkthrough

The challenge gives an ELF executable. First, checking it with `file` reveals that it has been packed with UPX, so we perform an unpack first. Once completed, we open IDA Pro for further analysis.

First, let's look at `main`. The program reads the user's input and checks if the length is `0x2c`, which is 44 bytes.

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

From this, we can observe that the flag length is 44. Additionally, the program uses `rand() % 44` to randomly select an index. When `i` equals this index, it directly executes `return 0`. This means that during normal execution, the program will almost never actually reach `f_0(v7)`. Therefore, we must use static analysis to obtain the flag.

Next, analyzing `f_0` shows that it only checks the 0-th character:

```c
__int64 __fastcall f_0(_BYTE *a1)
{
  if ( (unsigned __int8)rol8(*a1 ^ 0x31u, 1) == 0xAA )
    return f_1(a1);
  puts("Wrong");
  return 0;
}
```

If successful, it calls `f_1`; otherwise, it prints "Wrong".

Looking at `f_1`, it only checks the 1st character:

```c
__int64 __fastcall f_1(__int64 a1)
{
  if ( ((unsigned __int8)ror8((unsigned __int8)(*(_BYTE *)(a1 + 1) + 104), 2) ^ 0xB4) == 0xC6 )
    return f_2(a1);
  puts("Wrong");
  return 0;
}
```

Thus, the entire verification workflow cascades sequentially from `f_0` all the way to `f_43`, with each function processing only a single character. Moreover, the operations are just simple byte manipulations such as `add`, `sub`, `xor`, `rol8`, and `ror8`.

Consequently, instead of manually reversing all 44 functions, we can directly brute-force the printable characters for each `f_i`.

First, use `objdump` to dump the assembly. Then, write a script to automatically extract the assembly from `f_0` to `f_43` and test the range `0x20` to `0x7e` for each index. By simulating the simple operations within each function, we can verify whether the final `cmp al, dl` condition holds true.

## Flag

```text
dalctf{symb0ls_4r3_4lw4ys_3xtr3m3ly_h3lpfu1}
```
