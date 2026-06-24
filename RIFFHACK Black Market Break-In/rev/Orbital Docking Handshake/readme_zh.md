# Orbital Docking Handshake

## 題目描述

The docking console hides its handshake phrase in a runtime-built buffer behind one more computed alignment value. Use the lightest reversing path and recover both values.

## 解題思路

這個程式進去後要先輸入 `Docking phrase` 和 `Alignment window`，之後判斷輸入的 `Docking phrase` 是否等於它預期的結果，再比對 `Alignment window` 和計算好的結果是否一樣，是的話才印出 flag

其中 flag 是被加密的，需要使用程式預期的 `Docking phrase` 和用它計算出的 `Alignment window` 才能解密

所以我就寫了一個腳本解出 flag，要注意因為 `mask_for()` 回傳的是 `unsigned __int8`，而 `print_flag()` 的第二個參數是 `char`，所以在需要 AND 0xff 來保留低 8 bits，這樣和 C 的結果才會一樣

## Flag

```text
bitctf{{0rb1t4l_d0ck1ng_r0ut1n3}}
```
