# The Crawler's Courtesy

## 題目描述

The marketplace tried to politely hide one operator scrap from search engines. Courtesy files are not access control, and crawlers are not the only ones who can read them.

## 解題思路

看 `/robots.txt` 可以發現一個隱藏路徑

```text
User-Agent: *
Allow: /
Disallow: /operator-cache-drop
```

進到 `/operator-cache-drop` 以後即可得到 flag

## Flag

```text
bitflag{r0b0ts_4r3_n0t_4_s3cr3t_v4ult}
```
