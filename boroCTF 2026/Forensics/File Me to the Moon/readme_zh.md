# kitty kitty meow meow

## 題目描述

Frank sinatra accidentally deleted the file extension on one of his files!!!

What file extension is it supposed to be???

> boroCTF{file_extension}

## 解題思路

用 hex editor 打開以後可以很明顯看出他是 powerpoint 的檔案

![alt text](image.png)

之後就要判斷他是 ppt 還是 pptx 還是其他的，可以藉由使用 file 發現他是 2007+ 以後的檔案，所以副檔名是 pptx

```text
┌──(kali㉿kali)-[~/Desktop]
└─$ file superfile       
superfile: Microsoft PowerPoint 2007+
```

## Flag

```text
boroCTF{pptx}
```
