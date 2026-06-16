# Looking through Windows

## 題目描述

My friend thinks he can hide his secrets from me by deleting them...

Who's gonna tell him?

## 解題思路

用 `strings -el challenge.vhd` (用 -el 是因為 NTFS 檔名通常是 UTF-16LE) 可以發現幾個可疑的檔案 `$IIFYI8L.zip`, `flag.zip`, `$RIFYI8L.zip`

上網查了一下可以發現 `$Ixxxx.ext` 是檔案的 metadata，而 `$Rxxxx.ext` 是被刪除檔案的本體，所以可以推斷出 `$RIFYI8L.zip` 就是被刪除的 flag.zip，所以用 Autopsy 簡單看一下就可以看到並提取 `$RIFYI8L.zip`

![alt text](image.png)

之後我發現這個 zip 有設密碼，使用我們的老朋友 john 即可爆破密碼並得到 flag，密碼是 `forget92936281`

## Flag

```text
boroCTF{f!l3_f0r3nsics_FTW!!}
```
