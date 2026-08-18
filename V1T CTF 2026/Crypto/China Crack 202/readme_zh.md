# China Crack 202 Writeup

## 題目描述

I spent lots of token on this

## 解題思路

題目使用 ZUC 產生 keystream，然後把 flag 和 keystream 做 XOR：

```python
cipher_flag = xor(flag, keystream)
```

因此只要能還原出每個 32-bit keystream word，就可以直接解出 flag。

題目另外輸出了幾組 leak：

```python
leak1 = [((words[i] ^ words[i+1]) * 0x9e3779b1 >> 24) & 0xFF for i in range(len(words)-1)]
leak2 = [((words[i] * 0x45d9f3b) ^ (words[i] >> 16)) & 0xFFFF for i in range(len(words))]
leak3 = [bin(words[i]).count("1") for i in range(len(words))]
partial_crc = zlib.crc32(flag[:16])
```

功能分別是：

```text
leak1：相鄰 keystream word 的關係
leak2：單一 keystream word 的 16-bit 洩漏
leak3：每個 keystream word 的 bit count
partial_crc：flag[:16] 的 CRC32
```

觀察上面的leak，可以發現可以從leak2開始著手，因為只取最後 16-bit 的結果，所以有可能可以枚舉。

加上leak1、leak3、partial_crc可以有效篩選可能的flag，加上已知前綴，所以可以從一個已知起點開始，一路把整個flag推完。

以下是每個leak的細節：

### leak2

題目的 leak2 是：

```python
leak2 = ((w * 0x45d9f3b) ^ (w >> 16)) & 0xFFFF
```

因為最後只取低 16 bits，所以：

```text
(w * 0x45d9f3b) & 0xffff
```

只會受到低 16 bits(lo)影響，不會受到高 16 bits(hi)影響。

所以可以改寫成：

```python
leak2 = ((lo * 0x45d9f3b) & 0xffff) ^ hi
```

所以枚舉範圍從2^32直接降到2^16，並且對每個 lo，都可以直接反推出 hi：

```python
hi = leak2 ^ ((lo * 0x45d9f3b) & 0xffff)
word = (hi << 16) | lo
```

### leak1

leak1 給的是相鄰兩個 keystream word 的關係：

```python
leak1[i] = (((words[i] ^ words[i+1]) * 0x9e3779b1) >> 24) & 0xff
```

所以可以從第一個 word 開始，逐層接下一個 word：

```python
if (((prev_word ^ cur_word) * 0x9e3779b1 >> 24) & 0xff) == leak1[i]:
    keep
```

只要不能接在一起，就可以直接捨棄。

### leak3

題目給了：

```python
leak3 = [bin(words[i]).count("1") for i in range(len(words))]
```

所以leak3會把我們猜的keystream word轉成二進位，然後算我們的keystream word有幾個1，然後對比正確的word，如果不等於題目的leak就可以直接捨棄。

### flag prefix

根據flag格式，第一個 4 bytes 的 plaintext 一定是：

```python
b"V1T{"
```

因此第一個 keystream word 可以直接算：

```python
word0 = int.from_bytes(cipher_flag[:4] ^ b"V1T{", "big")
```

這可以讓搜尋從唯一的起點開始。

### partial_crc

題目給了：

```python
partial_crc = zlib.crc32(flag[:16])
```

所以當目前已經還原出 16 bytes plaintext 時，就可以檢查：

```python
zlib.crc32(candidate_plain[:16]) == partial_crc
```

可以檢查是不是錯誤路徑。

## Flag

```text
V1T{7fK9xL2mQp8ZrT5uWc3Yd6Hs0AaBbCcDdEeFf}
```
