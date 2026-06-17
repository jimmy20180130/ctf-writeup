# Qwerty!

## Description

I am so very sorry.... I made a lot of typos :(

I should rot in hell 😭

?AEAGJ8NJF,\0[d5JcE-

## Solution Walkthrough

1. **Step 1**:

    The problem description hints that this is ROT, but because the ciphertext contains many symbols and is not just letters, we must use ROT47, which can handle printable ASCII.

    First, apply ROT47:

    ```python
    s = r"?AEAGJ8NJF,\0[d5JcE-"

    def rot47(s):
        out = ""
        for c in s:
            x = ord(c)
            if 33 <= x <= 126:
                out += chr(33 + ((x - 33 + 47) % 94))
            else:
                out += c
        return out

    print(rot47(s))
    ```

    You will get:

    ```text
    nptpvyg}yu[-_,5dy4t\
    ```

2. **Step 2**:

    This doesn't look like the flag yet, so through my amazing observation skills, I discovered that if you shift every character one key to the left on the keyboard, you get the flag.

    ```text
    n -> b
    p -> o
    t -> r
    p -> o
    v -> c
    y -> t
    g -> f
    } -> {
    ```

    You will get:

    ```text
    boroCTF{typ0_m4st3r}
    ```

## Flag

```text
boroCTF{typ0_m4st3r}
```
