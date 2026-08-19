# License

## 題目描述

(none)

## 解題思路

用 ida 分析可以看到前面是一大坨大便，然後可以注意到最後面有解密 flag 的函式，跟 404 那題一樣

阿又非常碰巧解密函式不會需要前面那個 license key 所以直接逆向他即可

```c
v60 = 1;
for ( k = 126; ; k += 26 )
{   // buf[v60 - 1]
    *((_BYTE *)&v66[3] + v60 + 7) = byte_20020F[v60] ^ (k - 13);
    if ( v60 == 31 )
    break;
    buf[v60] = k ^ byte_200210[v60];
    v60 += 2;
}
buf[31] = 0;
v63 = -1;
do
    v4 = buf[++v63] == 0;
while ( !v4 );
sys_write(1u, buf, v63);
sys_write(v64, "\n", 1u);
```

這邊基本上就是解密 flag 的地方，把 `byte_200210` 那 31 bytes 讀出來照著解就好

## Flag

```text
THJCC{license_pipeline_rebuilt}
```
