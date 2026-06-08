# LCG Seed Squared Writeup

## 題目描述
```text
I've been messing around with LCGs recently. I've forgotten the seed but I can remember I took something squared...
```

[LCGSeedSquared.py](https://dalctf2026.com/files/ac8457bd4520347e429cd7646c287947/LCGSeedSquared.py?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6Njk5fQ.aiYvvQ.6-fHsjDOwp-tFDAp-8iELQidSw4)
[output.txt](https://dalctf2026.com/files/565ae9d4460f95400888df30cf28ad06/output.txt?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzQwfQ.aiYvvQ.fB9rlNdzGn5slvEL3lSha3iM3WE)

## 解題思路

1. **第一步**：

    因為題目有固定的flag format：
    ```text
    Dalctf{
    ```
    
    所以可以用LCGSeedSquared.py的邏輯，從D暴力破解rng(x)，進而得到x的值。

    ```python
    def rng(y):
        return pow(int((175*y + 17) / 14 + 45), 15, 4294967295)

    X = 71303168 // ord('D')

    for x in range(10000):
        if rng(x) == X:
            print(x)
            break
    ```

2. **第二步**：

    得到x=324後，用x跑相同rng邏輯之後取mod，再用output除以每輪得到的rng(x)，就可以拿到flag。

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