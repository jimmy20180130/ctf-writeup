# Chronos

## 題目描述

Would you rather posess the powers of Chronos, the God of Time or posess the powers of a bilingual?

## 解題思路

用 wireshark 打開 `chronos.pcap`，裡面只有一堆 TCP 封包，而且按 follow 以後並沒有看到任何資料

![alt text](image.png)

有了 `blackwall protocol` 這題的經驗以後，我去看了一下延遲，發現只有 0.25 秒或是 0.75 秒，所以就假設差 0.25 的為 0，差 0.75 的為 1，之後 decode 完就是 flag 了

## Flag

```text
boroCTF{c0mbobulat3_sp@gh3tti_nep0t1$m}
```
