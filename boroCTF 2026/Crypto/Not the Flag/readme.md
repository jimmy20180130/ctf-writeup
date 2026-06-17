# Not the Flag

## Description

Challenge: So is this not the flag? If its not not, then what else?

```text
9d 90 8d 90 bc ab b9 84 8b 97 ce db a0 96 8c a0 91 cf 8b a0 91 90 8b a0 8b 97 cc a0 99 93 bf 98 82
```

## Solution Walkthrough

This is a sequence of hex bytes; perform a bitwise XOR with 0xff (bitwise NOT) on each byte, and then convert these hex bytes into ASCII.

## Flag

```text
boroCTF{th1$_is_n0t_not_th3_fl@g}
```
