# Tiny

## 題目描述

The tini duck makes the tini rev challenge with the tiniest flag

## 解題思路

用 ida 分析以後可以發現程式長這樣，先讀取使用者的輸入，然後算他們 ascii 的總和 (會存在 v3 裡面)，其中換行字元 (`\n`、`\r`) 不會被計入

```c
v0 = v71;
v1 = sys_read(0, buf, 0x100u);
v3 = 0;
if (v1 > 0)
{
    v4 = v2;
    v5 = v1;
    do
    {
        v6 = *v4++;
        if (v6 != 10 && v6 != 13)
            v3 = v6 + (unsigned int)v3;
        --v5;
    } while (v5);
}
```

接著程式會從 `loc_4001B8` 讀取 227 個 word，並且每個 word 都減掉剛剛算出的總和 v3，把結果寫到另一塊緩衝區

```c
v7 = (__int16 *)&loc_4001B8;
v8 = &v73;
v9 = 227;
do
{
    v10 = *v7++;
    *(_WORD *)v8 = v10 - v3;
    v8 += 2;
    --v9;
} while (v9);
```

這邊可以注意到 `loc_4001B8` 其實是一段加密過的資料，IDA 把它誤判成程式碼，所以反編譯後半段才會出現一堆看起來像垃圾的 `jb` / `jnz` / `add` 指令，那些都可以直接忽略

後半段程式會把解密後的字元當成 RLE (Run-Length Encoding) 資料使用，輸出由 0 和 1 組成的圖案。`loc_40037E` 存的是每一列的 RLE segment 數量，一共有 10 列，每列 140 個字

![alt text](image.png)

每一列會先讀一個字元，用最低 bit 決定起始字元是 '0' 還是 '1'，之後每讀一個 run length 就填入對應數量的字元，並且交替 0/1，一列結束後補上 `\n`，最後用 sys_write 一次輸出

```c
v11 = v72;
v12 = (unsigned __int16 *)&v74;
v13 = (unsigned __int8 *)&loc_40037E;
for (i = 10; i; --i)
{
    v15 = *v13++;               // 這一列的 segment 數量
    v16 = v12 + 1;
    v17 = *v16;
    v12 = v16 + 1;
    v18 = (v17 & 1) + 48;       // 起始字元 '0' 或 '1'
    v19 = v71;
    v20 = 140;                  // 每列 140 個字
    for (j = v15 - 1; j; --j)
    {
        v22 = *v12++;           // run length
        if (v22 > v20)
            v22 = v20;
        v20 -= v22;
        while (v22)
        {
            *v19++ = v18;
            --v22;
        }
        v18 ^= 1u;              // 交替 0/1
    }
    qmemcpy(v11, v71, v19 - v71);
    v24 = &v11[v19 - v71];
    *v24 = 10;
    v11 = v24 + 1;
}
v25 = sys_write(1u, v72, v11 - v72);
v27 = sys_exit(0);
```

到這裡就可以直接把正確的總和 s 算出來，因為每一列固定 140 個字，解密後第一列的 run length 加起來一定是 140；而加密只是每個字元都多加了一個 s，n 個字元就多了 n 個 s

```text
第一列加密字元的總和 = 140 + n * s

s = (第一列加密字元的總和 − 140) / n
```

之後打開程式隨便輸入一個 ascii 總和為 625 的字串例如 `ZZZZZZU` 就可以得到 flag

![alt text](image-1.png)

## Flag

```text
v1t{^}
```
