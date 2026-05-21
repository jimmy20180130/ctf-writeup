# FirstStep

## Description

Everyone walks through the same door to get here. The question is whether you know how to open it. Welcome.

### Hints

1. Flag format: 0xV01D{...}

## Solution Walkthrough

1. First, note that the flag format begins with 0xV01D.
2. We can see that '0' XOR 0x72 gives 0x42.
3. Likewise, 'x' XOR 0x3a also results in 0x42.
4. By applying the same XOR pattern, we can recover the flag.

## Flag

```text
0xV01D{W3LC0M3_T0_CTF}
```
