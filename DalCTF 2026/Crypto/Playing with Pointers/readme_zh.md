# Playing with Pointers

## 題目描述

I watched a youtube video earlier showing off this funny trick you can do with pointers. I forget what it's called though. Maybe I'll go play some Quake to think about it.

## 解題思路

1. **第一步**：

    題目給的程式還缺了一些：

    ```c
    for(int i=0;i<x;i++){
        fflag[i] = (float) FLAG[i];
        fflag[i] = fflag[i] * fflag[i];
        // man I forgot what line needs to go here... Maybe I should play some quake to think about it
    }
    ```

    藉由quake的提示，很明顯是少了Fast inverse square root的magic number，所以我把缺少的程式碼補上。~~也補上了wtf?~~

    ```c
    for(int i=0;i<x;i++){
        fflag[i] = (float) FLAG[i];
        fflag[i] = fflag[i] * fflag[i];
        lflag[i] = 0x5f3759df - ((*(long *)&fflag[i]) >> 1); // what the fuck?
    }
    ```

2. **第二步**：

    原始加密方式：

    flag char → ASCII → float → 平方 → float bit pattern → output

    其中float bit pattern可以用來做圖形處理，所以才有這個優化算法。

3. **第三步**：

    解密：

    用暴力破解的方式，讓每個字元都跑一樣的流程，只要對上output就是正確的flag。

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
