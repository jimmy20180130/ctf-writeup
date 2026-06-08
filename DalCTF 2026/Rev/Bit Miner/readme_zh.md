# Bit Miner

## 題目描述

Mine, upgrade, and mine some more! Think outside the box and buy the flag in the shop. (Note: when making an account, make sure other users can't guess your password and use your bits!)

## 解題思路

觀察 main.c 可以發現在扣款的時候邏輯出了一些問題，檢查餘額用的是舊的 bits，但確認購買以後又會重新讀取一次帳號資料，此外可以發現 bits 是
 unsigned long，代表可以被扣到負數導致 overflow

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

由上述結果可以得知這是一個 TOCTOU 問題，解法是先挖礦挖到帳號有 10 bits，用同個帳號開兩個連線同時買 upgrade，第一個帳號會成功購買，並且被扣十塊錢，餘額為 0，但是第二個連線讀取到的餘額為 0，再扣十塊就會變成 -10 元，然而因為 bits 是 unsigned long，所以 0 - 10 會發生 unsigned integer underflow

在 64-bit 環境下，結果會變成 2^64 - 10 = 18446744073709551606，這個數值遠大於 flag 的價格，因此可以直接購買 flag。

## Flag

```text
dalctf{b1t_w4rp1ng_5ucc3s5ful}
```
