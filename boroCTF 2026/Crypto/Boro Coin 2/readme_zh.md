# Boro Coin 2

## 題目描述

Congratulations! You got their private key! Little problem ... we have no clue what to do with it. Could you generate a signature for us :). Please have the recipiant be "Boro_Confiscation_Committee". Since you're emptying the wallet anyway, just reuse the nonse again.

Note: This challenge does not contain a flag. You will need to submit the transaction signature (lowercase hex, no prefix) as the flag. Example: boroCTF{3045022100ed...}

## 解題思路

1. **第一步**：

    題目要求 reuse nonse，所以先從 transactions 裡面找相同的 r，再回推 nonse k。

    從上一題可以知道 r 為：

    ```text
    r = 2cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec7
    ```

    private key 為：

    ```text
    1b7ba9dafeb7c7a30fd8043a656c3ab89509db070dbd48b593d8e266b56ca22d
    ```

    初始餘額為 51.42，按順序套用交易，第 13 筆交易不能算，因為是 Suspect 轉給 Suspect，最後的餘額是 32.35。

    hash：

    ```text
    Suspect:Boro_Confiscation_Committee:32.35
    ```

    然後寫一個可以簽上面這個 message hash 的腳本，就可以得到 transaction signature(flag)。

## Flag

```text
boroCTF{304402202cbda85fc21f5e62f94d8378d2dad1a05bc5d5522d5a717f2bdf1df13d558ec70220033a47e398c6d81b053a235884c13b41f5618a6fa85715198a09beefdd5c3342}
```
