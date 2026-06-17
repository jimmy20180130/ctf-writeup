# Coming Together

## 題目描述

You have yours and I have mine. Together we have something larger than ourselves.

```text
nc oq7qaruz5vsw.boroctf.com 25287
```

## 解題思路

1. **第一步**：

    chal的邏輯大概長這樣：

    ```c
    puts("What number will you contribute?");
    fgets(buf, 12, stdin);

    my_number = 2;
    your_number = atoi(buf);

    if (your_number > 10000) {
        puts("Wow there, try not to out do my number too much.");
        your_number = 1;
    }

    if (your_number < 0) {
        puts("No negatives!");
        your_number = -your_number;
    }

    total = my_number + your_number;

    if (total < 0) {
        puts("Huh? That's not supposed to happen.");
        // print flag
    }
    ```

2. **第二步**：

    C 的 int 範圍是 -2147483648 到 2147483647，所以我送出 -2147483648，程式會觸發 No negatives!，想要把我的 input 轉成正數。

    但因為 int 正數上限是 2147483647，沒辦法轉成正數，仍然維持 -2147483648，在最後計算 total 時，就算 my_number 是 2147483647，total 也會是 -1，所以一定會觸發 print flag。

## Flag

```text
boroCTF{tw0s_c0mpl3men+_M3}
```
