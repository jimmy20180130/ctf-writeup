# NoNo

## 題目描述

Our SOC pulled the HTTP logs off chal.thjcc.org after an alert fired overnight. Find the secret message within these logs :)

## 解題思路

在 `nginx-access.ndjson` 中可以看到以下的東西，發現 `/s3cr3t/rep0rt` 很可能是藏了什麼線索

```json
{"@timestamp": "2025-08-15T03:13:02Z", "event.dataset": "nginx.access", "source.ip": "10.0.2.15", "destination.ip": "172.67.74.226", "url.domain": "chal.thjcc.org:50000", "http.request.method": "GET", "url.path": "/s3cr3t/report", "url.original": "/s3cr3t/report", "url.full": "http://chal.thjcc.org:50000/s3cr3t/report", "http.response.status_code": 404, "http.response.body.bytes": 76, "user_agent.original": "Mozilla/5.0", "message": "10.0.2.15 - chal.thjcc.org:50000 \"GET /s3cr3t/report HTTP/1.1\" 404 76"}
```

使用假設法假設 flag 在 http://chal.thjcc.org:50000/s3cr3t/report，然後假設錯了，頁面顯示 404

之後繼續找，發現 `url.domain` 除了有 `chal.thjcc.org:50000` 也有 `internal.portal`，且 `internal.portal` 的路徑是 `/s3cr3t/rep0rt`，又因為他們的 `destination_ip` 都是 `172.67.74.226`，所以訪問 http://chal.thjcc.org:50000/s3cr3t/rep0rt 即可看到 flag

## Flag

```text
THJCC{f0ll0w_th3_str34m_2_th3_h1dd3n_r3p0rt}
```
