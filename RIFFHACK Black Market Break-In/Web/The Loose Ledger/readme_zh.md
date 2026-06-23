# The Loose Ledger

## 題目描述

A buyer lookup tool is meant to retrieve one order at a time, but a loose query turns a single reference check into a wider ledger leak.

## 解題思路

題目說是 `buyer lookup tool`，於是轉向 `/orders` 去觀察，先輸入範例的 `escrow-1042`，查到了一筆訂單

![alt text](image.png)

於是我嘗試使用 SQL Injection，輸入 `' OR 1=1;--`，結果成功得到 flag

![alt text](image-1.png)

## Flag

```text
bitflag{1nj3ct10n_turn5_4_l00kup_1nt0_4_l34k}
```
