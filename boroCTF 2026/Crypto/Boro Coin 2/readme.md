# Boro Coin 2

## 題目描述

Congratulations! You got their private key! Little problem ... we have no clue what to do with it. Could you generate a signature for us :). Please have the recipiant be "Boro_Confiscation_Committee". Since you're emptying the wallet anyway, just reuse the nonse again.

Note: This challenge does not contain a flag. You will need to submit the transaction signature (lowercase hex, no prefix) as the flag. Example: boroCTF{3045022100ed...}

## 解題思路

1. **Step 1**:
    The problem requires reusing the nonce, so first find the identical r from the transactions, and then deduce the nonce k.
    From the previous problem, we know that r is:

    ```text
    r = 2cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec7
    ```

    The private key is:

    ```text
    1b7ba9dafeb7c7a30fd8043a656c3ab89509db070dbd48b593d8e266b56ca22d
    ```

    The initial balance is 51.42. Apply the transactions in order. The 13th transaction should not be counted because it is a transfer from Suspect to Suspect. The final balance is 32.35.
    hash:

    ```text
    Suspect:Boro_Confiscation_Committee:32.35
    ```

    Then, write a script that can sign the above message hash, and you will get the transaction signature (flag).

## Flag

```text
boroCTF{304402202cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec70220033a47e398c6d81b053a235884c13b41f5618a6fa85715198a09beefdd5c3342}
```
