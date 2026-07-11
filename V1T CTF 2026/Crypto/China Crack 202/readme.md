# China Crack 202 Writeup

## Description

I spent lots of token on this

## Solution Walkthrough

The challenge uses ZUC to generate a keystream, then XORs the flag with the keystream:

```python
cipher_flag = xor(flag, keystream)
```

Therefore, as long as we can recover each 32-bit keystream word, we can directly recover the flag.

The challenge also outputs several leaks:

```python
leak1 = [((words[i] ^ words[i+1]) * 0x9e3779b1 >> 24) & 0xFF for i in range(len(words)-1)]
leak2 = [((words[i] * 0x45d9f3b) ^ (words[i] >> 16)) & 0xFFFF for i in range(len(words))]
leak3 = [bin(words[i]).count("1") for i in range(len(words))]
partial_crc = zlib.crc32(flag[:16])
```

Their functions are:

```text
leak1：relationship between adjacent keystream words
leak2：16-bit leak of a single keystream word
leak3：bit count of each keystream word
partial_crc：CRC32 of flag[:16]
```

By observing the leaks above, we can start from leak2, because it only keeps the final 16-bit result, making enumeration possible.

With leak1, leak3, partial_crc, and the known prefix, we can effectively filter possible flags. Starting from a known starting point, we can recover the entire flag step by step.

Below are the details of each leak:

### leak2

The challenge's leak2 is:

```python
leak2 = ((w * 0x45d9f3b) ^ (w >> 16)) & 0xFFFF
```

Since only the low 16 bits are kept at the end:

```text
(w * 0x45d9f3b) & 0xffff
```

It is only affected by the low 16 bits (lo), not by the high 16 bits (hi).

Therefore, it can be rewritten as:

```python
leak2 = ((lo * 0x45d9f3b) & 0xffff) ^ hi
```

This reduces the enumeration range from 2^32 directly to 2^16, and for each lo, we can directly derive hi:

```python
hi = leak2 ^ ((lo * 0x45d9f3b) & 0xffff)
word = (hi << 16) | lo
```

### leak1

leak1 gives the relationship between two adjacent keystream words:

```python
leak1[i] = (((words[i] ^ words[i+1]) * 0x9e3779b1) >> 24) & 0xff
```

So we can start from the first word and connect the next word layer by layer:

```python
if (((prev_word ^ cur_word) * 0x9e3779b1 >> 24) & 0xff) == leak1[i]:
    keep
```

If a word cannot be connected, we can discard it directly.

### leak3

The challenge gives:

```python
leak3 = [bin(words[i]).count("1") for i in range(len(words))]
```

So leak3 converts our guessed keystream word into binary, counts how many 1 bits it contains, and compares it with the correct leak. If it is not equal to the challenge's leak, we can discard it directly.

### flag prefix

Based on the flag format, the first 4 bytes of plaintext must be:

```python
b"V1T{"
```

Therefore, the first keystream word can be calculated directly:

```python
word0 = int.from_bytes(cipher_flag[:4] ^ b"V1T{", "big")
```

This allows the search to start from a unique starting point.

### partial_crc

The challenge gives:

```python
partial_crc = zlib.crc32(flag[:16])
```

So when we have recovered 16 bytes of plaintext, we can check:

```python
zlib.crc32(candidate_plain[:16]) == partial_crc
```

This can be used to check whether we are on a wrong path.

## Flag

```text
V1T{7fK9xL2mQp8ZrT5uWc3Yd6Hs0AaBbCcDdEeFf}
```
