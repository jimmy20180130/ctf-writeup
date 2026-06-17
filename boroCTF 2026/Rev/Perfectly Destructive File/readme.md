# Perfectly Destructive File

## Description

Subject: Urgent - John's computer is acting up again

To whom it may concern,

John said that he downloaded a financial report for this quarter, yet now his computer has a "virus". He says that all of his files suddenly have a weird double extension. Like they all have ".boroCTF" appended onto them.

Can you help figure out what happened? Probably pirating video games again if you ask me.

Thanks, Jill

Note - This challenge does NOT contain any functional malware.

## Solution Walkthrough

When you open this PDF, there is a button that, when clicked, says `Ya, I'm not making it that easy.`

Next, I tried using pypdf to extract all the objects inside, and found a string: `Ym9yb0NURnswbjFfRiFsZV9JNV9AMTFfaXRfdEFrZSR9`. After decoding it from base64, I obtained the flag.

## Flag

```text
boroCTF{0n1_F!le_I5_@11_it_tAke$}
```
