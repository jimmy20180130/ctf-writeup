# LYKN Corp

## 題目描述

Welcome to our company's internal system. We have just launched a new Onboarding portal for new employees.The system looks very safe and secure, but is it really?

Let's find the secrets hidden inside!

## 解題思路

先去 `robots.txt`，看到了 `/backup`，然而進去會被 403，然而 `/Backup` 他卻不會檔，而且還可以看到一組帳號密碼

```text
Username: tuan.nguyen
Password: Welcome123!
```

用帳號密碼登入以後可以看到 `minh.le@lykn.local` 傳來的信，而且我們可以回信或是轉發之類的。原本以為是 SSTI 或是 XSS 後面有 admin bot 或是其他東西，沒想到最後是 password spraying

所以登出以後帳號用 `minh.le` 密碼用 `Welcome123!`，即可登入並看到 admin 的帳號密碼

```text
Username: admin
Password: Adm1n_S3cur3_P@ss_2026
```

最後用該組帳號密碼登入就有 flag 了

## Flag

```text
LYKNCTF{c3feec4153bd4219b8bacc73be2a6c5c} (dynamic flag)
```
