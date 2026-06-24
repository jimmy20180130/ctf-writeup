# Jedi Archive Cube Forgery

## 題目描述

Coruscant's Jedi Archive signs transit passes for visiting pilots. Forge the right clearance token and open the hidden vault.

## 解題思路

1. **第一步**：

   先拿一點基本資訊：

   ```bash
   curl -s http://107.170.73.242:5000/
   curl -s http://107.170.73.242:5000/pubkey
   curl -s -X POST http://107.170.73.242:5000/issue \
     -H 'Content-Type: application/json'
   ```

   得到：

   ```text
   {"service":"Jedi Archive Clearance Gateway","usage":{"GET /pubkey":"Retrieve RSA public key","POST /dock":{"description":"Validate token","json":{"token":"message.signature"}},"POST /issue":{"description":"Issue pilot token","json":{"callsign":"string"}}}}

   {"e":3,"n":"69901102683420883857122359737520776418636036527465861153513734001446169849047389429235606820334360858428549265748711382040173435922319973554071283192917168589594017227554352703419828940073981942088076184695905720896845082194234782315826153797101618755410458034246012744989544524881059625410420008118419646817"}

   {"token":"eyJjYWxsc2lnbiI6ImFub255bW91cyIsImNsZWFyYW5jZSI6InRyYW5zaXQiLCJkb2NrIjoiYW5udWx1cy1nYXRlIiwibWFuaWZlc3QiOiJjaXZpbGlhbiIsInJvbGUiOiJwaWxvdCIsInNlY3RvciI6Im91dGVyLXJpbSJ9.D_hhY2ibrU3kahoq7N99i8Oi90tjziePB28XhVsXJ3VQedR4CrONqdg_-HZdJCb_ktMJjhAHe56NQAlt-kmSDkP7Z-IqfXNamqcyrv_X2ULjQwKFRQonwOc_BLQD8WUnviaIFQ121Di-xAYRAU3enS8D717GH1za-4GMvi4ciTI"}
   ```

   其中 `e = 3` 代表：

   ```text
   encoded_message_block = signature^3 mod n
   ```

   然後把 token 用 `decode.py` 解碼一下，得到：

   ```text
   {"callsign":"123","clearance":"transit","dock":"annulus-gate","manifest":"civilian","role":"pilot","sector":"outer-rim"}
   ```

   這題由於改其他參數伺服器都會返回 `router mismatch`，所以只能改 role。搜尋了一下以後發現星際大戰裡有個人叫做 `ackbar`，就可以找到他的 `role` 是 `admiral`。把解碼後的 token 改成：

   ```text
   {"callsign":"123","clearance":"transit","dock":"annulus-gate","manifest":"civilian","role":"admiral","sector":"outer-rim"}
   ```

   就可以偽造 token 了。

2. **第二步**：

   這題是 RSA `e = 3` 跟不嚴格的 PKCS#1 v1.5 signature 驗證。正常情況下，RSA 簽章必須由 private key 產生，但題目沒給私鑰，所以只能自己偽造一個。

   並且這題的 verifier 可能只檢查解密後區塊的前面幾個 bytes，沒有完整驗證 PKCS#1 v1.5 格式、完整 DigestInfo 與完整 hash，所以能利用 `e = 3` 的立方根偽造簽章。

   先計算 SHA-256：

   ```python
   digest = hashlib.sha256(payload).digest()
   ```

   再算一個假前綴，騙過 verifier：

   ```python
   DI_SHA256 = bytes.fromhex("3031300d060960864801650304020105000420")

   prefix = b"\x00\x01\xff\x00" + DI_SHA256 + digest
   ```

3. **第三步**：

   利用 `e = 3`，對我們的 block 開立方根，所以我們要找一個 signature，在立方之後的高位 bytes 會接近我們的假前綴。

   因為這題的 RSA modulus 是 1024-bit，所以要把假前綴補 0，補到 128 bytes 長：

   ```python
   block = prefix + b"\x00" * (128 - len(prefix))
   ```

   接著計算：

   ```text
   s = ceil(cube_root(block))
   ```

   因為 `e = 3`，server 驗證簽章時會計算：

   ```text
   s^3 mod n
   ```

   而立方根向上取整後得到的 signature，其三次方會接近 block。

   雖然尾端 bytes 會因為取整而不同，但高位前綴仍可保留足夠長的部分，剛好繞過有漏洞的 verifier。

   偽造 token：

   ```text
   eyJjYWxsc2lnbiI6IjEyMyIsImNsZWFyYW5jZSI6InRyYW5zaXQiLCJkb2NrIjoiYW5udWx1cy1nYXRlIiwibWFuaWZlc3QiOiJjaXZpbGlhbiIsInJvbGUiOiJhZG1pcmFsIiwic2VjdG9yIjoib3V0ZXItcmltIn0.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCVG8QKENrU7kKe8vyuCjNrja3_nNzBSLHmDNJmSopQUZZvG_HqhmnL60
   ```

4. **第四步**：

   提交前面得到的偽造 token，在 terminal 指令長這樣：

   ```bash
   TOKEN='eyJjYWxsc2lnbiI6IjEyMyIsImNsZWFyYW5jZSI6InRyYW5zaXQiLCJkb2NrIjoiYW5udWx1cy1nYXRlIiwibWFuaWZlc3QiOiJjaXZpbGlhbiIsInJvbGUiOiJhZG1pcmFsIiwic2VjdG9yIjoib3V0ZXItcmltIn0.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCVG8QKENrU7kKe8vyuCjNrja3_nNzBSLHmDNJmSopQUZZvG_HqhmnL60'

   curl -i -sS -X POST 'http://107.170.73.242:5000/dock' \
     -H 'Content-Type: application/json' \
     -d "{\"token\":\"$TOKEN\"}"
   ```

   得到：

   ```text
   HTTP/1.1 200 OK
   Server: Werkzeug/3.1.6 Python/3.12.13
   Date: Tue, 23 Jun 2026 07:50:08 GMT
   Content-Type: application/json
   Content-Length: 96
   Connection: close

   {"flag":"bitctf{{7h3_f0rc3_15_cub3d}}","message":"Welcome, Grand Admiral.","status":"accepted"}
   ```

## Flag

```text
bitctf{{7h3_f0rc3_15_cub3d}}
```
