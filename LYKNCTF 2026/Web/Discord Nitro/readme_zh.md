# Discord Nitro

## 題目描述

Free Discord Nitro

## 解題思路

先用帳號 `guest`，密碼 `guest` 登入，發現他會有一個 JWT

因為我不知道 secret 也懶得猜，於是把 alg 設為 none，接著發現 server 不會驗證簽章，接著進去 admin panel 以後就是 flag 了

## Flag

```text
LYKNCTF{51c3237f94a1404aa9ce6423e096643f} (dynamic flag)
```
