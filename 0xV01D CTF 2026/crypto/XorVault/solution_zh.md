# XorVault

## 題目描述

Something is locked away. It was locked more than once, by more than one hand. Find what was left behind.

Flag format: 0xV01D{...}

hint : Focus on the order of operations applied to each byte, especially anything using i % 8 or d[i] ^= i.

## 解題思路

這題從標題可以看到是在做 XOR，從敘述可以推斷他 XOR 很多次，從提示可以看到 `i % 8` 和 `d[i] ^= i`  

- `i % 8` 代表使用長度為 8 的 key，每 8 個 byte 循環  
- `d[i] ^= i` 則代表每個 byte 會跟自己的 index 做 XOR  

我們已知 flag 格式是 0xV01D{...}，所以可以用已知明文去推測加密流程，我是先假設 `cipher[i] = plain[i] XOR key[i % 8] XOR i`，算出來 key 是 `47 d6 11 ce ee 91 75`  

常見的 byte 操作除了 XOR 之外常見還有 rotate、add/sub 之類的，我先測試 rotate 後，會得到 `de ad be ef ca fe ba`，再用最後一個 } 帶進去可以得到 `de ad be ef ca fe ba be`

之後就可以依照流程得出 flag 了

```text
cipher byte
-> XOR i
-> rotate right 3 bits
-> XOR key[i % 8]
-> plain byte
```

## Flag

```text
0xV01D{X0R_V4ULT_0P3N3D}
```
