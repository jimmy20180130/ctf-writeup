# The Trusting Verifier

## 題目描述

Vendors must prove their legitimacy to join the marketplace. Some have discovered the verification process can peek into places it shouldn't. What secrets lie behind the check?

## 解題思路

在 `/vendor-application` 這個頁面可以看到有一個 verify 的功能，基本上就是很明顯的 SSRF 了，因為他不只回覆驗證成不成功，還回覆了目標網頁內容，並且使用 `http://127.0.0.1:3000` 也可以正常看到首頁內容

SSRF 就是要找內部路徑，我找了很多像是 `/flag.txt` 和 `/flag` 等都沒東西，所以想說試試看 `http://169.254.169.254/`，這個東西在 AWS 當中是 IMDS 的固定位址，然後訪問 `http://169.254.169.254/latest/meta-data/` 還真的有東西

好你讀到這裡可能覺得很熟悉，因為這個就是 `The Upgrade Tunnel` 在做的事情，而這個題目看起來也非常 SSRF，所以應該是有另一個路徑

我們思路還是放在 `http://169.254.169.254/`，因為除了他我找不到別的內部節點了

這次找到了 `http://169.254.169.254/latest/user-data`，可以去看[官方說明書](https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html)

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
