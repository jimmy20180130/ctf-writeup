# Enc Writeup

## 題目描述

Oh no, My Flag is gone :<

## 解題思路

1. **第一步**：

    strings 掃一遍 enc.exe 之後可以看到一些關鍵字：

    ```text
    flag.png
    flag.enc
    ChaCha7539Engine
    AES
    PKCS7
    BouncyCastle
    ```

    所以這題應該是圖片被AES跟ChaCha7539加密之後被轉成.enc輸出。

    在 Ghidra 裡找到引用 flag.png / flag.enc 的 function 後，可以看出大致流程：

    ```text
    File.ReadAllBytes("flag.png")
        ↓
    AES encryption
        ↓
    ChaCha7539 encryption
        ↓
    File.WriteAllBytes("flag.enc", ...)
    ```

    所以解密時要反過來：

    ```text
    flag.enc
        ↓ ChaCha7539 decrypt
    AES ciphertext
        ↓ AES-256-ECB decrypt
    padded PNG
        ↓ PKCS#7 unpad
    flag.png
    ```

2. **第二步**：

    找程式裡面的 key，但程式裡不是直接放 AES key、ChaCha key 和 nonce，而是放了兩段 hardcoded hex 資料。

    還原後可以得到：

    ```python
    SEED_1 = bytes.fromhex(
        "926c3b1ec823f9414596ac39cbedb742"
        "f6b3e9a9411517da358c4f93ff630841"
        "bd3aea9a1010941ab48117ca1faa7c85"
    )
    SEED_2 = bytes.fromhex(
        "ba6168403341c29303bbe73e9b9c5ee1"
        "636ccc4e63d7e3fcbcc24a96de1569a8"
        "d588ffe4caf4541165281f7aada9eaf6"
        "6ff2b3c527232a1fce8a56fa3ece728a"
        "769b3e816ec195fee556dc18"
    )
    ```

    接著程式會用 SEED_1 來加密 SEED_2，得到真正的 key：

    ```text
    AES-CBC-PKCS7(
        plaintext = SEED_2,
        key       = SEED_1[16:],
        iv        = SEED_1[:16]
    )
    ```

    然後這些 key 的長度分別是：

    ```text
    AES-256 key     = 32 bytes
    ChaCha7539 key  = 32 bytes
    ChaCha7539 nonce = 12 bytes
    ```

    得到的 derived 再切成三段：

    ```python
    aes_key    = derived[:32]
    chacha_key = derived[32:64]
    nonce      = derived[64:76]
    ```

    然後就可以用這些資訊寫腳本拿到flag了。

## Flag

```text
v1t{1_am_Gu1lty_0xf_Making.NetAOT:(!}
```
