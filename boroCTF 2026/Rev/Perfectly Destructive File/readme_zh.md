# Perfectly Destructive File

## 題目描述

Subject: Urgent - John's computer is acting up again

To whom it may concern,

John said that he downloaded a financial report for this quarter, yet now his computer has a "virus". He says that all of his files suddenly have a weird double extension. Like they all have ".boroCTF" appended onto them.

Can you help figure out what happened? Probably pirating video games again if you ask me.

Thanks, Jill

Note - This challenge does NOT contain any functional malware.

## 解題思路

這個 pdf 他打開來會有一個按鈕，按下去會說 `Ya, I'm not making it that easy.`

接著我嘗試使用 pypdf 來把裡面的 object 全部拿出來，之後就看到一串 `Ym9yb0NURnswbjFfRiFsZV9JNV9AMTFfaXRfdEFrZSR9`，base64 decode 以後即為 flag

## Flag

```text
boroCTF{0n1_F!le_I5_@11_it_tAke$}
```
