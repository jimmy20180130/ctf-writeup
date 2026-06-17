# Not Your Time

## Description

One of the trifecta of bitwise operations.

## Solution Walkthrough

Opening it with IDA reveals that the program checks each input character, performs a bitwise NOT operation on it, takes the low byte (lobyte), and compares it with the corresponding character in the `v6` array.

So, I wrote a script and obtained the flag.

## Flag

```text
boroCTF{N0t_nO+_tH3_FL@g}
```
