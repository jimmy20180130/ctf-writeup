# Follow The Layer

## Description

Our fraud response team flagged a suspicious USDT transfer linked to an online scam operation.

The payment trail starts here:

```text
d4500023a8114caaa640ab92bb8f73830a5303ccdfc4e9b0cf862bdae7ae336b
```

The money didn't just vanish — it was layered through a series of wallets before disappearing into the shadows. But every hop leaves a trace.

Trace the laundering chain, find where the money stops being attributable, and answer:

What is the **transaction hash** of the last traceable hop?
What **date** did it occur? *(MM/DD/YYYY)*
What is the **name** of the sanctioned entity at the heart of this operation? **Flag format**: `LYKNCTF{tx_hash:MM/DD/YYYY:ENTITY}` **Examble** :`LYKNCTF{a1b2c3...f64:01/15/2025:BINANCE}`

## Solution Walkthrough

Go to [this website](https://usdt.tokenview.io/cn/tx/d4500023a8114caaa640ab92bb8f73830a5303ccdfc4e9b0cf862bdae7ae336b) to see that this transaction involved a transfer of 2700 USDT from `TXk7Dor9GeRRpR5hbCGd4rBieM21v4BcwX` to `TNmRfnSUXZoWWzxcDDbf95eGQYXt1mJDt8`.

[Clicking into it](https://usdt.tokenview.io/cn/address/TNmRfnSUXZoWWzxcDDbf95eGQYXt1mJDt8), we can see that they later transferred 5222 USDT to `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`.

![alt text](image.png)

Continuing the investigation, we can see that `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` transferred 5222 USDT to `TJ7hhYhVhaxNx6BPyq7yFpqZrQULL3JSdb`. This is an exchange address due to the high frequency of transactions. According to the challenge, the transaction hash is `7e401f8004084d4bf9f792535fdf5b89138a935d027b6b75ceb2dd3ac8838fab` and the date is `03/21/2025`.

As for the sanctioned entity, we need to check [this website](https://sanctionssearch.ofac.treas.gov), where we can find it is `FUNNULL`.

![alt text](image-1.png)

## Flag

```text
LYKNCTF{7e401f8004084d4bf9f792535fdf5b89138a935d027b6b75ceb2dd3ac8838fab:03/21/2025:FUNNULL}
```
