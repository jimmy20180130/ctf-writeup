# The Crawler's Courtesy

## Description

The marketplace tried to politely hide one operator scrap from search engines. Courtesy files are not access control, and crawlers are not the only ones who can read them.

## Solution Walkthrough

Checking `/robots.txt` reveals a hidden path:

```text
User-Agent: *
Allow: /
Disallow: /operator-cache-drop
```

Accessing `/operator-cache-drop` will yield the flag.

## Flag

```text
bitflag{r0b0ts_4r3_n0t_4_s3cr3t_v4ult}
```
