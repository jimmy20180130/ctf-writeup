# Riffhack Coupon Malleability Writeup

## 題目描述

A riffhack vendor trusts encrypted coupon receipts because buyers cannot read them. Show that encryption without integrity still lets the right bytes move.

## 解題思路

1. **第一步**：

   連上伺服器後，會跳出：

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

   其中 `receipt_nonce` 跟 `receipt_blob` 都可以輸入。

   這題是 AES-CBC 的 bit flipping，把 `nonce` 當成 IV 就可以了。

   這題的目標是把 `blob` 弄成題目可以接受的 vendor/admin receipts。既然題目同時給我們改 `nonce` 跟 `blob`，就代表很有可能要從 IV 改 ciphertext 的第一部分，在不讓任何 ciphertext 壞掉的情況下通過檢查。

2. **第二步**：

   剩下的就是猜 `blob` 長怎樣了，因為題目有說 vendor/admin receipts only，但如果要一起改的話，最短的 ciphertext 是：

   ```text
   grp=vendor;tier=admin
   ```

   要 21 bytes，不可能一起放在前 16 bytes 改完，所以猜出應該是改其中一個就好。

   可能的排序（四個隨便交換，`grp` 或 `tier` 在前面就好）：

   ```text
   grp/tier
   issuer
   product
   ```

   寫腳本猜 `blob` 順序，並依照 `blob` 順序改 `nonce`，就可以得到 flag。

   最終 `nonce` 與 `blob`：

   ```text
   47c03be4bddd5b67a3f70f8c5527d130
   grp=retail;issuer=riffhack-labs;tier=trial;product=SilentCart
   ```

## Flag

```text
bitctf{{cbc_c0up0n5_n33d_m4c5}}
```
