# All's Fair in Love and CTFs

## Description

Help me decrypt this hidden message! Wrap result in dalctf{}

## Solution Walkthrough

It looks like this challenge uses a Playfair cipher, but the provided table was missing the second and fourth letters. After filling them in, it looks like this:

```text
A B C D E
F G H I K
L M N O P
Q R S T U
V W X Y Z
```

Once that is done, split the ciphertext into pairs: `CLDYIKMHILSUKCLQBF` -> `CL DY IK MH IL SU KC LQ BF`. Decrypting them according to the rules yields the flag.

```text
CL -> AN
DY -> YT
IK -> HI
MH -> NG
IL -> FO
SU -> RT
KC -> HE
LQ -> FL
BF -> AG
```

## Flag

```text
dalctf{anythingfortheflag}
```
