# Remedy

## Description

Just a random pic?

## Solution Walkthrough

Using exiftool, you can see this string: `6d14166842b6ecb67622284a65bde8a87e03344564bde3ab7e1e324b648dc4a87e0a2f4976bdffbd7e0233435ea6cbb45c`

First, take the first eight bytes and XOR them with `LYKNCTF{` to obtain the key. Then, XOR the entire string with `214d5d2601e2aacd` to get the flag.

## Flag

```text
LYKNCTF{Would_Be_Nice_If_Someone_Grow_Up_One_Day}
```
