# BlackFrost

## 題目描述

(none)

## 解題思路

用 ida 分析可以看到程式要 `--token`，驗 hash，再跟 `127.0.0.1:31337` 的 C2 對 config，但解 flag 的地方完全不看前面那些，直接逆 `byte_140003080` 那段就好

```c
v35 = 1;
v36 = 38;
do
{
  *((_BYTE *)&v87[1] + v35 + 7) = byte_140003080[v35 - 1] ^ (v36 - 13);
  *((_BYTE *)&NumberOfBytesWritten.wVersion + v35) = v36 ^ byte_140003080[v35];
  v35 += 2;
  v36 += 26;
}
while ( v35 != 35 );
```

key 從 `0x26` 開始，每兩個 byte 加 `0x1A`，偶數位 xor `key - 0xD`，奇數位 xor `key`

## Flag

```text
THJCC{blackfrost_config_recovered}
```
