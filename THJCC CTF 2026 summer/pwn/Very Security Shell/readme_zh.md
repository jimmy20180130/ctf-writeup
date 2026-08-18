# Very Security Shell

## 題目描述

This is a very secure shell. Each time you connect, a randomly generated 16-character printable string will be used as the password to enter.

nc chal.thjcc.org 11039

## 解題思路

程式 strip 過，只有 `main` 跟 `sub_11E9` 兩個函式。`sub_11E9` 是產密碼的，從 `/dev/urandom` 取 16 bytes，每個 `% 94` 對到 stack 上那張 94 字元的表，湊出 16 字元的密碼

```c
  strcpy(v6, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~");
  fd = open(file: "/dev/urandom", oflag: 0);
  if ( fd < 0 || read(fd, buf, nbytes: 0x10u) != 16 )
  {
    perror(s: "urandom");
    _exit(status: 1);
  }
  close(fd);
  for ( i = 0; i <= 15; ++i )
    *(_BYTE *)(i + a1) = v6[buf[i] % 0x5Eu];
  *(_BYTE *)(a1 + 16) = 0;
```

密碼本身沒得猜，問題在 `main` 比較的方式

```c
  sub_11E9(a1: s2);
  while ( 1 )
  {
    puts(s: "Welcome to very security shell");
    puts(s: "please input your password:");
    if ( (unsigned int)__isoc99_scanf(a1: "%16s", s) != 1 )
      break;
    v4 = strlen(s);
    if ( v4 > 0 && strncmp(s1: s, s2, n: v4) == 0 )
    {
      puts(s: "You input the right password, welcome!");
      system(command: "/bin/sh");
      return 0;
    }
    puts(s: "Wrong password.");
  }
```

`strncmp` 的第三個參數是 `strlen(s)`，送多長就只比多長。送 1 個字元的話，只要它等於 `password[0]` 就過，後面 15 個完全不看

而且猜錯只印 `Wrong password.` 就回到迴圈開頭，只有 `scanf` 失敗才會 break，同一條連線可以無限重試

Exploit:

1. 密碼的每個字元一定落在 `sub_11E9` 那張 94 字元表裡
2. 照表一個一個送單字元一定有一個命中 `password[0]`
3. 收到 `You input the right password, welcome!` 就進 shell，`cat flag.txt`

## Flag

```text
THJCC{strnc0mp_1s_n0t_s3cur3}
```
