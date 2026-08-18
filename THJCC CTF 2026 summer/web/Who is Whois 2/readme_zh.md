# Who is Whois? 2

## 題目描述

Who is Whois? http://chal.thjcc.org:5000/

## 解題思路

首頁有兩個功能，`/whois` 單筆查詢 (POST JSON `{"query": ...}`)，`/batch` 批次查詢 (上傳一個一行一筆的檔案，串流回結果)

`/whois` 會把使用者輸入原封不動當 argv 丟給系統的 `whois`，送 `--version` 就回 `Version 5.5.17.`，代表參數是可以注入的

`whois` 支援 `-h HOST -p PORT OBJECT`，可以連到任意的 host:port 並把 `OBJECT` 當內容送過去，輸入裡的 `\r\n` 也不會被過濾，等於有了一個任意 TCP client

拿它掃 `127.0.0.1` 會發現 port 6379 是沒有認證的 Redis 7.0.15

```text
-h 127.0.0.1 -p 6379 INFO

$5090
# Server
redis_version:7.0.15
```

`ACL WHOAMI` 是 `default`，權限 `+@all` 且不用密碼，但 `CONFIG` / `SAVE` / `BGSAVE` / `SLAVEOF` 都被拿掉了，打過去只回 `unknown command`，改 `dir` / `dbfilename` 寫 RDB 這條路走不通

不過 `MODULE LOAD` 還在

```text
-h 127.0.0.1 -p 6379 "MODULE LOAD a.so"

-ERR Error loading the extension. Please check the server logs.
```

Redis 載 module 是走 `dlopen()`，而 `dlopen()` 在檢查 `RedisModule_OnLoad` 之前就會先跑 `.so` 的 `__attribute__((constructor))`，載入失敗也無所謂，constructor 已經執行了，剩下的問題只有怎麼把 `.so` 寫進磁碟

寫檔的地方是 `/batch`，上傳的檔案會存成 `/tmp/<job_id>`，`job_id` 在串流的第一個事件就回傳

```json
{"type":"upload","job_id":"<uuid>","temporary_path":"/tmp/<uuid>", ...}
```

但 job 一跑完 temp 檔就會被刪掉，所以要想辦法讓 job 跑久一點

batch 的每一行都是獨立的 `whois` argv，所以帶 flag 的行也吃，而 `-h 10.255.255.1 -p 43 x` 連的是不可路由的位址，會卡滿 5 秒的 connect timeout；ELF 內容被 `\n` 切出來的行都是無效的，不計入筆數，於是把檔案拼成這樣

```text
[ solution.so ]
\n-h 10.255.255.1 -p 43 x
\n-h 10.255.255.1 -p 43 x
\n-h 10.255.255.1 -p 43 x
\n-h 10.255.255.1 -p 43 x
```

4 行 × 5 秒約 20 秒 (上限 25 秒 / 20 筆)，temp 檔就能活這麼久，夠另一條連線去發 `MODULE LOAD`

payload 是在 `127.0.0.1:31337` 開一個 bind shell，再用同一個 whois SSRF 連回去下指令，constructor 裡 double-fork 加 `setsid` 跑成獨立 daemon，Redis 之後 `dlclose` 也影響不到

拿到的 shell 是 `redis` 使用者 (uid=100)，跑 `/flag` 就可以拿到 flag 了

## Flag

```text
THJCC{Wh0_15_wH015???WH0_15_wh0_15:D}
```
