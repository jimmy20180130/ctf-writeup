# The Hidden Offer Hunt

## Description

Some offers never appear in the public catalog. Can you find the signal that makes one surface?

## Solution Walkthrough

To be honest, this challenge is a bit guessy. Each product page is located at `/listing/<name>` (e.g., `/listing/loader-laas`). On each product page, there is a `Contact vendor` button. After clicking it and filling out the form, it POSTs the `message` to `/api/contact` using `multipart/form-data`. Note that the form field label says `Message (Markdown/HTML)`, which indicates that the message will be processed as markup.

Then came the "psychic" part. Honestly, when I first saw the challenge title and description, I thought the flag was on some hidden page like `/welcome`, but it wasn't. After a long time of guessing with no results, while solving `The Trusting Verifier`, I thought I needed to make a certain shop have the "trust" tag, so I noticed the following:

You can see that a `Trusted Vendor` gets an extra HTML tag as shown in the image below:

![alt text](image.png)

So, I thought I could try inserting something similar into the contact and operator notes, but it seems it only works within the contact section.

```html
<span class="badge badge-trusted" data-issued-by="riffhack">Trusted Vendor</span>
```

Once that's done, you can see the flag.

![alt text](image-1.png)

## Flag

```text
bitflag{0c34n5_11_c0up0n_h31st}
```
