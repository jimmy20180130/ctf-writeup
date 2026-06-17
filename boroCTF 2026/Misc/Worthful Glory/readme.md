# Worthful Glory

## Description

The sysadmin left behind a single photo of the Boro football field. He said the key was a field goal on game day. We need to recover the corrupted log file he hid, unlock it, and find the flag.

## Solution Walkthrough

Upon closer observation of the image, you can see a line of text in the top-left corner: `3P0INTERBABY` (not `3POINTERBABY`, which is where I got stuck for a few hours).

![alt text](image.png)

Next, use `steghide extract -sf football_field_fixed.jpg` and use that as the passphrase to obtain `alexander_log.txt`.

Since `alexander_log.txt` starts with PK, it can be inferred that it is a compressed archive.

I then discovered the archive is password-protected. After some intuition, I found the password to be `football`, which then yielded the flag.

## Flag

```text
boroctf{pixels_and_passwords_dont_mix}
```
