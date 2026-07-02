# try

## Description

c'mon, at least try to solve it yourself? it's the easiest rev already lmao

## Solution Walkthrough

First, look at `main`. The primary logic is in `sub_402962()`:

```c
sub_40276F(Buffer);
v4 = sub_4024D9();
v3 = sub_402618(Buffer, v4);
```

`sub_4024D9()` is an anti-debug routine that returns different keys based on the check results. Therefore, I will play by the rules and avoid using a debugger, performing static analysis instead:

```text
IsDebuggerPresent              -> 19  / 0x13
`sub_401F57()` aka 
`CheckRemoteDebuggerPresent`   -> 41  / 0x29
timing check                   -> 78  / 0x4e
normal                         -> 167 / 0xa7
```

Next, look at `sub_402618(Buffer, v4)`:

```c
v9 = strlen(a1);
memcpy(v10, a1, min(v9, 22));

v6 = sub_401FB8(v10, a2);
v8 = sub_401C53(v10);
v7 = sub_401D6F(a2);

return v6 && v9 == 22 && v8 == v7;
```

We can see that the flag length must be exactly `22`. The first 22 bytes are passed into `sub_401FB8` for inspection, and there is a hash check at the end.

`sub_401FB8` is essentially a VM that continuously calls `sub_401A3F` to read bytecode:

```c
bool __fastcall sub_401FB8(__int64 a1, unsigned __int8 a2)
{
  unsigned __int8 v3; // [rsp+33h] [rbp-1Dh] BYREF
  unsigned __int8 v4; // [rsp+34h] [rbp-1Ch]
  unsigned __int8 v5; // [rsp+35h] [rbp-1Bh] BYREF
  unsigned __int8 v6; // [rsp+36h] [rbp-1Ah] BYREF
  unsigned __int8 v7; // [rsp+37h] [rbp-19h] BYREF
  unsigned __int8 v8; // [rsp+38h] [rbp-18h] BYREF
  unsigned __int8 v9; // [rsp+39h] [rbp-17h] BYREF
  unsigned __int8 v10; // [rsp+3Ah] [rbp-16h] BYREF
  char v11; // [rsp+3Bh] [rbp-15h] BYREF
  char v12; // [rsp+3Ch] [rbp-14h] BYREF
  unsigned __int8 v13; // [rsp+3Dh] [rbp-13h] BYREF
  char v14; // [rsp+3Eh] [rbp-12h] BYREF
  unsigned __int8 v15; // [rsp+3Fh] [rbp-11h] BYREF
  int v16; // [rsp+40h] [rbp-10h]
  unsigned __int8 v17; // [rsp+45h] [rbp-Bh]
  unsigned __int8 v18; // [rsp+46h] [rbp-Ah]
  unsigned __int8 v19; // [rsp+47h] [rbp-9h]
  __int64 v20; // [rsp+48h] [rbp-8h] BYREF

  v20 = 0;
  v19 = 0;
  v18 = 0;
  v17 = 0;
  v16 = 0;
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        if ( !(unsigned int)sub_401A3F(&v20, a2, &v15) )
          return 0;
        if ( v15 > 0x71u )
          break;
        if ( v15 >= 0x71u )
        {
          if ( !(unsigned int)sub_401A3F(&v20, a2, &v11) )
            return 0;
          v19 ^= v11;
        }
        else
        {
          switch ( v15 )
          {
            case 0x18u:
              if ( !(unsigned int)sub_401A3F(&v20, a2, &v10) )
                return 0;
              v19 = sub_401891(v19, v10);
              break;
            case 0x32u:
              if ( !(unsigned int)sub_401A3F(&v20, a2, &v12) )
                return 0;
              v19 += v12;
              break;
            case 0x4Bu:
              if ( !(unsigned int)sub_401A3F(&v20, a2, &v13) )
                return 0;
              if ( v13 >= 0x16u )
              {
                v16 |= 0x100u;
                v13 %= 0x16u;
              }
              v19 = *(_BYTE *)(v13 + a1);
              break;
            case 0x5Du:
              if ( !(unsigned int)sub_401A3F(&v20, a2, &v14) )
                return 0;
              v18 = sub_401891((unsigned __int8)(v14 + v18), (v18 + (_BYTE)v20) & 7);
              v18 = sub_401DF8(v18);
              break;
            default:
              return 0;
          }
        }
      }
      if ( v15 != 169 )
        break;
      if ( !(unsigned int)sub_401A3F(&v20, a2, &v8)
        || !(unsigned int)sub_401A3F(&v20, a2, &v7)
        || !(unsigned int)sub_401A3F(&v20, a2, &v6)
        || !(unsigned int)sub_401A3F(&v20, a2, &v5) )
      {
        return 0;
      }
      if ( v8 >= 0x16u || v7 >= 0x16u )
      {
        v16 |= 0x200u;
        v8 %= 0x16u;
        v7 %= 0x16u;
      }
      v4 = sub_401B75(*(unsigned __int8 *)(v8 + a1), *(unsigned __int8 *)(v7 + a1), v8, v7, v6);
      v16 |= v5 ^ v4;
      ++v17;
    }
    if ( v15 != 212 )
      break;
    if ( !(unsigned int)sub_401A3F(&v20, a2, &v9) )
      return 0;
    v16 |= v9 ^ v19;
    ++v17;
  }
  if ( v15 != 238 )
    return 0;
  return (unsigned int)sub_401A3F(&v20, a2, &v3) && (v3 ^ v17 | v16) == 0;
}
```

