# FirstStep

## 題目描述

Everyone walks through the same door to get here. The question is whether you know how to open it. Welcome.

### 提示

1. Flag format: 0xV01D{...}

## 解題思路

1. 先注意到 flag format 是以 0xV01D 開頭。
2. 可以發現 '0' 和 0x72 做 XOR 之後會得到 0x42。
3. 同樣地，'x' 和 0x3a 做 XOR 也會得到 0x42。
4. 依照這個 XOR 規律推下去，就可以還原出 flag。

## Flag

```text
0xV01D{W3LC0M3_T0_CTF}
```
