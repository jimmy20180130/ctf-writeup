# The Trusting Verifier

## Problem Description

Vendors must prove their legitimacy to join the marketplace. Some have discovered the verification process can peek into places it shouldn't. What secrets lie behind the check?

## Solution Walkthrough

On the `/vendor-application` page, you can see that there is a verify feature. Basically, it is very obviously SSRF, because it not only returns whether the verification succeeded, but also returns the content of the target webpage. Also, using `http://127.0.0.1:3000` can successfully show the homepage content.

SSRF means we need to find internal paths. I tried many things like `/flag.txt` and `/flag`, but there was nothing, so I thought I would try `http://169.254.169.254/`. This is the fixed address for IMDS in AWS, and when accessing `http://169.254.169.254/latest/meta-data/`, there really was something there.

Okay, if you have read this far, it might feel very familiar, because this is exactly what `The Upgrade Tunnel` does. This challenge also looks very much like SSRF, so there should be another path.

We still focus our thinking on `http://169.254.169.254/`, because other than that, I could not find any other internal nodes.

This time I found `http://169.254.169.254/latest/user-data`. You can check the [official documentation](https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html).

```json
{
    "success": true,
    "message": "Website verification successful",
    "body": "#!/bin/sh\nexport MARKETPLACE_ENV=ctf\nexport TRUSTING_VERIFIER_FLAG=bitflag{ssrf_1s_4_p4rty_cr4sh3r}\nnode server.js\n"
}
```

## Flag

```text
bitflag{ssrf_1s_4_p4rty_cr4sh3r}
```
