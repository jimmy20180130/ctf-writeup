# Scảry Duck

## Description

Can you peel back all the layers of protection and find the flag?

Good luck!

## Solution Walkthrough

After downloading, you will find `challenge.mp4` inside the archive. The beginning consists of AI slop, and around the three-second countdown, a very sus sound and image appear.

By treating the white pixels as 1 and black pixels as 0, you get `11010110 11101110 00101111 11011101`, which converts to the hex `D6EE2FDD`.

![alt text](image.png)

Next is the audio. There are eight different frequencies: `600, 2250, 1800, 2250, 900, 1200, 1050, 2700`. It is easy to notice that they are all multiples of 150.

Subtracting 600 from each and then dividing by 150 gives `0 11 8 11 2 4 3 14`. Converting these to hex results in `0B8B243E`.

After trying some permutations, the final password was found to be `0b8b243ed6ee2fdd`.

Then, you can see `solver.py` and `flag.enc`. `solver.py` should actually be named `encrypt.py`. Regardless, the process is `reverse -> xor -> base64 encode`.

```py
@base64_layer
@xor_layer
@reverse_layer
def encode(data: bytes) -> bytes:
    return data
```

Following the steps above and using `0b8b243ed6ee2fdd` as the XOR key, you get the string `-0day-I05Dqrhk0WASzcVa4EovsSduXJpFxRpKbjORsM9-RCE-`. Decoding the middle part `I05Dqrhk0WASzcVa4EovsSduXJpFxRpKbjORsM9` using base62 gives the flag. The process is as follows:

![alt text](image-1.png)

## Flag

```text
V1T{7h47_dUck_l00k_5c4ry_7h0}
```
