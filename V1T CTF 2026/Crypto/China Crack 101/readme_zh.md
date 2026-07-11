# China Crack? - 101 Writeup

## 題目描述

"This is a Chinese signature and encryption algorithm"
The ZIP password is the same one used in last year’s challenge that sounds similar to this one, go find it.

## 解題思路

1. **第一步**：

    因為題目說類似去年的題目，所以我去2025的v1t ctf，發現了念起來很像的Tryna crack?(forensics)。

    https://2025.v1t.site/challenges/

    因為題目說zip的密碼去年有出現過，所以我在網路上找了別人的writeup來參考：

    https://yocchin.hatenablog.com/entry/2025/11/03/105306

    找到這個：

    ```text
    D4mn_br0_H0n3y_p07_7yp3_5h1d
    ```

    然後就可以把壓縮檔打開了。

2. **第二步**：

    把.secret裡面的資料從二進位轉ascii之後會變成`sqrt(SMSM)`，加上題目提示的Chinese signature and encryption algorithm，可以推測是SM2。

    並且檔案寫`.secret = zip_password + _V1T`，所以就是：

    ```text
    D4mn_br0_H0n3y_p07_7yp3_5h1d_V1T
    ```

    剛好可以拿來當private key，之後把challenge用SM2解密，就可以得到：

    ![alt text](cc01.png)

    ```text
    V1T{Tryna_cRacK_iS_BaCk_MtfK_[that-zip-password-in-md5]}
    ```

    所以flag就是：

    ```text
    V1T{Tryna_cRacK_iS_BaCk_MtfK_dffdf21a13908662e27d8c5c875809e4}
    ```

## Flag

```text
V1T{Tryna_cRacK_iS_BaCk_MtfK_dffdf21a13908662e27d8c5c875809e4}
```
