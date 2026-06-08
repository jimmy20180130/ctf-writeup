# Haskell2 Writeup

## 題目描述

My friend's gave me a compiler for the unreleased haskell2. Apparently its easy and cool now! But I did not pay attention in my functional programming class and cannot code in it! Write a program to extract the flag. To have the checker run it, pass the program as base64.

## 解題過程

先觀察題目給的 compiler，可以看到它會接受 `.hs2` 原始碼檔案，接著用 `strings` 查看 binary 裡面的字串，可以找到一些關鍵語法提示：

```text
semantic error at line %d: function arguments must be remembered variables
expected a string, number, or variable expression
expected a newline after statement
expected 'that' after 'remember'
expected a variable name after 'remember that'
expected a parameter name after 'of'
expected 'is' after variable name
expected a variable name after 'innocuous'
expected '<-' in monadic file read
expected a string path after 'read file'
expected an iterator name after 'for each'
expected 'in' after iterator name
expected a file binding after 'in'
expected 'tell' in line iterator
source file must use the .hs2 extension
semantic error at line %d: effectful read must be bound before use
semantic error at line %d: file values must be consumed by a line iterator
expected '-' after '<'
unterminated string escape
unexpected character
unterminated string literal
unknown string escape
expected ')' after expression
expected 'me' after 'tell'
that
innocuous
expected 'read' after '<-'
expected 'file' after 'read'
file
expected a statement
expected 'each' after 'for'
each
tell
```

從這些訊息可以推測語法大概是：

```text
innocuous <變數> <- read file "<檔名>"
for each <變數> in <檔案變數> tell me <變數>
```

所以我們可以使用以下的 payload 來得到 flag

```text
innocuous f <- read file "flag.txt"
for each line in f tell me line
```

題目說要把 payload 轉成 base64，於是輸入 `aW5ub2N1b3VzIGYgPC0gcmVhZCBmaWxlICJmbGFnLnR4dCIKZm9yIGVhY2ggbGluZSBpbiBmIHRlbGwgbWUgbGluZQo=` 即可

## Flag

```text
dalctf{n3w_l&nguAg3_uNl0ck3d}
```
