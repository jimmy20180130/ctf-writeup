# Klaud Code

## Description

Klaud is the hot new AI company, offering their new MAX subscription for only $2,000/month!

You're stuck on the Free tier and broke, and your usage dies right after you say "hi".

Can you find a way to get Klaud Max for free?

https://9zkv6e70cc16.boroctf.com/

## Solution Walkthrough

According to the challenge description, the goal upon entering this website is to upgrade to Klaud Max, so do not be distracted by other elements on the webpage.

There are quite a few distractions. The first one is the Workspace, where you can view configs and other details; however, it does not provide us with any tokens or other useful information.

![alt text](image.png)

The text seen after clicking into the workspace consists entirely of placeholders and serves no actual purpose.

![alt text](image-1.png)

The second distraction is the `session_jwt`. Its signature ending looks very strange. Initially, I deduced that the server might only decode the JWT without verifying it, but I later discovered that no matter what request is sent, the server always returns the exact same `Set-Cookie` header.

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2FybCIsInJvbGUiOiJ1c2VyIiwidGllciI6ImZyZWUiLCJhZG1pbiI6ZmFsc2UsImlhdCI6MTc4MTUxNzc2Nn0.t-S69_8uL5-3_1n7r0py_v4l1d4t10n_f4k3
```

The JWT payload is also meaningless; modifying `admin` to `true` does not make the server return anything useful.

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

The third distraction is the chat. No matter what you send, it always responds with: `I am Klaud (Free Tier). I can assist with basic formatting and general knowledge. Please upgrade to Klaud Max for advanced reasoning.` I tried many different combinations, but none of them worked.

![alt text](image-3.png)

The fourth distraction involves `Authentication` and `Legacy V1 Integrations` inside the docs. It mentions `curl -H "Authorization: Bearer kl_live_..." https://api.klaud.ai/v1/chat`. I initially thought this was an internal endpoint, but after searching for a while, I couldn't find any place vulnerable to SSRF. Furthermore, the current chat API endpoint is `/api/chat`, and my attempts at `/v1/chat` and `/api/v1/chat` both failed.

Now that the distractions have been covered, let's explain how to actually get the flag.

Based on the challenge description, our goal is to acquire Klaud Max. The initial price is 2000 dollars. A careful inspection of the webpage source code reveals that the flag will be displayed upon a successful upgrade, and it also indicates that we can upgrade to Klaud Max once the price reaches 0.

![alt text](image-4.png)

![alt text](image-5.png)

At this point, you can notice a "Redeem Credits" input field at the bottom. We don't know what the code is yet, and attempts like SQL Injection did not work.

Later, I found a [YouTube link](https://www.youtube.com/watch?v=vDFLh16yJL8) inside `/about.html`. Watching it until the end reveals the code: `KLAUD20OFF`.

![alt text](image-6.png)

![alt text](image-7.png)

Applying it reduces the price from 2000 to 1600. After a long period of trial and error, I discovered that not only does `KLAUD20OFF` work, but `klaud20off` can also be used, which grants another 20% off, bringing the price down to 1200 dollars.

Therefore, I continued trying variations like `Klaud20off` and `kLaud20off`. Eventually, I successfully brought the price down to 0 dollars and obtained the flag.

![alt text](image-8.png)

## Flag

```text
boroCTF{kl@ud_c0d3d_btw_lol}
```
