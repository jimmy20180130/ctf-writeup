# LYKN Corp

## Description

Welcome to our company's internal system. We have just launched a new Onboarding portal for new employees.The system looks very safe and secure, but is it really?

Let's find the secrets hidden inside!

## Solution Walkthrough

First, I went to `robots.txt` and saw `/backup`. However, accessing it resulted in a 403 error. But, it does not block `/Backup`, and I was able to see a set of credentials there:

```text
Username: tuan.nguyen
Password: Welcome123!
```

After logging in with the username and password, I could see an email from `minh.le@lykn.local`, and we have the ability to reply or forward it. I originally thought it was SSTI or XSS involving an admin bot or something else, but it turned out to be password spraying.

So, after logging out, I used the username `minh.le` and the password `Welcome123!` to log in, which allowed me to see the admin's username and password:

```text
Username: admin
Password: Adm1n_S3cur3_P@ss_2026
```

Finally, logging in with those credentials provided the flag.

## Flag

```text
LYKNCTF{c3feec4153bd4219b8bacc73be2a6c5c} (dynamic flag)
```
