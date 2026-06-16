# Worthful Glory

## 題目描述

The sysadmin left behind a single photo of the Boro football field. He said the key was a field goal on game day. We need to recover the corrupted log file he hid, unlock it, and find the flag.

## 解題思路

一開始仔細觀察圖片可以發現左上角有一行字 `3P0INTERBABY` (不是 `3POINTERBABY`，因為這個我卡了好幾個小時)

![alt text](image.png)

接著用 `steghide extract -sf football_field_fixed.jpg` 把他當 passphrase 即可得到 `alexander_log.txt`

因為 `alexander_log.txt` 開頭是 PK，所以可以推斷他是一個壓縮檔

接著可以發現壓縮檔有密碼，通靈一下發現是 `football`，接著就得到 flag 了

## Flag

```text
boroctf{pixels_and_passwords_dont_mix}
```
