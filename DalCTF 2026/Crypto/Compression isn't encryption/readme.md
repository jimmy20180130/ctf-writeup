# Compression isn't encryption

## Description

What could this binary mean? Seems to have a pretty variable length...

## Solution Walkthrough

Based on the challenge name and the provided materials, it can be inferred that this challenge involves Huffman coding.

So, with the assistance of AI, I wrote a script. The general process is to first construct a Huffman tree, and then use the bit string provided by the challenge to decode starting from the root. Go to the left subtree when encountering a 0, and go to the right subtree when encountering a 1. Upon reaching a leaf node, retrieve the character and return to the root to continue decoding.

Initially, if the Huffman tree is built by sorting solely based on frequency, it yields a result like `dalctf{y311e8wi11_4m4eypt_32tni274}`, which looks correct in format but makes no sense in content.

The reason is that a fixed tie-break rule is required when weights are identical in a Huffman tree; otherwise, different implementations will generate different trees, leading to different decoding results. (solution.py has already been fixed, so running it will give the correct flag).

## Flag

```text
dalctf{y0u_wi11_3ncrypt_4lw4y$}
```
