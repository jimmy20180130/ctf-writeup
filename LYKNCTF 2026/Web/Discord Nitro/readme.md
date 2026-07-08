# Discord Nitro

## Description

Free Discord Nitro

## Solution Walkthrough

First, log in with the username `guest` and password `guest`. You will notice that it issues a JWT.

Since I didn't know the secret and didn't feel like guessing, I set the `alg` to `none`. I then discovered that the server does not verify the signature. After that, I entered the admin panel to retrieve the flag.

## Flag

```text
LYKNCTF{51c3237f94a1404aa9ce6423e096643f} (dynamic flag)
```
