# Riffhack License Forger

## Description

A vendor dropped a trial build of a riffhack payload builder, but the paid features are locked behind a local activation check. 

## Solution Walkthrough

In this challenge, you must first enter the `license`, then the `builder secret`. The program first checks if the `license` is a demo (handled by `sub_18A8`). If it is, it outputs `demo receipt only - no payout` and terminates (see `solution.py` for reference).

If not, there are three functions that check the `license`: `sub_127B`, `sub_135C`, and `sub_1637`. Let's look at `sub_127B` first.

```c
_BOOL8 __fastcall sub_127B(__int64 a1)
{
  if ( strlen((const char *)a1) != 20 )
    return 0;
  if ( *(_BYTE *)a1 != 82 || *(_BYTE *)(a1 + 1) != *(_BYTE *)a1 - 10 || *(_BYTE *)(a1 + 2) != 45 )
    return 0;
  if ( *(_BYTE *)(a1 + 8) != *(_BYTE *)(a1 + 2) || *(_BYTE *)(a1 + 13) != *(_BYTE *)(a1 + 2) )
    return 0;
  return *(_BYTE *)(a1 + 3) == 84 && *(_BYTE *)(a1 + 4) == 82 && *(_BYTE *)(a1 + 7) == 76;
}
```

You can see that it first checks if the length of the `license` is 20 and if it matches the format `RH-TR??L-????-??????`, where the question marks can be any character.

Next, let's look at `sub_135C`.

```c
_BOOL8 __fastcall sub_135C(_BYTE *a1)
{
  int v2; // [rsp+Ch] [rbp-Ch]
  unsigned __int64 i; // [rsp+10h] [rbp-8h]

  if ( (a1[3] ^ a1[7]) != 24 )
    return 0;
  if ( (unsigned __int8)a1[5] + (unsigned __int8)a1[4] + (unsigned __int8)a1[6] != 220 )
    return 0;
  if ( a1[5] != 73 || a1[6] != 65 )
    return 0;
  if ( (char)a1[6] + 19 != (char)a1[3] || (char)a1[4] - 9 != (char)a1[5] )
    return 0;
  v2 = 0;
  for ( i = 9; i <= 0xC; ++i )
  {
    if ( (char)a1[i] <= 47 || (char)a1[i] > 57 )
      return 0;
    v2 = 10 * v2 + (char)a1[i] - 48;
  }
  if ( v2 != 2026 )
    return 0;
  if ( a1[14] != 79 || a1[15] != 80 || a1[16] != 69 || a1[17] != 78 )
    return 0;
  if ( (a1[14] ^ a1[17]) != 1 )
    return 0;
  if ( (unsigned __int8)a1[18]
     + (unsigned __int8)a1[17]
     + (unsigned __int8)a1[16]
     + (unsigned __int8)a1[15]
     + (unsigned __int8)a1[14]
     + (unsigned __int8)a1[19] == 372 )
    return a1[18] == 33 && a1[19] == a1[18];
  return 0;
}
```

From the above, it can be determined that the `license` should be `RH-TRIAL-2026-OPEN!!`. I won't go into more detail here. Finally, there is `sub_1637`.

```c
_BOOL8 __fastcall sub_1637(__int64 a1)
{
  return (unsigned int)sub_15D9(a1) == -949605801;
}

__int64 __fastcall sub_15D9(__int64 a1)
{
  unsigned int v2; // [rsp+Ch] [rbp-Ch]
  unsigned __int64 i; // [rsp+10h] [rbp-8h]

  v2 = 9384357;
  for ( i = 0; i <= 0x13; ++i )
    v2 = __ROL4__(16777619 * ((unsigned __int8)(*(_BYTE *)(a1 + i) + 69 * i) ^ v2), 5);
  return v2;
}
```

This function calculates a hash; if the previous inputs were correct, this step is just a verification.

Once you obtain and enter the `license`, the program will print the `builder secret`. Enter the `builder secret` it outputs, and you will obtain the flag.

```text
riffhack license forger // paid builder unlock
vendor: riffhack-labs
enter activation key to unlock the builder
license> RH-TRIAL-2026-OPEN!!
stage one accepted. builder secret recovered:
FORGE-STAGE-2
builder secret> FORGE-STAGE-2
paid builder receipt unlocked:
bitctf{{r1ff_l1c3n53_m4k3r_unl0ck3d}}
```

## Flag

```text
bitctf{{r1ff_l1c3n53_m4k3r_unl0ck3d}}
```
