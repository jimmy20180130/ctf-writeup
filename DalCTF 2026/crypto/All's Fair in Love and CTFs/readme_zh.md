# All's Fair in Love and CTFs

## 題目描述

Help me decrypt this hidden message! Wrap result in dalctf{}

## 解題思路

這題感覺是 Playfair cipher，但是他給的表缺了第二和第四個字母，所以補完以後長這樣

```text
A B C D E
F G H I K
L M N O P
Q R S T U
V W X Y Z
```

好了以後把密文分組，`CLDYIKMHILSUKCLQBF` -> `CL DY IK MH IL SU KC LQ BF`，並按照規則來解密，即可得到 flag

```text
CL -> AN
DY -> YT
IK -> HI
MH -> NG
IL -> FO
SU -> RT
KC -> HE
LQ -> FL
BF -> AG
```

## Flag

```text
dalctf{anythingfortheflag}
```
