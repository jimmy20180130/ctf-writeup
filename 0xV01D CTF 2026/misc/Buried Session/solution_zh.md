# Buried Session

## 題目描述

The provided artifact is self-contained. Analyze it carefully and submit the recovered flag.

Flag format : `0xV01D{......}`

Submit the complete flag exactly as shown by the format, including the prefix `0xV01D` and the braces.

## 解題思路

題目給的 artifact.bin 的熵值很高，而且用 strings 後找不到什麼有用的資料，也看不到常見的 file header
所以我就先懷疑他是將原本的檔案做 XOR，在不知道 key 的情況下，我就決定先從 00 到 FF 來爆破
我就寫了個腳本，先爆破之後尋找 zlib header，再使用 zlib.decompress() 解壓，若解壓成功，再搜尋是否有符合 flag 格式的字串。

## Flag

```text
0xV01D{XOR_ZLIB_LAYER_CAKE}
```
