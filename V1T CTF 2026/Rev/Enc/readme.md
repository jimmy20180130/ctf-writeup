# Enc Writeup

## Description

Oh no, My Flag is gone :<

## Solution Walkthrough

1. **Step 1**：

    After scanning enc.exe with strings, we can see some keywords:

    ```text
    flag.png
    flag.enc
    ChaCha7539Engine
    AES
    PKCS7
    BouncyCastle
    ```

    Therefore, this challenge should be about an image being encrypted with AES and ChaCha7539, then output as a .enc file.

    After finding the function that references flag.png / flag.enc in Ghidra, we can see the general flow:

    ```text
    File.ReadAllBytes("flag.png")
        ↓
    AES encryption
        ↓
    ChaCha7539 encryption
        ↓
    File.WriteAllBytes("flag.enc", ...)
    ```

    Therefore, when decrypting, we need to reverse the process:

    ```text
    flag.enc
        ↓ ChaCha7539 decrypt
    AES ciphertext
        ↓ AES-256-ECB decrypt
    padded PNG
        ↓ PKCS#7 unpad
    flag.png
    ```

2. **Step 2**：

    Find the keys inside the program. However, the program does not directly store the AES key, ChaCha key, and nonce. Instead, it stores two hardcoded hex blobs.

    After recovering them, we get:

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

    Then the program uses SEED_1 to encrypt SEED_2, producing the real keys:

    ```text
    AES-CBC-PKCS7(
        plaintext = SEED_2,
        key       = SEED_1[16:],
        iv        = SEED_1[:16]
    )
    ```

    The lengths of these keys are:

    ```text
    AES-256 key     = 32 bytes
    ChaCha7539 key  = 32 bytes
    ChaCha7539 nonce = 12 bytes
    ```

    The derived data is then split into three parts:

    ```python
    aes_key    = derived[:32]
    chacha_key = derived[32:64]
    nonce      = derived[64:76]
    ```

    Then we can use this information to write a script and obtain the flag.

## Flag

```text
v1t{1_am_Gu1lty_0xf_Making.NetAOT:(!}
```
