# Forbidden Attack

## 題目描述

`nc chal.thjcc.org 12002`

## 解題思路

連進去可以得到 nonce 和 三個 msg 以及 target

```text
NONCE 8c6d2f5c5cf96298463f22b7
MSG 77656c636f6d6520746f20746865207661756c742c207468657265206973206e6f7468696e6720746f207365652068657265 c4cab8e85e60fd409f24c8b746d525837e929be81cd5653b465bb871674e2510d1909dad3b45e7796d673f91d26ccf513b7d 0d5814e13a847e7a2b50ee929ea1395c
MSG 7374617475733a206e6f6d696e616c c0dbb5ff447ea240852485aa40d169 5e8347b42c92b3c61856faa418bad9ef
MSG 72656d696e6465723a20726f7461746520796f7572206b6579732c20736f6d65206461792c206d617962652c20627574206e6f7420746f646179 c1cab9e25f69fd12d16b9aac5ad171903f9e98e942d57a365a5af1717d52681b9e8094bd7902aa6c7b2529d8972ed24069769711d6821f1f57fb 98142749b2fa43e53e6ae31b766e44fd
TARGET 67697665206d652074686520666c6167
```

`MSG` 三欄分別是明文、密文、tag 的 hex，明文解出來是 `welcome to the vault, there is nothing to see here` 這類廢話，重點是三組訊息共用最上面那一個 `NONCE`，要我們對 `give me the flag` 這段 `TARGET` 補出合法的密文和 tag

密文那半很好處理，GCM 的加密就是 CTR，keystream 只跟 (key, nonce) 有關，nonce 重複代表三組用的是同一段 keystream，`pt ^ ct` 就直接把它挖出來，取最長的那組蓋過 16 bytes 的 `TARGET`，XOR 一下就是 target 的密文

tag 那半就是題目名字所指的 forbidden attack，nonce 重複時 GHASH 的 key `H` 可以從兩組 (ciphertext, tag) 解出來，直接去 github 找別人的實作 [jvdsn/crypto-attacks](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/gcm/forbidden_attack.py)，`recover_possible_auth_keys(a1, c1, t1, a2, c2, t2)` 吐出候選的 `H`，`forge_tag(h, a, c, t, target_a, target_c)` 拿 `H` 和一組已知訊息就能對任意密文算出 tag

Exploit:

1. 三組 `pt ^ ct` 取最長的當 keystream，`target ^ keystream` 得到 target 的密文
2. 拿前兩組 (ciphertext, tag) 餵 `recover_possible_auth_keys`（沒有 AAD，`a` 都是空的），得到候選的 `H`
3. 用第三組訊息驗證候選，過的就是真的 `H`
4. `forge_tag` 算出 target 密文的 tag，把密文和 tag 送回去就可以得到 flag

## Flag

```text
THJCC{h_r3c0v3r3d_gcm_1s_f0rb1dd3n_w1th0ut_fr3sh_n0nc3s}
```
