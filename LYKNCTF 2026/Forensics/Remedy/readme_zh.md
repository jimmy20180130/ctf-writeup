# Remedy

## 題目描述

Just a random pic?

## 解題思路

用 exiftool 可以看到這串 `6d14166842b6ecb67622284a65bde8a87e03344564bde3ab7e1e324b648dc4a87e0a2f4976bdffbd7e0233435ea6cbb45c`

先取前面八個 byte 跟 `LYKNCTF{` 做 XOR 得到 key 以後再將整串對 `214d5d2601e2aacd` xor，即可得到 flag

## Flag

```text
LYKNCTF{Would_Be_Nice_If_Someone_Grow_Up_One_Day}
```
