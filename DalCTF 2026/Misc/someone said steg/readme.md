# someone said steg?

## Description

everyone <3s steg right?

## Solution Walkthrough

This is an APNG, and you can see there are 16 frames in total. I first tried using strings, zsteg, LSB, etc., but didn't see anything meaningful.

After spending a lot of time on it, I realized that for a PNG's alpha channel, 0 usually means completely transparent and 255 means completely opaque. So I looked for values that were neither 0 nor 255, and then I found out those happened to be ASCII characters. Piecing them together gave me the flag.

## Flag

```text
dalctf{pianoman}
```
