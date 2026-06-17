# 64 is life

## 題目描述

Truth, broken into sixty-four.

## 解題思路

可以發現 `64/ctf_chunks` 裡面的檔名經過 base64 decode 以後為 1 ~ 64 的數字，將他們的內文取出並按照順序排列，接著移除裡面的 40，即為一串 base64 encode 過後的 flag

## Flag

```text
boroCTF{s1xty_f0ur_b3auty}
```
