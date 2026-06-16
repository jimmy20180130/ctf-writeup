# Broken Promise

## 題目描述

My friend David has been sobbing uncontrollably recently. He even changed his socials to "SandevastedMoonboy".

## 解題思路

查名稱可以找到[這篇文章](https://www.reddit.com/r/Edgerunners/comments/1tneaip/just_finished_cyberpunk_for_the_first_time_i_feel/?tl=pt-br)，點進去連結可以發現一張 moon.jpg，但是用 hex editor 打開以後卻看到有提示說 flag 不在圖片裡面

所以就覺得可能是留言裡面藏了什麼東西，用 [reddit api](https://www.reddit.com/user/SandevastedMoonboy/comments/.json) 查了一下發現真的有藏東西

把 \u200b 當作 0，\u200c 當作 1，每 8 位轉 ASCII，即可得到 flag

## Flag

```text
boroCTF{s0rry_w1sh_w3_c0uld_g0_t0_th3_m00n_t0g3th3r}
```
