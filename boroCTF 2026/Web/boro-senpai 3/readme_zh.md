# boro-senpai 3

## 題目描述

------------ was an actress. A public figure. Then one day, she wasn't. Her AobaNet account — gone. Her name — scrubbed. The internet forgot she existed. But the internet doesn't actually delete things. Prove she existed.

https://5l24ruh9miuo.boroctf.com/

## 解題思路

可以先觀察 /static/main.js，可以看到有一個隱藏的 api `/api/user/<username>?<window._modFlags.k>=<window._modFlags.v>`，其中 `window._modFlags` 目前我們不知道是什麼

去 404 的頁面滑到最底下即可看到 `window._modFlags` 為 `{k: 'include_deleted', v: 'true'}`

按照題目線索可以猜被停用的帳號是 `mai-sakurajima`，於是去 `/api/user/mai-sakurajima?include_deleted=true` 即可看到 flag

```json
{
  "bio": "Account suspended per user request. Data retained per moderation policy.",
  "deleted_at": "2013/09/01 03:17",
  "display_name": "___________ / ___________",
  "followers": 94211,
  "following": 41,
  "joined": "2011/05/20",
  "location": "Tokyo, Japan",
  "mod_notes": "Soft-deleted 2013-09-01 03:17 JST. Account holder flagged for adolescence syndrome — subject ceased to be perceived by public observers. Deletion requested by management (ref: ticket #AN-20130901-004). Data preserved under internal policy §4.2(c). Do not surface in public search. Mod review pending. -- boroCTF{th@nk_y0u_y0u_d!d_w3ll_!_l0v3_y0U<3}",
  "posts": 1337,
  "recent_posts": [
    {
      "date": "2013/08/31 22:55",
      "id": "m-004",
      "text": "みんな、今日も覚えていてくれてありがとう。"
    },
    {
      "date": "2013/08/30 18:20",
      "id": "m-003",
      "text": "また誰かに無視された。気づいたら独りだった。でも、私はここにいる。"
    },
    {
      "date": "2013/08/28 14:10",
      "id": "m-002",
      "text": "撮影の合間にひとりでカフェに来た。誰も気づかない。"
    },
    {
      "date": "2013/08/25 09:44",
      "id": "m-001",
      "text": "消えていくような気がする。でも消えたくない。"
    }
  ],
  "status": "deleted",
  "username": "mai-sakurajima"
}
```

## Flag

```text
boroCTF{th@nk_y0u_y0u_d!d_w3ll_!_l0v3_y0U<3}
```
