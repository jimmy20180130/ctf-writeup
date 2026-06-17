# Amazing

## Description

Escape is impossible unless you take the right step.

## Solution Walkthrough

Notice the `hope()` function.

```py
def hope():
    sequence = b'...'
    mod = (player_pos[0] ^ (player_pos[1] + player_pos[1])) * player_pos[0]
    try:
        bytes = rsa_encrypt(sequence, mod)

        if len(bytes) == 0:
            return
        object = marshal.loads(bytes)
        impossible = types.FunctionType(
            object, 
            globals(), 
            "impossible"
        )
        impossible()
    except Exception:
        pass
```

Here, a mod is calculated based on the current player's position `player_pos`, and then `rsa_encrypt()` is used to decrypt the sequence.

```py
def rsa_encrypt(data, modulus_length):
    result = bytearray()
    state = modulus_length & 0xFFFFFFFF 
    
    for byte in data:
        state = (1103515245 * state + 12345) & 0xFFFFFFFF
        stream_byte = (state >> 16) & 0xFF 
        result.append(byte ^ stream_byte)
        
    return bytes(result)
```

Therefore, the actual key is `mod = (player_pos[0] ^ (player_pos[1] + player_pos[1])) * player_pos[0]`.

If the player stands at the correct position, the decrypted sequence becomes a valid Python marshaled code object, which is then loaded and executed by `marshal.loads()`. Since the x and y coordinates can only be at most 100, there are at most 10,000 possible combinations. Thus, we can simply brute-force to find which position successfully decrypts into a valid marshal code object.

After execution, you can see a string in the output: `Ym9yb0NURntlczRAcGVfd0E1XzFuZXYhdGFibGV9`. Base64 decoding it yields the flag.

## Flag

```text
boroCTF{es4@pe_wA5_1nev!table}
```
