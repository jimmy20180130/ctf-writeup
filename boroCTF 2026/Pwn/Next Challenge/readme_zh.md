# Next Challenge

## 題目描述

Psst...I've been hearing some rumors about this special command called nc. I don't know what it is so I have to assume it means Next Challenge ... right?? Maybe that MAN has more answers.

```text
nc thww9zyp6ygt.boroctf.com 19350
```

## 解題思路

進去之後先用 help 看一下有什麼指令，發現有 cheese 跟 flag。

選 cheese 的話會掉進陷阱裡，會被無情嘲諷然後斷開連接(沒截到圖)。

選 flag 的話，之後會問你要不要看看 cheese，然後選 n 就可以拿到 flag。(選 y 的話八成也是貼臉開大然後 disconnected 吧)

![alt text](image.png)

## Flag

```text
boroCTF{0nLinE_C@ts*}
```
