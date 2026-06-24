# Riffhack Coupon Malleability Writeup

## Description

A riffhack vendor trusts encrypted coupon receipts because buyers cannot read them. Show that encryption without integrity still lets the right bytes move.

## Solution Walkthrough

1. **Step 1**:

   After connecting to the server, you will see:

   ```text
   :: RIFFHACK RECEIPT DESK ::
   [!] buyer export recovered from dead-drop cache
   policy gate: vendor/admin receipts only
   [leak] export parser saw grp=retail and tier=trial before encryption
   ---{ encrypted receipt }---
   issuer=riffhack-labs
   product=SilentCart receipt export
   receipt_nonce=47c03be4b9dd4162a5e90f8c5527d130
   receipt_blob=AT7WU7O2/Oj+QY/SrVLv2OCXh8Jd+YVSRoWCw0BSYOiWi4iZGgoaBqjDQZw5UCs0pszMZrP26BqavD/DBFBZKA==
   ---{ submit forged receipt }---
   $ receipt_nonce >>
   $ receipt_blob >>
   ```

   Both `receipt_nonce` and `receipt_blob` can be input.

   This challenge is an AES-CBC bit flipping attack; you can treat `nonce` as the IV.

   The goal of this challenge is to make the `blob` acceptable to the problem as vendor/admin receipts. Since the problem allows us to modify both `nonce` and `blob`, it is very likely that we need to modify the first part of the ciphertext from the IV, passing the check without corrupting any part of the ciphertext.

2. **Step 2**:

   The rest is to guess what the `blob` looks like. Since the problem states "vendor/admin receipts only," but if we want to modify them together, the shortest ciphertext is:

   ```text
   grp=vendor;tier=admin
   ```

   It requires 21 bytes, which cannot fit entirely within the first 16 bytes to be modified, so I suspect we only need to modify one of them.

   Possible orderings (any permutation of the four, as long as `grp` or `tier` is at the beginning):

   ```text
   grp/tier
   issuer
   product
   ```

   Write a script to guess the `blob` order and modify the `nonce` according to the `blob` order to obtain the flag.

   Final `nonce` and `blob`:

   ```text
   47c03be4bddd5b67a3f70f8c5527d130
   grp=retail;issuer=riffhack-labs;tier=trial;product=SilentCart
   ```

## Flag

```text
bitctf{{cbc_c0up0n5_n33d_m4c5}}
```
