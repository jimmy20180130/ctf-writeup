# Not Your Time

## 題目描述

One of the trifecta of bitwise operations.

## 解題思路

用 IDA 打開可以發現，程式會檢測輸入的每個字元，將其進行位元反轉後取其低位元組（lobyte），並比對是否和 v6 陣列中的對應字元相等

所以就寫了一個腳本然後就拿到 flag 了

## Flag

```text
boroCTF{N0t_nO+_tH3_FL@g}
```
