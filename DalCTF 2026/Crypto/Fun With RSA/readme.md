# Fun With RSA

## Description

Made my own rsa implementation. Hoping its safe enough that no one can crack it. I even xored things to make it safer

## Solution Walkthrough

The challenge provides an RSA implementation. In addition to outputting the standard RSA `n, e`, it also outputs:

```python
s = sq + h*q
spz = sq + hf*q
ct = int(xor(bin(c), bin(p), bin(q)), 2)

```

Looking further into the code, there is a section performing a CRT (Chinese Remainder Theorem) operation:

```python
dp = d % (p-1)
dq = d % (q-1)
qinv = inverse(q, p)

sp = pow(m, dp, p)
sq = pow(m, dq, q)

h = (qinv * (sp - sq)) % p
s = sq + h*q

```

Where:

```text
sp ≡ m^d mod p
sq ≡ m^d mod q

```

The program then uses CRT to combine `sp` and `sq` back into a result modulo `n`. Therefore, we can get:

```text
s ≡ m^d mod n

```

In other words, `s` is actually the RSA signature of the message `m`. Thus, by simply performing an operation on `s` with the public exponent `e`, the plaintext can be restored:

```text
s^e ≡ (m^d)^e ≡ m mod n

```

As a result, there is absolutely no need to factor `n`, nor is there any need to handle the XOR of `ct`.

## Flag

```text
dalctf{s3gf4u17_r54_m1x3d_w17h_x0r}
```
