# Et Tu, Brute

## Description

Stabbed by his own men. Each stab wound marked how betrayed he was. Can you reverse the damage?

erurFWI{@iu13qgq0pru3}

## Solution Walkthrough

From `erur`, we can guess that this might be some kind of Caesar cipher. Upon observation, it was discovered that this challenge uses ROT -3. By shifting each character of the provided `erurFWI{@iu13qgq0pru3}` backward by 3 positions (ignoring symbols), you can obtain the flag.

## Flag

```text
boroCTF{@fr13ndn0mor3}
```
