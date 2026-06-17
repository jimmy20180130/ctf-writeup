# 64 is life

## Description

Truth, broken into sixty-four.

## Solution Walkthrough

It can be observed that the filenames in `64/ctf_chunks`, when base64 decoded, correspond to the numbers 1 through 64.

Extract their contents and arrange them in order, then remove the 40 within them to obtain a base64 encoded flag.

## Flag

```text
boroCTF{s1xty_f0ur_b3auty}
```
