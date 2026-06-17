# Satoshi: A Memory of The Past

## Description

All these crimes. Its not him. His soul is gone. It took his soul and trapped it inside the cache. I still hear his pulse.... Please don't lose his memory. I can't live without my beloved Satoshi.

> Satoshi's wife, Yukiko Nakamuda

(Note: the flag is already wrapped in boroCTF{} when you find it)

**UNRELATED TO THE OSINT CHALLENGES** *(other than the plot)*

## Solution Walkthrough

Observing it, we can see a bunch of items, which look like an array.

![alt text](image.png)

Looking further down, we can see that the data is XORed with 0x42 to get the flag.

![alt text](image-1.png)

## Flag

```text
boroCTF{s4t0sh1_1n_th3_c4ch3}
```
