# George Orwell

## 題目描述

Big Brother says: We're always watching. Your words, no matter how silent, will be heard.

Note - This challenge simulates real malware but contains NO malicious payloads.

## 解題思路

這是一個 windows 執行檔，用 strings 可以發現

```text
Gui, Add, Text, w250 Center, [ WE ARE LISTENING ]
Gui, Show, w300 h100, System Monitor
return
:*:iloveboroctf::
secret := Chr(98) . Chr(111) . Chr(114) . Chr(111) . Chr(67) . Chr(84) . Chr(70) . Chr(123)
secret := secret . Chr(65) . Chr(72) . Chr(75) . Chr(95) . Chr(49) . Chr(115) . Chr(95)
secret := secret . Chr(108) . Chr(73) . Chr(115) . Chr(43) . Chr(101) . Chr(110) . Chr(105)
secret := secret . Chr(52) . Chr(103) . Chr(125)
MsgBox, 64, System Notification, Access Granted!`n`nFlag: %secret%
```

### 解法一

直接輸入 iloveboroctf 即可得到 flag

![alt text](image.png)

### 解法二

secret 就是 flag，把 ascii 轉成 text 即可得到 flag

## Flag

```text
boroCTF{AHK_1s_lIs+eni4g}
```
