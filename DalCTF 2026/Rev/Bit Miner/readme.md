# Bit Miner

## Description

Mine, upgrade, and mine some more! Think outside the box and buy the flag in the shop. (Note: when making an account, make sure other users can't guess your password and use your bits!)

## Solution Walkthrough

By observing `main.c`, we can see that there is a logical flaw in the deduction mechanism. The balance check uses the old `bits` value, but after confirming the purchase, the account data is reloaded. Furthermore, `bits` is an `unsigned long`, which means it can be deducted into a negative value, resulting in an underflow.

```c
void buy(int item, int level, unsigned long price, unsigned long bits) {
    if (price > bits) {
        printf("You don't have enough money for this item\n");
        return;
    }

    char option_chr = 'X';
    while (option_chr != 'y' && option_chr != 'n') {
        printf("Confirm purchase (y / n): ");
    
        do {
            option_chr = fgetc(stdin);
        } while (option_chr <= ' ');
    } 

    if (option_chr == 'n') {
        return;
    }

    Account account = storage_get_account(username);

    switch (item) {
        case 1:
            account.speed_upgrades = level;
            break;
        case 2:
            account.bonus_upgrades = level;
            break;
        case 3:
            account.bonus_chance_upgrades = level;
            break;
        case 4:
            printf("Flag: %s\n", FLAG);
            break;
    }

    account.bits -= price;

    storage_save_account(username, account);
}
```

From the above results, we can infer that this is a TOCTOU (Time-of-Check to Time-of-Use) vulnerability. The solution is to mine until the account has 10 bits, then open two concurrent connections using the same account to purchase an upgrade simultaneously.

The first connection will successfully make the purchase, deducting 10 bits and leaving the balance at 0. However, the second connection then reads the balance as 0, and deducting another 10 bits makes it -10. Since `bits` is an `unsigned long`, subtracting 10 from 0 causes an unsigned integer underflow.

In a 64-bit environment, the result will become 2^64 - 10 = 18446744073709551606. This value is far greater than the price of the flag, allowing us to purchase the flag directly.

## Flag

```text
dalctf{b1t_w4rp1ng_5ucc3s5ful}
```
