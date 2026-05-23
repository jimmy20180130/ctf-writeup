# Canvas Drift

## 題目描述

The provided artifact contains everything needed to recover one valid flag.

Flag format : 0xV01D{......}

Submit the complete flag exactly as shown by the format, including the prefix 0xV01D and the braces.

## 解題思路

先將 ppm 轉成 png，接著藉由題目可以發現他是 LSB 圖片隱寫
將轉換完的圖片丟到 https://stylesuxx.github.io/steganography/ 即可得到 flag

## Flag

```text
0xV01D{LSB_PIXELS_TELL_STORIES}
```
