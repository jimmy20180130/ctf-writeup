# 404

## 題目描述

(none)

## 解題思路

用 ida 分析可以發現裡面是一小坨 vm，但注意到這裡

```c
case 7:
    v30 = 53;
    for ( j = 0; j != 32; j += 2 )
    {
        buf[j] = byte_200280[j] ^ (v30 - 13);
        buf[j + 1] = v30 ^ byte_200281[j];
        v30 += 26;
    }
    LOBYTE(v37) = 0;
    v32 = -1;
    do
        v4 = buf[++v32] == 0;
    while ( !v4 );
    sys_write(1u, buf, v32);
    sys_write(v33, "\n", 1u);
    return 0;
```

這邊基本上就是解密 flag 的地方

## Flag

```text
THJCC{vm_bytecode_is_a_contract}
```
