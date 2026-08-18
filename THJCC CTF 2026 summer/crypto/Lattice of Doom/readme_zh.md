# Lattice of Doom

## 題目描述

(none)

## 解題思路

`signer_excerpt.py`：

```python
NONCE_BYTES = 29


def make_nonce(trng):
    return int.from_bytes(trng.read(NONCE_BYTES), "big")


def sign(d, msg, trng):
    k = make_nonce(trng)
    r = (k * G).x() % N
    s = pow(k, -1, N) * (sha256_int(msg) + r * d) % N
    return r, s
```

nonce 只有 232 bits，比 secp256k1 的 256-bit group order 少 24 bits，每筆簽章的 `k` 高 24 bits 都是 0，直接套 [bitlogik/lattice-attack](https://github.com/bitlogik/lattice-attack)

Exploit:

1. 把 `output.json` 的簽章轉成該工具的格式，每筆 `{"r": r, "s": s, "hash": sha256(msg), "kp": 0}`，配上 `curve: SECP256K1`、`known_type: MSB`、`known_bits: 24`、`public_key: [Qx, Qy]`
2. 呼叫 `recover_private_key(sigs, None, Q, "SECP256K1", "MSB", 24, True)` 拿到私鑰 `d`
3. `key = sha256(b"wallet-v1|" + d)[:16]`，AES-128-CBC 解 `flag_enc` 即為 flag

## Flag

```text
THJCC{l4tt1c3s_turn_b14s3d_n0nc3s_1nt0_pr1v4t3_k3ys}
```