```c
__int64 __fastcall sub_401A3F(_QWORD *a1, unsigned __int8 a2, _BYTE *a3)
{
  if ( *a1 >= 0x16D )
    return 0;

  v7 = *(_DWORD *)a1;
  v6 = byte_4043A8[(*a1)++];

  v5 = sub_40199F(v7, a2);
  *a3 = sub_4018ED((unsigned __int8)(v5 ^ v6), (a2 ^ (unsigned __int8)v7) & 7);
  return 1;
}
```

`byte_4043A8` is the encrypted bytecode with a length of `0x16d`. The decryption logic is simplified as follows:

```python
plain[i] = ror8(byte_4043A8[i] ^ sub_40199F(i, key), (key ^ i) & 7)
```

The VM also has a function `sub_401B75`, which is a pair constraint used by the `0xa9` opcode. It mixes two input bytes, two indices, and a seed to calculate a 1-byte result, which is then compared against the expected value in the bytecode:

```c
__int64 __fastcall sub_401B75(char a1, char a2, char a3, unsigned __int8 a4, int a5)
{
  char v6; // [rsp+2Fh] [rbp-1h]

  v6 = sub_401891((unsigned __int8)(((a4 + a5) ^ a2) + ((a3 + a5) ^ a1)), (a4 ^ (unsigned __int8)(a3 ^ a5)) & 7);
  return (unsigned __int8)(sub_401891(
                             (unsigned __int8)(((a5 >> 3) & 6 | 1) * a2 + (a5 & 6 | 1) * a1),
                             ((_BYTE)a5 + a4 + a3) & 7)
                         ^ v6);
}
```

The `sub_401891` function inside is actually `rol8`:

```c
__int64 __fastcall sub_401891(int a1, char a2)
{
  __int64 result; // rax

  if ( (a2 & 7) != 0 )
    LOBYTE(result) = (a1 >> (8 - (a2 & 7))) | (a1 << (a2 & 7));
  else
    LOBYTE(result) = a1;
  return (unsigned __int8)result;
}
```

After decrypting with `key = 0xa7`, the beginning of the bytecode looks like this:

```text
5d dc 4b 12 71 45 32 50 18 06 71 93 d4 8e ...
```

The VM opcodes are roughly as follows:

```text
0x4b idx             acc = input[idx]
0x71 imm             acc ^= imm
0x32 imm             acc += imm
0x18 imm             acc = rol8(acc, imm)
0xd4 imm             assert acc == imm
0xa9 i j seed exp    pair constraint
0xee cnt             end
```

Taking the first segment as an example:

```text
5d dc
4b 12
71 45
32 50
18 06
71 93
d4 8e
```

It is equivalent to:

```c
x = input[18];
x ^= 0x45;
x += 0x50;
x = rol8(x, 6);
x ^= 0x93;
assert(x == 0x8e);
```

By reversing it, we can obtain:

```text
input[18] = 'a'
```

Therefore, as long as all `0xd4` constraints are solved, the flag can be recovered. The subsequent `0xa9` opcodes are additional checks between two characters used to verify the results.

## Flag

```text
v1t{n0_dump_just_pain}
```
