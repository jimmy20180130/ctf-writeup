# Because There is no one Make Reverse So I Create This Chal

## 題目描述

(none)

## 解題思路

用 ida 分析可以發現他要先輸入 flag 然後程式會驗證他對不對

`start()` 裡面沒有直接比對，而是有以下的邏輯

```c
v9 = (v5 >> 3) - 1344675008;
v10 = 507523160;
v11 = 32;
v12 = -1640531527;
do
{
  v9 += (v8 + *(_DWORD *)&v39[4 * (v8 & 3)]) ^ (((16 * v10) ^ (v10 >> 5)) + v10);
  v8 -= 1640531527;
  v10 += (((16 * v9) ^ (v9 >> 5)) + v9) ^ (v12 + *(_DWORD *)&v39[4 * ((v12 >> 11) & 3)]);
  v12 -= 1640531527;
  --v11;
}
while ( v11 != 0 );
v4[v5] = v9 ^ byte_100000B98[v5];
```

這段拿去問 ai 得知是 xtea，然後 key 是 `sub_100000AB0`

```c
*result = 629208321;
result[1] = -778772443;
result[2] = -1622618389;
result[3] = 88641190;
```

所以整段就是拿 `(block_index - 1344675008, 507523160)` 當 plaintext 去加密，產生的東西再跟 `byte_100000B98` XOR

解出來的東西丟給 `sub_1000008DC`，這是一顆小 VM。看 switch 可以整理出 opcode

| opcode | 行為 |
| --- | --- |
| `0x97 imm` | `idx = imm` |
| `0x86` | `acc = idx < len ? input[idx] : 0` |
| `0x15 imm` | `acc ^= imm` |
| `0x18 imm` | `acc += imm` |
| `0xE5 imm` | `acc -= imm` |
| `0x74 imm` | `acc = rol8(acc, imm & 7)`，imm 必須是 1~7 |
| `0x8F imm` | `fail \|= imm ^ (uint8)acc` |
| `0xCD imm` | `fail \|= len ^ imm` |
| `0x5B imm` | 跳過後面 imm bytes (垃圾資料) |
| `0x5A` | halt，回傳 `fail == 0` |

`fail` 只有 OR 沒有分支，所以不能一個 byte 一個 byte 爆破；不過也不需要，因為每個字元的運算都是可逆的：`0x97` 指定位置、`0x86` 把該位置的字元讀進來、中間幾個 `xor/add/sub/rol`、最後 `0x8F` 跟常數比對。從 `0x8F` 的常數往回推就直接得到明文

好然後這題 ai assist 解花了十幾分鐘吧，如果直接串 ida pro mcp 的話 claude opus 5 只花了一分五十三秒就解出來了

## Flag

```text
THJCC{1_w0nd3r_h0w_l0n6_41_50lv35_17_>w<}
```
