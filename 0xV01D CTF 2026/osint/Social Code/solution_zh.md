# Social Code

## 題目描述

Before Kali Team… there was another project.

A small online store called "Social-Code".

The store disappeared. The website is no longer online.

A billing invoice related to this project has been recovered. However, some details were lost during transfer.

but nothing truly disappears from the internet.

Your mission is to travel back in time,

find the archived version of the website,
locate the Instagram logo displayed on the homepage,
and extract the exact file name of that image.
⚠️ Only submit the image file name, including the extension.

Flag format:

> 0xV01D{filename.png}

Author: [F4R3S](https://instagram.com/fares_almahsery)

## 解題思路

看題目敘述可以發現他是一間叫做 social-code 的店  
我參考了[這個網站](https://www.collegesidekick.com/study-docs/16331200)，發現了一般長度為 3 的域名，例如 .org 的收據如下圖所示

![alt text](image.png)

仔細觀察可以發現題目給的圖片中 D 往後退了一格，代表他應該是 .shop 而不是其他的 .com 等等  

接著去 [wayback machine 上面找](https://web.archive.org/web/20250329141912/http://social-code.shop/)，然後就可以看到圖片名稱了

## Flag

```text
0xV01D{1_c15cd605-362b-4f64-91f0-085ad2805b3f.png}
```
