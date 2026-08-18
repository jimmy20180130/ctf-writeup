# A Million Messages

## 題目描述

`nc chal.thjcc.org 12003`

## 解題思路

連上去得到 `N E C`

```text
N 99029731cbac77199c74745bb1fbd6895c70ee56530a4eeca2c2cf26d7849f7ef980862c7a1457d28e262c810fbb1d6b9cef72c7b244bffab2377412b36112b7
E 10001
C 162d382d1160b191b53924c4947b6c4814f19f3acd9c3b6a44f97eaa49a73ab90db83412b6ed55b8b674282f4fd7d6c8147f87063c2269d50b065a69e834a0e7
```

`N` 是 512 bit，也就是 `k = 64` bytes，`C` 是 flag 加密後的結果。之後每行收一個 hex ciphertext、回一行結果，連線不會斷

把 `C` 原封不動送回去回 `OK`，隨便輸入東西就會是 `BAD`，代表它解完之後在檢查明文開頭是不是 `00 02`，也就是一個 PKCS#1 v1.5 的 padding oracle，配上題目名稱就是 Bleichenbacher 的 million message attack

腳本我是直接用 https://github.com/emilyfane/rsa-bleichenbacher 的 `attack.py`，它把整套 step 2a / 2b / 2c 跟區間收斂都寫好了

Exploit:

1. 收 banner 取 `N` `E` `C`
2. 把 pwntools 的連線包成上面那三個方法
3. 呼叫 `Bleichenbacher(c, RemoteOracle())`，區間收斂成單點後 `PKCS1_decode` 剝掉 PKCS#1 v1.5 的外殼就是 flag

## Flag

```text
THJCC{bl31chenb4ch3r_st1ll_3ats_pkcs1_v1_5}
```
