# Orbital Docking Handshake

## Description

The docking console hides its handshake phrase in a runtime-built buffer behind one more computed alignment value. Use the lightest reversing path and recover both values.

## Solution Walkthrough

After entering this program, you must first input the `Docking phrase` and `Alignment window`. It then checks whether the `Docking phrase` matches its expected result, and subsequently verifies if the `Alignment window` matches the calculated result. If both are correct, it prints the flag.

The flag is encrypted, and you need the program's expected `Docking phrase` and the `Alignment window` calculated from it to decrypt it.

Therefore, I wrote a script to solve for the flag. It is important to note that since `mask_for()` returns an `unsigned __int8` and the second parameter of `print_flag()` is a `char`, you need to AND it with 0xff to keep the lower 8 bits so that the result matches the C implementation.

## Flag

```text
bitctf{{0rb1t4l_d0ck1ng_r0ut1n3}}
```
