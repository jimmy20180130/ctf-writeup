# Amazing

## 題目描述

Escape is impossible unless you take the right step.

## 解題思路

注意到 `hope()`

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

這裡會根據目前玩家的位置 player_pos 算出一個 mod，然後用 rsa_encrypt() 對 sequence 做解密。

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

所以真正的 key 就是 `mod = (player_pos[0] ^ (player_pos[1] + player_pos[1])) * player_pos[0]`

如果玩家站在正確的位置，sequence 解密後會變成一個合法的 Python marshaled code object，接著被 marshal.loads() 載入並執行，因為 x 和 y 座標最多只能是 100，所以組合最多只有 10000 種可能，故就直接暴力找出哪個位置可以成功解出合法的 marshal code object 即可

執行完以後可以看到輸出中有一串字串 `Ym9yb0NURntlczRAcGVfd0E1XzFuZXYhdGFibGV9`，把他 base64 decode 以後即為 flag

## Flag

```text
boroCTF{es4@pe_wA5_1nev!table}
```
