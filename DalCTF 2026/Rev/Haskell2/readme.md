# Haskell2

## Description

My friend's gave me a compiler for the unreleased haskell2. Apparently its easy and cool now! But I did not pay attention in my functional programming class and cannot code in it! Write a program to extract the flag. To have the checker run it, pass the program as base64.

## Solution Walkthrough

First, observing the provided compiler, we can see that it accepts `.hs2` source code files. Next, checking the strings inside the binary using `strings` reveals some key syntax hints:

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

From these error messages, we can infer that the syntax roughly looks like this:

```text
innocuous <variable> <- read file "<filename>"
for each <variable> in <file_variable> tell me <variable>
```

Therefore, we can use the following payload to retrieve the flag:

```text
innocuous f <- read file "flag.txt"
for each line in f tell me line
```

The challenge states that the payload needs to be converted to Base64, so submitting `aW5ub2N1b3VzIGYgPC0gcmVhZCBmaWxlICJmbGFnLnR4dCIKZm9yIGVhY2ggbGluZSBpbiBmIHRlbGwgbWUgbGluZQo=` will do the trick.

## Flag

```text
dalctf{n3w_l&nguAg3_uNl0ck3d}
```
