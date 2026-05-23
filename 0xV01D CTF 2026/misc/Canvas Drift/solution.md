# Canvas Drift

## Description

The provided artifact contains everything needed to recover one valid flag.

Flag format : 0xV01D{......}

Submit the complete flag exactly as shown by the format, including the prefix 0xV01D and the braces.

## Solution Walkthrough

1. convert canvas.ppm to canvas.png.
2. this is a challenge of LSB steganography, so use [this website](https://stylesuxx.github.io/steganography/) and get the flag.

## Flag

```text
0xV01D{LSB_PIXELS_TELL_STORIES}
```
