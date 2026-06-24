# Aperture Science Test Chambers

## 題目描述

GLaDOS has locked the flag behind twenty Aperture Science test chambers. Each chamber is an illuminated panel grid — pressing any panel toggles it and all its immediate neighbours. Find the sequence of presses that extinguishes every panel in each chamber, and she will release what you've earned.

## 解題思路

這個題目是一個按燈泡的遊戲，原理是這樣的

正方形板子上面有很多個燈泡，有的是暗的有的是亮的，當按下某格時，它上下左右的燈泡都會切換狀態 (亮的變暗，暗的變亮)，我們要做的事就是要找到方法把全部的燈泡都關掉

了解玩法以後參考網路上的解法就可以了

## Flag

```text
bitctf{{gl4d0s_s4ys_y0u_p4ss3d_4ll_ch4mb3rs}}
```
