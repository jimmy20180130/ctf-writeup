# someone said steg?

## 題目描述

everyone <3s steg right?

## 解題思路

這是一張 apng，可以看到總共有 16 幀。我先嘗試用 strings 和 zsteg 以及 lsb 等等的都沒看到有意義的東西

接著搞了很久發現 png 的 alpha 通常 0 是完全透明，255 是完全不透明，所以就找不是 0 也不是 255 的，之後就發現那些剛好是 ASCII，拼起來就是 flag

## Flag

```text
dalctf{pianoman}
```
