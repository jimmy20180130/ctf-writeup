# Glass Meridian Drift

## 題目描述

A quiet RSA key was generated at noon and corrected by a tiny offset. The correction was smaller than the operator thought.

## 解題思路

我們已知 RSA 中

$$n = p\cdot q$$

由題目可知 $p$ 與 $q$ 之差小於 $2^{25}$，這代表 $p$ 和 $q$ 很接近，於是我就使用 Fermat 因式分解法。

設

$$a=\frac{p+q}{2},\qquad b=\frac{q-p}{2}$$

則有

$$n=a^2-b^2=(a-b)(a+b).$$

要分解 $n$ 的話，要找一個大於 $\sqrt{n}$ 的整數 $a$，並檢查

$$a^2-n=b^2$$

是否為完全平方數。若成立，則可由

$$p=a-b,\qquad q=a+b$$

得到質因數。

因為 $p$ 和 $q$ 很接近，$a$ 會非常接近 $\sqrt{n}$，所以我是把 $\sqrt{n}$ 無條件進位，然後就成功了，得到以下 $p, q$：

$$p = 30781960399176818588848237874504350891261490762280592662378670237356982853595044454492776283649913589684358691506813$$

$$q = 30781960399176818588848237874504350891261490762280592662378670237356982853595044454492776283649913589684358702733033$$

接著拿去解就可以拿到 flag 了。

## Flag

```text
0xV01D{nearby_primes_make_lattices_louder}
```
