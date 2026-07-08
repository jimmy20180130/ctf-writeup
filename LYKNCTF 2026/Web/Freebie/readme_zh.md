# Freebie

## 題目描述

Human error is the weakest link.

## 解題思路

這是一題爛題目，跟 human error 沒半點關係

進去題目是一個登入頁面，不能用 admin 登入也不能創名為 admin 的帳號，然而得到 flag 就必須以 username 是 admin 的帳號登入

嘗試把 username 設定為 `admin ` 或 `admin ` 或 `ad"+"min` 等東西但都沒用，最後就發現應該是 weak secret，然而用 rockyou 怎麼爆破都沒用

最後無聊用了 `?debug=1` 就出現原始碼了，可以看到他包含了一個 secret key `sup3r_s3cr3t_ctf_k3y_727`，用他造一個 username 是 admin 的 cookie 即可得到 flag

## Flag

```text
LYKNCTF{2a16cd4d8964453aa9948ec5b2b92db0} (dynamic flag)
```
