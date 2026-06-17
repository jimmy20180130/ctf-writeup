# Coming Together

## Description

You have yours and I have mine. Together we have something larger than ourselves.

```text
nc oq7qaruz5vsw.boroctf.com 25287
```

## Solution Walkthrough

1. **Step 1**:

    The logic of the chal looks roughly like this:

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

2. **Step 2**:

    The range for a C `int` is -2147483648 to 2147483647, so when I send -2147483648, the program triggers "No negatives!" and attempts to convert my input into a positive number.

    However, because the maximum positive value for an `int` is 2147483647, it cannot be converted to a positive number and remains -2147483648. In the final calculation of `total`, even if `my_number` is 2147483647, the `total` will still be -1, so the flag will definitely be printed.

## Flag

```text
boroCTF{tw0s_c0mpl3men+_M3}
```
