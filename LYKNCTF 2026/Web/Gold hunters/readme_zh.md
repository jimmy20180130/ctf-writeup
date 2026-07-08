# Gold hunters

## 題目描述

It looks like they intentionally or unintentionally put some gold in front of your eye. Can you find it?

## 解題思路

可以看到網頁原始碼有這行

```js
window.API_KEY = "Lp1-QNMM-U3I9FKzwQZq3mVFkZATfzCTOQvTr3h9pbA";
```

接著就打，發現 `/api/openapi.json` 有東西

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Contact Portal API",
    "version": "0.1.0"
  },
  "paths": {
    "/api/contact": {
      ...
    },
    "/api/get-flag": {
      "get": {
        "summary": "Get Flag",
        "description": "Well done! You found the hidden flag endpoint.",
        "operationId": "get_flag_api_get_flag_get",
        "parameters": [
          {
            "name": "x-api-key",
            "in": "header",
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
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "title": "Response Get Flag Api Get Flag Get"
                }
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
    }
  },
  "components": {
    ...
  }
}
```

所以就去 `/api/get-flag`，並且加上 `x-api-key: Lp1-QNMM-U3I9FKzwQZq3mVFkZATfzCTOQvTr3h9pbA` 的 header 即可得到 flag

## Flag

```text
LYKNCTF{14b7cf4437404bdea0cb20ff55588d96} (dynamic flag)
```
