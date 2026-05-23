# Rimal Transit

## 題目描述

Hidden stale copy with broken external file link. Do not publish.

## 解題思路

可以看到這幾筆從 00 到 05 的封包
![alt text](image.png)

排列完以後長這樣

```text
00 d6fqqaacoygguax7go
01 uaqmzqosuu5sjlrzhs
02 wswmjuwy4l2kjuvm3t
03 bjrex4ssenf7fc6lkj
04 rxh4rt2nvucqb3wbxo
05 zcsaaaaa
```

把第二欄串起來：

```text
d6fqqaacoygguax7gouaqmzqosuu5sjlrzhswswmjuwy4l2kjuvm3tbjrex4ssenf7fc6lkjrxh4rt2nvucqb3wbxozcsaaaaa
```

這串資料只使用小寫字母與 2-7，很像 Base32，將其轉成大寫後做 Base32 decode 可以看到開頭是 `1f 8b 08`，這是 gzip 的 magic bytes，解壓縮以後即可得到 flag

## Flag

```text
0xV01D{dns_frames_rebuilt_the_route_home}
```
