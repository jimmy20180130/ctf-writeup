# Fun With RSA

## 題目描述

Made my own rsa implementation. Hoping its safe enough that no one can crack it. I even xored things to make it safer

## 解題思路

題目給了一段 RSA 實作，除了輸出一般 RSA 的 `n, e` 之外，還額外輸出了：

```python
s = sq + h*q
spz = sq + hf*q
ct = int(xor(bin(c), bin(p), bin(q)), 2)
```

繼續看程式碼可以看到一段做 CRT 運算的程式碼

```python
dp = d % (p-1)
dq = d % (q-1)
qinv = inverse(q, p)

sp = pow(m, dp, p)
sq = pow(m, dq, q)

h = (qinv * (sp - sq)) % p
s = sq + h*q
```

其中：

```text
sp ≡ m^d mod p
sq ≡ m^d mod q
```

接著程式利用 CRT 把 sp 和 sq 合併回模 n 的結果，因此可以得到：

```text
s ≡ m^d mod n
```

也就是說，s 其實就是訊息 m 的 RSA signature。因此只要把 `s` 再用公鑰指數 `e` 做一次運算，就能還原明文：

```text
s^e ≡ (m^d)^e ≡ m mod n
```

所以根本不需要分解 `n`，也不需要處理 `ct` 的 XOR

## Flag

```text
dalctf{s3gf4u17_r54_m1x3d_w17h_x0r}
```
