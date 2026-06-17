# Broken Promise

## Description

My friend David has been sobbing uncontrollably recently. He even changed his socials to "SandevastedMoonboy".

## Solution Walkthrough

Searching the name leads to [this post](https://www.reddit.com/r/Edgerunners/comments/1tneaip/just_finished_cyberpunk_for_the_first_time_i_feel/?tl=pt-br). Clicking the link reveals a moon.jpg, but opening it with a hex editor shows a hint that the flag is not in the image.

Therefore, I suspected that something was hidden in the comments. Using the [reddit api](https://www.reddit.com/user/SandevastedMoonboy/comments/.json) to check, I discovered something was indeed hidden there.

By treating \u200b as 0 and \u200c as 1, and converting every 8 bits to ASCII, the flag can be obtained.

## Flag

```text
boroCTF{s0rry_w1sh_w3_c0uld_g0_t0_th3_m00n_t0g3th3r}
```
