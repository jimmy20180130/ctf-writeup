# Spoiled Cheese Pull

## 題目描述

My cheese got pulled and now I can't eat it. Can you help me find out who did it?

## 解題思路

可以發現下載下來是 chall.png，但是開頭卻是 JFIF，把他改成 PNG，並修正 `IHET -> IHDR`，`ISAD -> IDAT`，`SEND -> IEND`

好了以後會得到一個 qrcode，網路上隨便找個 qrcode scanner 即可得到 flag

## Flag

```text
dalCTF{WhY_$O_L0N5}
```
