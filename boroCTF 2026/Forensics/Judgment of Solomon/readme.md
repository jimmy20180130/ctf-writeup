# Judgment of Solomon

## Description

The birth of reconstruction.

## Solution Walkthrough

You can see a string `boroCTF{I_C0xL6n"+_d0_it_St11nz_n0w_go}` hidden in the code, but that is not the flag.

After trying many methods, I thought about using color codes: `FFFFFF` for white, `000000` for black, `FF0000` for red, and `0A` for a newline. Following these rules, I could get something that looked like a QR code.

After generating `code.png`, I noticed that the square frames in the top-left, top-right, and bottom-left were missing. So, I used PowerPoint to add them back, and then I could get the flag.

You can find the square frames by simply searching for "qrcode" on Google.

![alt text](image.png)

## Flag

```text
boroCTF{I_f1%ed_wHat_w4$_br0Ken}
```
