# The Great Discount Heist

## 題目描述

Expensive tools shouldn't be free, but some users claim they've found a way. Can you discover their secret?

## 解題思路

這題老梗了，在 `/auth` 頁面往下滑可以看到通往 `/welcome` 的連結，`/welcome` 裡面有一個優惠碼，叫做 `WELCOME20`

接著到 `/listing/macro-builder` 去購買，為什麼是老梗呢，因為我們可以調整優惠碼的大小寫，讓系統以為我們用的是不同的優惠碼，最後將價格變成 0 元，即可得到 flag

![alt text](image.png)

## Flag

```text
bitflag{c0up0n_st4ck1ng_1s_4_d34l}
```
