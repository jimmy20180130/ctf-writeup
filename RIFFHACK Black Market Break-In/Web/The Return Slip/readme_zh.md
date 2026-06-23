# The Return Slip

## 題目描述

The login desk is happy to send buyers back where they came from. If the return address is trusted too much, something extra may tag along.

## 解題思路

這題是當使用者尚未登入就想進到內部頁面時，系統 (應該) 就會把他帶到登入頁面 (`/auth`)，並加上一個 `next` 參數

這裡的 `next` 是通靈出來的，出題者說訪問 `/support` 頁面就會被導向 `/auth`，但我自己是沒有被導向

這題的漏洞就是你可以把 `next` 後面的 url 改成隨便一個 url，例如 `https://google.com`

改完以後登入完成就會被重新導向到 `https://google.com?handoff=bitflag%7Btru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts%7D`，`handoff` 後面的那串就是 flag

## Flag

```text
bitflag{tru5t3d_r3d1r3cts_c4n_c4rry_s3cr3ts}
```
