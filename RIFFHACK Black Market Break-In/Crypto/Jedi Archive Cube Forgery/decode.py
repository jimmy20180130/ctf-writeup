import base64

token = "eyJjYWxsc2lnbiI6IjEyMyIsImNsZWFyYW5jZSI6InRyYW5zaXQiLCJkb2NrIjoiYW5udWx1cy1nYXRlIiwibWFuaWZlc3QiOiJjaXZpbGlhbiIsInJvbGUiOiJwaWxvdCIsInNlY3RvciI6Im91dGVyLXJpbSJ9.Sl6gh28TqsEoAy36aaNh08vV8atpQmKznvIqddz9YUR61qqtgxi-UUcesDqTaIPYe_6dNUbuGVQhnt1KpDSxKtjEdA2HFU7toacn86n59PTef0pebcFhbPXdHAUndOE5t0vZSsw0OjoeAj3Jsvd88YZzFR-qBmtQPnb44nd09Ao"

payload_b64, sig_b64 = token.split(".", 1)

payload_b64 += "=" * (-len(payload_b64) % 4)

payload = base64.urlsafe_b64decode(payload_b64)

print(payload.decode())