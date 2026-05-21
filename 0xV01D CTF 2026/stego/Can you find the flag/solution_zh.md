# Can you find the flag

## 題目描述

i accedntly downloaded this picture insted of a whole website can you find the website files or a flag?

### 提示

1. Hint: fr it's easy  
    Have you checked E9 exif my guy? forget about the zip it's just a fake flag  
    Go on i wanna see the 1st blood guys!!!
2. Hint: trust me it worth it  
    `https://gofile.io/d/tdNLHn` i changed sth in it to make it easier for you now!!

## 解題思路

先看下載下來的 `cicada_original.jpg`，可以看到有一串 hex string
接下來看提示可以根據連結下載 `E9.jpg`，裡面圖片有一串 base64 編碼的字串 `aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9maWxlLzV4a21ubGVueWI5a3QzaC81RTJSL2ZpbGU=`
可以得到 `https://www.mediafire.com/file/5xkmnlenyb9kt3h/5E2R/file`，下載下來後可以看到 `5E2R` 這個檔案，他是 gzip/tar，用 hex editor 可以看到後半段的 flag，`1ng_St3g0_D4mn_WP}` 和前半段 `0xV01D{St4rt3d_S0lv`，合在一起就是 flag

## Flag

```text
0xV01D{St4rt3d_S0lv1ng_St3g0_D4mn_WP}
```
