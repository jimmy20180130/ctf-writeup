# Oracle of Padding

## 題目描述

`nc chal.thjcc.org 12000`

## 解題思路

連進去是一行 hex

```text
TOKEN 46f056ce37590a3f849fd0b2065c405ddf1bcc14a0c64b2b70660c3ff16f0cea01d5fb08802f389574df76e59693d27c577417fef998a667934b6fd7801a3140e11566cd8e6e5e657181488f6b7532bb27d15c4eecad7267177ee454e378159d1a6e86c6deae4fb70690ddb7a0f7d400
```

把原本的 token 原封不動送回去回 `OK`，隨便翻掉一個 byte 就回 `BAD`，連線不會斷，可以一直送，這就是 CBC padding oracle，`OK` 和 `BAD` 洩漏的是解密後 PKCS#7 padding 合不合法

CBC 解密是 `P_i = D(C_i) XOR C_{i-1}`，`D(C_i)` (中間值) 只跟 key 有關，改前一塊不會影響它。所以要解第 `i` 塊，只送 `C_{i-1} || C_i` 兩塊就好，`C_i` 變成最後一塊 (padding 只檢查最後一塊)，`C_{i-1}` 換成自己捏的

先從最後一個 byte 開始，把 `C_{i-1}[15]` 掃過 0..255，伺服器回 `OK` 就代表解出來的最後一個 byte 是 `\x01`，於是

```text
D(C_i)[15] = guess XOR 0x01
```

拿到 `D(C_i)[15]` 之後把 `C_{i-1}[15]` 設成 `D(C_i)[15] XOR 0x02`，再掃 `C_{i-1}[14]` 湊出 `\x02\x02`，依此類推到整塊 16 個 byte，最後

```text
P_i = D(C_i) XOR 原本的 C_{i-1}
```

`pad=1` 那一輪要注意：如果掃到的值剛好等於原本的 `C_{i-1}[15]`，解出來的是原始明文自帶的合法 padding (可能是 `\x02\x02`、`\x03\x03\x03`…) 而不是 `\x01`，會拿到錯的中間值。所以 `pad=1` 有兩個命中時要挑跟原始 byte 不同的那個

另外每個 byte 最多要試 256 次，16 bytes × 6 塊 = 兩萬多次 round trip，一次一來一回太慢。伺服器是一行一個 token、照順序回覆，所以直接把 256 個候選一次 `send` 出去，再用 `recvlines(256)` 一起收回來

```python
def batch_oracle(msgs):
    io.send(b"".join(m.hex().encode() + b"\n" for m in msgs))
    return [line == b"OK" for line in io.recvlines(len(msgs))]
```

Exploit:

1. 連線收 banner，取出 `TOKEN` 後面的 hex，切成 16 bytes 一塊 (第一塊是 IV)
2. 對每一塊 `C_i`，`pad` 從 1 掃到 16，每輪把 256 個 `C_{i-1} || C_i` 候選一次送出，命中的 guess XOR pad 就是 `D(C_i)` 的那個 byte
3. 整塊中間值 XOR 原本的 `C_{i-1}` 得到明文，最後剝掉 PKCS#7

```json
{"user":"guest","admin":false,"note":"THJCC{p4dd1ng_0r4cl3s_l34k_0n3_byt3_p3r_qu3ry}"}
```

## Flag

```text
THJCC{p4dd1ng_0r4cl3s_l34k_0n3_byt3_p3r_qu3ry}
```
