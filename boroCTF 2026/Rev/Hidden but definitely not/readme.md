# Hidden but definitely not

## Description

The most trite challenge concept.

## Solution Walkthrough

Open it with IDA and you can see that the password is `Rate5StarsBecauseGreatChallenge`. After entering it, you will get the flag.

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  int i; // [rsp+Ch] [rbp-1A4h]
  char v5[128]; // [rsp+10h] [rbp-1A0h] BYREF
  char s2[12]; // [rsp+90h] [rbp-120h] BYREF
  int v7; // [rsp+9Ch] [rbp-114h]
  __int64 v8; // [rsp+A0h] [rbp-110h]
  __int64 v9; // [rsp+A8h] [rbp-108h]
  __int64 v10; // [rsp+B0h] [rbp-100h]
  __int64 v11; // [rsp+B8h] [rbp-F8h]
  __int64 v12; // [rsp+C0h] [rbp-F0h]
  __int64 v13; // [rsp+C8h] [rbp-E8h]
  __int64 v14; // [rsp+D0h] [rbp-E0h]
  __int64 v15; // [rsp+D8h] [rbp-D8h]
  __int64 v16; // [rsp+E0h] [rbp-D0h]
  __int64 v17; // [rsp+E8h] [rbp-C8h]
  __int64 v18; // [rsp+F0h] [rbp-C0h]
  __int64 v19; // [rsp+F8h] [rbp-B8h]
  __int64 v20; // [rsp+100h] [rbp-B0h]
  __int64 v21; // [rsp+108h] [rbp-A8h]
  char s[136]; // [rsp+110h] [rbp-A0h] BYREF
  unsigned __int64 v23; // [rsp+198h] [rbp-18h]

  v23 = __readfsqword(0x28u);
  qmemcpy(v5, "ehuhDSA|NXO?XJG0ni`XTsU6i`2XdOfktz", 34);
  strcpy(s2, "Rate5Stars");
  s2[11] = 0;
  v7 = 0;
  v8 = 0;
  v9 = 0;
  v10 = 0;
  v11 = 0;
  v12 = 0;
  v13 = 0;
  v14 = 0;
  v15 = 0;
  v16 = 0;
  v17 = 0;
  v18 = 0;
  v19 = 0;
  v20 = 0;
  v21 = 0;
  printf("Give me the password (youll never find it it's just tooooo hard)\n> ");
  fgets(s, 128, stdin);
  s[strcspn(s, "\n")] = 0;
  strcpy(&s2[strlen(s2)], "BecauseGreatChallenge");
  if ( !strcmp(s, s2) )
  {
    puts("wow you really got me this time. if only i used better obfuscation techniques.");
    for ( i = 0; i < strlen(v5); ++i )
      putchar(v5[i] ^ 7);
    putchar(10);
  }
  else
  {
    puts("My disappointment is immeasurable.");
  }
  return 0;
}
```

## Flag

```text
boroCTF{I_H8_M@7ing_StR1ng5_cHals}
```
