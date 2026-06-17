# Not the Flag

## 題目描述

Challenge: So is this not the flag? If its not not, then what else?

```text
9d 90 8d 90 bc ab b9 84 8b 97 ce db a0 96 8c a0 91 cf 8b a0 91 90 8b a0 8b 97 cc a0 99 93 bf 98 82
```

## 解題思路

這是一段 hex bytes，然後把每個 byte 做 xor 0xff (bitwise NOT)，然後再把這些 hex bytes 轉成 ascii 就可以了。

## Flag

```text
boroCTF{th1$_is_n0t_not_th3_fl@g}
```
