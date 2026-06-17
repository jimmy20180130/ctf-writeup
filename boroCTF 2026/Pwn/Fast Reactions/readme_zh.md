# Fast Reactions

## 題目描述

Need higher WPM? Try monkeytype.

```text
nc tnkemaq46125.boroctf.com 56354
```

## 解題思路

連上伺服器後，會跳出：

```text
Please enter 0xe6 characters!
```

長度每次都會不一樣，而且沒有馬上輸入指定長度的話，會回傳 Too slow!，也沒辦法拿到 flag。

所以我寫了一個腳本自動輸入跟接flag。

## Flag

```text
boroCTF{Hum@n1y_im7o5s!ble}
```
