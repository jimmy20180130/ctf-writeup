# Klaud Code

## 題目描述

Klaud is the hot new AI company, offering their new MAX subscription for only $2,000/month!

You're stuck on the Free tier and broke, and your usage dies right after you say "hi".

Can you find a way to get Klaud Max for free?

https://9zkv6e70cc16.boroctf.com/

## 解題思路

進去這個網站根據題目敘述，是要升級到 Klaud Max，所以不要被網頁上的其他東西干擾了

干擾的東西蠻多的，第一個是 Workspace，可以看 config 以及其他東西，然而他並不會給我們任何 token 或其他有用的資訊

![alt text](image.png)

點進去 workspace 以後看到的文字也都是模板，並沒有實質作用

![alt text](image-1.png)

第二個干擾的東西是 session_jwt，可以看到它的結尾非常奇怪，我一開始是推斷伺服器只會 decode JWT 而不會驗證，但後來發現不管發什麼請求伺服器永遠都會回傳 Set-Cookie，且內容是一樣的

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2FybCIsInJvbGUiOiJ1c2VyIiwidGllciI6ImZyZWUiLCJhZG1pbiI6ZmFsc2UsImlhdCI6MTc4MTUxNzc2Nn0.t-S69_8uL5-3_1n7r0py_v4l1d4t10n_f4k3
```

JWT 的 payload 也沒有意義，把 admin 改為 true 以後伺服器也不會回傳有意義的東西

```json
{
  "user": "Karl",
  "role": "user",
  "tier": "free",
  "admin": false,
  "iat": 1781517766
}
```

![alt text](image-2.png)

第三個干擾的東西是 chat，可以發現不管傳什麼，他永遠只會回應 `I am Klaud (Free Tier). I can assist with basic formatting and general knowledge. Please upgrade to Klaud Max for advanced reasoning.`，我試了很多種組合也都沒用

![alt text](image-3.png)

第四個干擾的東西是 docs 裡面的 `Authentication` 以及 `Legacy V1 Integrations`，他提到 `curl -H "Authorization: Bearer kl_live_..." https://api.klaud.ai/v1/chat`，我一開始認為這是內部節點，但找半天都沒發現可以 SSRF 的地方。而且目前 chat 的 api 節點是 `/api/chat`，我嘗試 `/v1/chat` 和 `/api/v1/chat` 都沒用

干擾的部分說完了，現在就來講到底要怎麼拿到 flag

根據題目的敘述，我們要做的事是拿到 Klaud Max，而他一開始的價格是 2000 元，仔細查看網頁原始碼也可以發現升級成功後就會顯示 flag 了，也可以看到當價格為 0 的時候我們就可以升級成 Klaud Max

![alt text](image-4.png)

![alt text](image-5.png)

此時可以注意到底下有一個 Redeem Credits 的輸入框，裡面的 code 我們目前還不知道是什麼，試了 SQL Injection 等等的都沒用

後來我在 /about.html 裡面看到一個 [youtube 連結](https://www.youtube.com/watch?v=vDFLh16yJL8)，點進去看到最後就可以得到 code 了 (KLAUD20OFF)

![alt text](image-6.png)

![alt text](image-7.png)

用了以後可以發現價格從 2000 變成 1600，接著通靈了許久以後發現不只 KLAUD20OFF 有用，klaud20off 也可以使用，並且也是 20% off，讓價格變成 1200 元

所以我之後繼續嘗試 Klaud20off 和 kLaud20off 等 code，最後成功讓價格變成 0 元，拿到了 flag

![alt text](image-8.png)

## Flag

```text
boroCTF{kl@ud_c0d3d_btw_lol}
```
