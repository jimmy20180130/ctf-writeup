# Naive John

## Description

John is just like many people online: one username, one password, and way too many places to reuse it.

He goes by the username:

`quackyjohn42067`

Some people scatter their accounts everywhere. Others collect everything into a single flashy bio page, usually with a Discord presence and enough “e-gangster” . He talk about guns lol energy to scare absolutely nobody.

John left a locked note somewhere in his little internet shrine. Find the note, figure out what password he probably reused, and recover the flag.

His password hash: `9a6219cd940a3025b0f1773886c507a4dfee3a3f`

## Solution Walkthrough

I couldn't find anything on `quackyjohn42067` using various OSINT tools. Later, I noticed the challenge mentioned `e-gangster`, `single flashy bio page`, and `guns lol`. Anyone who frequently watches [NTTS](https://www.youtube.com/c/NoTextToSpeech) would immediately recognize this as the website guns.lol.

Going to guns.lol/quackyjohn42067, you can see [a link](https://anotepad.com/notes/bt5fnnjb). After entering the password, the flag is revealed.

The password, `charyarn53`, was obtained using [this website](https://hashes.com/en/decrypt/hash).

![alt text](image.png)

## Flag

```text
v1t{1113g41_051n7_15_7h3_n3w_m3t4_41ght}
```
