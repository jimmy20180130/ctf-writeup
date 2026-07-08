# Migrant

## 題目描述

The company currently changed their brand identity, and all staff must migrate their accounts to this new website. But... something is off with the transfer function.

## 解題思路

這題應該要是 crypto 🥀

進去以後拿到一個 v1 migration token `u4TlwTsu32US4uDJlfeEx/SvQVYKyyv4/FxepRUjSuIjH+8h6MDy9GuvXj+WOdR/o4bDgoQLPGvNKiROynO5ig==`，拿去 migrate 會返回是否成功，並且 role 是 user

```json
{
  "message": "Migration successful.",
  "profile": { "role": "user", "user": "guest", "v": "1.0" }
}
```

token base64 decode 出來剛好 48 bytes = 3 個 16-byte block，沒有 MAC 又完全由 client 控制，可以推斷他是 AES-CBC 密文（第一個 block 是 IV），於是想到 padding oracle

一般 padding oracle 是拿來解密別人的密文，但這題目標是把自己變成 admin，所以真正好用的是它的反向操作 —— **padding oracle encryption**：用 oracle 生出一段能解成「任意我們指定明文」的合法密文，逐 block 從尾往前倒推

1. 對每個明文 block，固定後面那個密文 block `C_next`，用 padding oracle 一 byte 一 byte 還原它 AES 解密後的中間值 `I = Dec(C_next)`（每個位置爆破 256 種，靠有沒有 `invalid padding` 判斷）
2. 令 `C_prev = I XOR plaintext_block`，就保證 `Dec(C_next) XOR C_prev == plaintext_block`，這個 block 會被解成我們要的明文
3. 最後一個 block 的 `C_next` 先設全 0（自己挑一個已知密文 block），一路往前把算出的 `C_prev` 接在前面，串起來就是合法密文

偽造的明文只要有 role 就好，server 不驗 `user` 和 `version`，直接用最短的 `{"role":"admin"}`，剛好 16 bytes pad 到 32，密文只有 3 個 block（含尾端全 0），比塞完整 profile 少 1/4 的 oracle 查詢。送回 `/api/migrate`，server 解密、padding 通過、讀到 `role=admin`，帳號就遷移成 admin 拿 flag

## Flag

```text
LYKNCTF{f740972d47ad47aebaf3a5cafe0853f3} (dynamic flag)
```
