# XorVault

## Description

Something is locked away. It was locked more than once, by more than one hand. Find what was left behind.

Flag format: 0xV01D{...}

hint : Focus on the order of operations applied to each byte, especially anything using i % 8 or d[i] ^= i.

## Solution Walkthrough

From the title, we can see this is about XOR operations. From the description, we can infer XOR is performed multiple times. The hints show `i % 8` and `d[i] ^= i`:

- `i % 8` indicates a key of length 8, cycling every 8 bytes
- `d[i] ^= i` means each byte is XORed with its own index

Since the flag format is `0xV01D{...}`, we can use known plaintext to deduce the encryption process. I first assumed `cipher[i] = plain[i] XOR key[i % 8] XOR i`, which gives us the key: `47 d6 11 ce ee 91 75`.

Common byte operations besides XOR include rotate and add/sub. After testing rotate, we get `de ad be ef ca fe ba`. Using the final `}` character, we can derive the complete key: `de ad be ef ca fe ba be`.

Following this process, we can decrypt the flag:

```text
cipher byte
-> XOR i
-> rotate right 3 bits
-> XOR key[i % 8]
-> plain byte
```

## Flag

```text
0xV01D{X0R_V4ULT_0P3N3D}
```
