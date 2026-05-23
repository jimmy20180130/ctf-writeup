# Glass Parcel

## 題目描述

The provided artifact is self-contained. Analyze it carefully and submit the recovered flag.

Flag format : 0xV01D{......}

Submit the complete flag exactly as shown by the format, including the prefix 0xV01D and the braces.

## 解題思路

可以看到圖片藏了一個 zip
把裡面的 payload.bin 依照提示跟 0x42 做 xor 即可得到 flag

## Flag

```text
0xV01D{POLYGLOT_FILES_CAN_SING}
```
