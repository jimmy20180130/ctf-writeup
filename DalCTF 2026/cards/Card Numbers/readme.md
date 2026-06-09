# Card Numbers

## Description

I went to China a while back and while I was there I got offered a credit card. I don't know if it's a scam so I should check to see if my credit card number is valid.

## Solution Walkthrough

I first searched for China T-Union credit cards online and found the card number shown in the image.

![alt text](image.png)

Then I entered it, only to find that it said it wasn't a valid card. After looking into it, I realized the checksum was wrong. The original `3104900011000335379` summed up to 52, which is not a multiple of 10, making it invalid.

Changing the last digit to 7 fixes it (as the total becomes 50, which is a multiple of 10).

## Flag

```text
dalctf{H4v1ng_fun_w1th_cr3d1t_c4rds}
```
