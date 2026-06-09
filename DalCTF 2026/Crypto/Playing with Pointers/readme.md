# Playing with Pointers

## Description

I watched a youtube video earlier showing off this funny trick you can do with pointers. I forget what it's called though. Maybe I'll go play some Quake to think about it.

## Solution Walkthrough

1. **Step 1**：

    The program provided by the challenge is still missing something:

    ```c
    for(int i=0;i<x;i++){
        fflag[i] = (float) FLAG[i];
        fflag[i] = fflag[i] * fflag[i];
        // man I forgot what line needs to go here... Maybe I should play some quake to think about it
    }
    ```

    Based on the Quake hint, it is obvious that the missing part is related to the magic number from Fast inverse square root, so I added the missing code. ~~I also added wtf?~~

    ```c
    for(int i=0;i<x;i++){
        fflag[i] = (float) FLAG[i];
        fflag[i] = fflag[i] * fflag[i];
        lflag[i] = 0x5f3759df - ((*(long *)&fflag[i]) >> 1); // what the fuck?
    }
    ```

2. **Step 2**：

    The original encryption process is:

    flag char → ASCII → float → squared → float bit pattern → output

    The float bit pattern can be used for graphics processing, which is why this optimization algorithm exists.

3. **Step 3**：

    Decryption:

    Use brute force. For each character, run the same process, and if the result matches the output, that character is part of the correct flag.

    ```python
    import struct

    outputs = [
        1167097856,
        1175651328,
        1177960448,
        1166821376,
        1172078592,
        1167663104,
        1181508608,
        1179558912,
        1158676480,
        1178182656,
        1159892992,
        1175258112,
        1176670208,
        1172424704,
        1178406912,
        1175258112,
        1180517376,
        1159073792,
        1161629696,
        1177092096,
        1175258112,
        1170735104,
        1158676480,
        1159073792,
        1178406912,
        1161629696,
        1159892992,
        1179324416,
        1160744960,
        1182016512,
    ]

    def encode_char(ch):
        f = float(ord(ch))
        f = f * f

        bits = struct.unpack("<I", struct.pack("<f", f))[0]
        return bits

    flag = ""

    for target in outputs:
        for c in range(32, 127):
            ch = chr(c)

            if encode_char(ch) == target:
                flag += ch
                break
        else:
            flag += "?"

    print(flag)
    ```

## Flag

```text
DalCTF{s0m3_fUn_w17h_P01n73r5}
```
