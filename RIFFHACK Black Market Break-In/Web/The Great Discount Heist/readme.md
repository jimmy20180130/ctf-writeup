# The Great Discount Heist

## Description

Expensive tools shouldn't be free, but some users claim they've found a way. Can you discover their secret?

## Solution Walkthrough

This challenge is a classic. By scrolling down on the `/auth` page, you can see a link to `/welcome`, which contains a promo code called `WELCOME20`.

Next, go to `/listing/macro-builder` to make a purchase. Why is this a classic? Because we can adjust the case of the promo code, tricking the system into thinking we are using a different code, and ultimately setting the price to 0 to get the flag.

![alt text](image.png)

## Flag

```text
bitflag{c0up0n_st4ck1ng_1s_4_d34l}
```
