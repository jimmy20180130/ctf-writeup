# LCG Seed Squared

## Description

I've been messing around with LCGs recently. I've forgotten the seed but I can remember I took something squared...

## Solution Walkthrough

1. **Step 1**：

    Since the challenge has a fixed flag format (`Dalctf{`)

    We can use the logic from LCGSeedSquared.py and brute-force rng(x) starting from D, which allows us to recover the value of x.

    ```python
    def rng(y):
        return pow(int((175*y + 17) / 14 + 45), 15, 4294967295)

    X = 71303168 // ord('D')

    for x in range(10000):
        if rng(x) == X:
            print(x)
            break
    ```

2. **Step 2**：

    After obtaining x=324, we run the same rng logic with x and take the modulo result. Then, by dividing each output value by the corresponding rng(x) value for that round, we can recover the flag.

    ```python
    seed = ""

    def rng(y):
        x = pow(int((175*y + 17) / 14 + 45), 15, 4294967295)
        return x

    en = []

    with open("output.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                en.append(int(line))


    x = 324

    for i in range(0, len(seed)):
        x += ord(seed[i])

    flag = ""

    for t in en:
        x = rng(x)
        ch = t // x
        flag += chr(ch)

    print(flag)
    ```

## Flag

```text
DalCTF{533m1ng1y_r4nd0m1y_g3n3r473d_num63rs}
```
