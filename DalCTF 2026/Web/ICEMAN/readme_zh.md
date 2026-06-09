# ICEMAN

## 題目描述

Drake's label OVO is days away from dropping ICEMAN — his most guarded project yet. They run a private API for members on the early-access list. You managed to snag a fan account. The vault is locked down tight... or is it?

## 解題思路

進到網站後會到 /graphql，前端提供一個 GraphQL console，並且可以在上方填入 JWT。

一開始先對 GraphQL 做 introspection，發現 schema 中有 Query 與 Mutation，其中 Mutation 提供了 register(username, password) 和 login(username, password)，兩者都會回傳 AuthPayload，而 AuthPayload 內含 token 欄位，因此可以先註冊一個 fan 帳號取得 JWT。

註冊後取得的 JWT payload 如下：

{
  "username": "aaa",
  "tier": "fan"
}

用這個 token 查詢 me 或 label 時，伺服器會回 `OVO membership required. Fan accounts do not have vault access`，代表權限不足

小通靈一下發現 tier 要改為 ovo，所以拿 jwt 去用 john 破解了一下發現 secret 是 iceman。

好了以後 me 就可以正常查詢

```text
{
  me {
    username
    tier
  }
}
```

```json
{
  "data": {
    "me": {
      "tier": "ovo",
      "username": "aaa"
    }
  }
}
```

之後就可以查 unreleased albums 了

```text
{
  label(name: "OVO") {
    name
    artists {
      name
      albums {
        id
        title
        status
        vaultManifest
      }
    }
  }
}
```

```json
{
  "data": {
    "label": {
      "artists": [
        {
          "albums": [
            {
              "id": "1",
              "status": "RELEASED",
              "title": "For All the Dogs",
              "vaultManifest": null
            },
            {
              "id": "2",
              "status": "RELEASED",
              "title": "Some Sexy Songs 4 U",
              "vaultManifest": null
            },
            {
              "id": "9",
              "status": "UNRELEASED",
              "title": "ICEMAN",
              "vaultManifest": "dalctf2026{open-ticket-send-me-ur-fav-song-in-album6}"
            }
          ],
          "name": "Drake"
        }
      ],
      "name": "OVO"
    }
  }
}
```

## Flag

```text
dalctf2026{open-ticket-send-me-ur-fav-song-in-album6}
```
