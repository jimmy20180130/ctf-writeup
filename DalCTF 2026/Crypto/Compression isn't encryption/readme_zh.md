# Compression isn't encryption

## 題目描述

What could this binary mean? Seems to have a pretty variable length...

## 解題思路

根據題目的名稱以及他給的東西可以推論出這題是 Huffman coding

所以就在 AI 輔助下寫了一個腳本，大致上是先弄出一顆 Huffman tree，再用題目給的 bit string 從樹根開始解碼，遇到 0 走左子樹，遇到 1 走右子樹，走到葉節點時取得一個字元，然後回到樹根繼續解碼。

一開始若只依照 frequency 排序建立 Huffman tree，會得到 `dalctf{y311e8wi11_4m4eypt_32tni274}` 這種看似格式正確但內容不合理的結果。

原因是 Huffman tree 在權重相同時需要固定 tie-break 規則，否則不同實作會產生不同的 tree，解碼結果也會不同。 (solution.py 已經弄好了所以執行他會是正確的 flag)

## Flag

```text
dalctf{y0u_wi11_3ncrypt_4lw4y$}
```
