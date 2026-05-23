# Buried Session

## Description

The provided artifact is self-contained. Analyze it carefully and submit the recovered flag.

Flag format : `0xV01D{......}`

Submit the complete flag exactly as shown by the format, including the prefix `0xV01D` and the braces.

## Solution Walkthrough

The entropy of artifact.bin is very high. After using `file` and `strings`, I can't find any flags or any common file header.
I tried to bruteforce XOR the file with key from 00 to FF. So I made a script to bruteforce it, after finished, the script will find the zlib header and try to decompress and find the flag.

## Flag

```text
0xV01D{XOR_ZLIB_LAYER_CAKE}
```
