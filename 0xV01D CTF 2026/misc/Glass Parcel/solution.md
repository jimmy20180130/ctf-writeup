# Glass Parcel

## Description

The provided artifact is self-contained. Analyze it carefully and submit the recovered flag.

Flag format : 0xV01D{......}

Submit the complete flag exactly as shown by the format, including the prefix 0xV01D and the braces.

## Solution Walkthrough

1. Notice that there is a zip file in polyglot.png.
2. unzip polyglot.zip
3. XOR payload.bin with 0x42

## Flag

```text
0xV01D{POLYGLOT_FILES_CAN_SING}
```
