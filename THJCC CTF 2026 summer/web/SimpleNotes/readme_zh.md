# SimpleNotes

## 題目描述

`chal.thjcc.org:31289`

A plain-text notes app. Flag is at /flag.txt.

## 解題思路

簡單測試，`GET /api/notes` 列出筆記檔名，`GET /api/read?f=<name>` 回檔案內容

`f` 一看就是 path traversal，但 `../flag.txt` 直接回 `u are blocked XD`

一次測一個 pattern 掃出來的黑名單是：`..`（任何位置）、開頭的 `/`、`%2e`、`%2f`、`%5c`、`%00` 都擋，`a/b` 這種不在開頭的 slash、單一個 `.`、`%25` 都放行，它同時檢查原始字串跟解一次碼之後的字串，所以 `%252e` 本身不含 `%2e` 也一樣被擋

關鍵是把已知檔名雙重編碼送過去還是讀得到

```text
$ curl "http://chal.thjcc.org:31289/api/read?f=%2572amen.txt"
中山站拉麵清單
```

所以可以合理推測 `%2572amen.txt` -> Tomcat 解一次 -> `%72amen.txt` -> 程式自己又解一次 -> `ramen.txt`

然後之後怎麼試都解不出來，後來問 AI，請他找這方面的 CVE 之類的，他就給了下面這個的解法

```java
int v = Integer.parseInt(s, i + 1, i + 3, 16);
```

`Integer.parseInt` 用 `Character.digit()` 判斷數字，而它不限 ASCII，全形也吃：`２` 是 2、`ｅ` 是 14、`ｆ` 是 15。也就是 `%２ｅ` 會被解成 `.`、`%２ｆ` 會被解成 `/`，但字串裡完全沒有 ASCII 的 `%2e` 和 `%2f`，黑名單的字串比對抓不到，然後因為好像沒辦法用絕對路徑，所以就改用相對路徑

## Flag

```text
THJCC{inspired_by_blackhat_asia_2026}
```
