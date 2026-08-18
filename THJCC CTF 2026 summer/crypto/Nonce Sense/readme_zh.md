# Nonce Sense

## 題目描述

`nc chal.thjcc.org 12001`

服務用 secp256k1 ECDSA 簽了兩筆訊息，要你對第三筆 target 訊息生出合法簽章

## 解題思路

連上去可以得到底下四個東西

```text
PUB daf8f8b6256f7a6fe2ec2f4e730c649c84d6e54e423e643a8b53a27494b4d00 524956ae5beff5c789a64492fc8e2d539b44842c8c7ad67d75680cf4796fed30
SIG 7472616e73666572203120636f696e20746f20616c696365 30272655b46adfe66171f0a789ef86aa5c6c57c55cc04001a5b621dd573a139c 8e3b3b7c11db8211ea90529bed37b7af019a041820e40a3627986bcb16b9ff11
SIG 7472616e73666572203220636f696e7320746f20626f62 30272655b46adfe66171f0a789ef86aa5c6c57c55cc04001a5b621dd573a139c 470e2ef2a47174a3735d886b6f69d7a32985435110690f7cbef45b031fe767b2
TARGET 61646d696e3d747275653b616374696f6e3d72656c656173655f666c6167
```

兩筆 `SIG` 的 `r` 完全一樣。`r = (k*G).x mod n`，`r` 相同就代表 `k` 相同也就是 nonce 被重用了

ECDSA 的簽章式是 `s = (z + d*r) / k mod n`，兩筆共用同一個 `k` 和同一把私鑰 `d`

```text
s1*k = z1 + d*r
s2*k = z2 + d*r
```

兩式相減，`d*r` 直接消掉

```text
k = (z1 - z2) / (s1 - s2) mod n
```

`z1` `z2` 是兩筆訊息的 SHA-256 當整數，`n` 是 secp256k1 的 group order。有了 `k` 再回代任一式就拿到私鑰

```text
d = (s1*k - z1) / r mod n
```

拿到 `d` 之後就可以自己簽 target 了

```text
s = (H(target) + d*r) / k mod n
```

## Flag

```text
THJCC{n3v3r_3v3r_r3us3_th3_s4m3_n0nc3}
```
