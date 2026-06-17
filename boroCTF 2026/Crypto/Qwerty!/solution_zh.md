# Qwerty!

## 題目描述

I am so very sorry.... I made a lot of typos :(

I should rot in hell 😭

?AEAGJ8NJF,\0[d5JcE-

## 解題思路

1. **第一步**：

    題目敘述有提示這是 ROT，但因為密文有很多符號，不是純字母，所以要用能處理 printable ASCII 的 ROT47。

    先 ROT47：

    ```python
    s = r"?AEAGJ8NJF,\0[d5JcE-"

    def rot47(s):
        out = ""
        for c in s:
            x = ord(c)
            if 33 <= x <= 126:
                out += chr(33 + ((x - 33 + 47) % 94))
            else:
                out += c
        return out

    print(rot47(s))
    ```

    會得到：

    ```text
    nptpvyg}yu[-_,5dy4t\
    ```

2. **第二步**：

    這看起來還不像 flag，所以我透過驚人的觀察力發現，如果把每個字元都在鍵盤上左移一格，就會是 flag 了。

    ```text
    n -> b
    p -> o
    t -> r
    p -> o
    v -> c
    y -> t
    g -> f
    } -> {
    ```

    會得到：

    ```text
    boroCTF{typ0_m4st3r}
    ```

## Flag

```text
boroCTF{typ0_m4st3r}
```
