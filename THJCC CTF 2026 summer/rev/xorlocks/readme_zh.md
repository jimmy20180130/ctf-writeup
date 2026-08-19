# xorlocks

## 題目描述

(none)

## 解題思路

用 ida 分析可以看到前面會驗密碼，但那些不重要，可以注意到這題和 404 以及 License 一樣，解 flag 的地方不會看前面的密碼或是啥的，所以直接逆向他解密的函式即可

```c
v9 = 1;
for ( j = 64; ; j += 26 )
{
    buf[v9 - 1] = byte_20016F[v9] ^ (j - 13);
    if ( v9 == 31 )
    break;
    buf[v9] = j ^ byte_200170[v9];
    v9 += 2;
}
buf[31] = 0;
v20 = -1;
do
    v4 = buf[++v20] == 0;
while ( !v4 );
sys_write(1u, buf, v20);
sys_write(v21, "\n", 1u);
return 0;
```

## Flag

```text
THJCC{xor_basics_are_not_magic}
```
