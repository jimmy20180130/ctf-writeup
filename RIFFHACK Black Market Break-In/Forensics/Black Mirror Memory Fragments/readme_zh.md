# Black Mirror Memory Fragments

## 題目描述

A corrupted mobile backup is all that remains of a wiped conversation. Sort the real evidence from the noise, reconstruct what actually happened, and recover the hidden key.

## 解題思路

簡單看了一下 `ch_y4.dat` 可以發現有一行 base64 編碼的字串，decode 以後就是後半部份的 flag (`3assembled_4cross_fragments}}`)

前半部份的 flag 則是在 `messages.db` 裡面的 `recovered_messages` 可以看到兩個 base64 編碼的字串 `Yml0Y3Rme3tzbTF0aDNy` 和 `MzNuX3RocjM0ZF9y`，decode 以後就是 `bitctf{{sm1th3r33n_thr34d_r`

## Flag

```text
bitctf{{sm1th3r33n_thr34d_r3assembled_4cross_fragments}}
```
