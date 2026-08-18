# Schizophrenic Signer

## 題目描述

讓隨機數在兩個不同的世界中反覆跳躍，難道不是最安全的做法嗎？ nc chal.thjcc.org 11451

## 解題思路

題目附了 `server.py`，nonce 是這樣生的

```python
class DualGenerator:
    def __init__(self, seed):
        self.state = seed
        self.a = random.randint(2**252, 2**253 - 1)
        self.b = random.randint(1, p - 1)

    def next_nonce(self):
        self.state = (self.a * self.state + self.b) % p
        return self.state % q
```

`a`、`b` 是公開的，只有 seed 未知

但 secp256k1 的 `p - q` 只有 129 bits，跟 256-bit 的 `p` 比起來小到不行。這代表 `state` 落在 `[q, p)` 的機率大約是 `2^-127`，85 個樣本裡幾乎必定全部滿足 `state < q`，也就是 `k_i = state_i`，LCG 的遞迴可以直接寫在 nonce 上

先把簽章轉成 nonce 的線性式，ECDSA 的 `s = (h + d*r) / k mod q` 反解

```text
u_i = r_i * s_i^-1 mod q
v_i = h_i * s_i^-1 mod q
k_i = u_i*d + v_i mod q
```

接著把 LCG 一步遞迴攤成整數等式，`m_i` 是取模丟掉的商

```text
a*k_i + b = m_i*p + k_{i+1}
```

`0 <= k_i < q < p` 且 `a < 2^253`，所以 `0 <= m_i < a`。把這條式子模 `q` 化簡 (`p ≡ p - q mod q`，`p - q` 可逆) 就得到

```text
m_i = c_i*d + e_i mod q
```

其中 `c_i`、`e_i` 只由公開的 `a`、`b`、`u`、`v` 組成。到這裡問題就從找 256-bit 的 `d`變成找一個小於 `a` 的 `m_i`

反過來用：`d = c_i^-1 * (m_i - e_i) mod q`，代回 `k_i = u_i*d + v_i` 得到 `k_i = (A*m_i + B) mod q`。乘上 `a` 會把模數一起放大成 `a*q`，代進原本的整數等式，`a*k_i + b - m_i*p` 就是 `k_{i+1}`，而 `k_{i+1}` 必須落在 `[0, q)`

```text
M = a*q,  L = a*A - p,  C = a*B + b
0 <= m_i < a   且   (L*m_i + C) mod M < q
```

這是標準的 CVP：格點 `(m, L*m + M*t)` 要同時把第一座標壓進寬 `a` 的區間、第二座標壓進寬 `q` 的區間。把 `m` 軸乘上 `w = q / a` 拉成同量級之後，兩邊都是 `q` 寬，而格的行列式是 `w*M ≈ q^2`，所以盒子裡期望剛好一個格點 —— 解是唯一的

```text
[ w    L ]
[ 0    M ]
```

二維的格不需要 LLL，Lagrange reduction 就能直接算出最短基底，而且全程整數不會有精度問題。化簡完對盒子中心 `(w*a/2, q/2 - C)` 用 Cramer 解出精確的基底座標再取整，就是 Babai。真正的解不見得是最近的格點，而是盒子裡的格點，所以要掃一圈 —— 把盒子的半寬 `(w*a/2, q/2)` 透過反矩陣換算回基底座標，就得到掃描範圍

```text
r1 = (w*a/2 * |e2_y| + q/2 * |e2_x|) / |det| + 1
r2 = (w*a/2 * |e1_y| + q/2 * |e1_x|) / |det| + 1
```

基底約化過所以兩個向量夾角不會太扁，`r1`、`r2` 都只有個位數，掃過的格點通常不到 40 個，其中能同時滿足 `0 <= m < a` 和 `(L*m + C) mod M < q` 的只有一到四個

候選之間怎麼挑不必回到格上。`(L*m + C) mod M < q` 這個條件本身就等價於整數等式 `a*k_0 + b = m*p + k_1`，所以每個候選都已經滿足第一個 transition，要區分它們只能看下一個：把 `d` 代回算出 `k_1`、`k_2`，比對 `(a*k_1 + b) % p == k_2`，錯的候選撞對的機率是 `2^-256`。整條攻擊實際上只用到前三筆簽章，剩下 82 筆是題目多給的

Exploit:

1. 收下 `a`、`b` 和 85 組 `(h, r, s)`
2. 算 `u_i = r_i * s_i^-1 mod q`、`v_i = h_i * s_i^-1 mod q`
3. 取第一組 transition，用 `p - q` 的模逆算出 `c`、`e`，再導出 `A`、`B` 與 `M`、`L`、`C`
4. 對 `[[w, L], [0, M]]` 做 Lagrange reduction，Babai 取整後照 `r1`、`r2` 掃出盒內格點得到 `m_i`，反推 `d = c_i^-1 * (m_i - e_i) mod q`
5. 用第二個 transition `(a*k_1 + b) % p == k_2` 篩掉誤中的候選，剩下的 `d` 送回去換 flag

## Flag

```text
THJCC{w0w_y0u_f0und_th3_h1dd3n_d3lt4_b3tw33n_p_4nd_q!}
```
