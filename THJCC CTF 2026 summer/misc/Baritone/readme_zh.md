# Baritone

## 題目描述

(none)

## 解題思路

`baritone.mp3` 聽起來就是不同頻率的音，每個音的持續時間差不多，中間沒有雜訊，可以推斷出一個音可能就代表一個字元

聽起來很像 do re mi fa so，所以嘗試把那些東西組合起來，但是失敗了，之後想到把頻率換成 MIDI note number

```python
midi = round(69 + 12 * log2(freq / 440.0))
```

`1046 Hz` -> 84、`526 Hz` -> 72、`588 Hz` -> 74、`390 Hz` -> 67，也就是 `T` `H` `J` `C`，MIDI 編號直接當 ASCII 碼讀就是 flag

## Flag

```text
THJCC{DoYouHavePerfectPitch}
```
