# Spoiled Cheese Pull

## Description

My cheese got pulled and now I can't eat it. Can you help me find out who did it?

## Solution Walkthrough

You can see that the downloaded file is `chall.png`, but its file header actually starts with `JFIF`. Change it to `PNG`, and fix the chunk names: `IHET -> IHDR`, `ISAD -> IDAT`, and `SEND -> IEND`.

Once fixed, you will get a QR code. Simply use any online QR code scanner to get the flag.

## Flag

```text
dalCTF{WhY_$O_L0N5}
```
