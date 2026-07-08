# Migrant

## Description

The company currently changed their brand identity, and all staff must migrate their accounts to this new website. But... something is off with the transfer function.

## Solution Walkthrough

This problem should be in the crypto category 🥀

After entering, you receive a v1 migration token `u4TlwTsu32US4uDJlfeEx/SvQVYKyyv4/FxepRUjSuIjH+8h6MDy9GuvXj+WOdR/o4bDgoQLPGvNKiROynO5ig==`. Taking it to the migration endpoint returns whether it was successful, and the role is `user`.

```json
{
  "message": "Migration successful.",
  "profile": { "role": "user", "user": "guest", "v": "1.0" }
}
```

The token, when base64 decoded, is exactly 48 bytes = three 16-byte blocks. With no MAC and full client control, it can be inferred that this is AES-CBC ciphertext (the first block is the IV). This leads to the idea of a padding oracle.

A padding oracle is typically used to decrypt someone else's ciphertext, but since the goal here is to change yourself into an `admin`, the most useful technique is its reverse operation — **padding oracle encryption**: using the oracle to generate valid ciphertext that decrypts to "arbitrary plaintext we specify," working backward from the last block.

1. For each plaintext block, fix the subsequent ciphertext block `C_next`. Use the padding oracle to restore the intermediate value `I = Dec(C_next)` byte by byte (brute-forcing 256 possibilities per position, determined by whether an `invalid padding` error occurs).
2. Set `C_prev = I XOR plaintext_block`, which guarantees `Dec(C_next) XOR C_prev == plaintext_block`. This block will decrypt to the plaintext we want.
3. For the last block's `C_next`, set it to all zeros (or pick any known ciphertext block) and work backward, prepending the calculated `C_prev` to construct the valid ciphertext.

The forged plaintext only needs to contain the role; the server does not validate `user` or `version`. Simply use the shortest string `{"role":"admin"}`, padded to 16 bytes. The resulting ciphertext is only 3 blocks long (including the trailing all-zero block), requiring 1/4 fewer oracle queries than inserting a full profile. Send this back to `/api/migrate`; the server decrypts it, the padding passes, it reads `role=admin`, and the account is migrated to admin, granting the flag.

## Flag

```text
LYKNCTF{f740972d47ad47aebaf3a5cafe0853f3} (dynamic flag)
```
