# Fast Reactions

## Description

Need higher WPM? Try monkeytype.

```text
nc tnkemaq46125.boroctf.com 56354
```

## Solution Walkthrough

After connecting to the server, it displays:

```text
Please enter 0xe6 characters!
```

The length changes every time, and if you don't enter the specified length immediately, it returns "Too slow!" and you cannot get the flag.

So, I wrote a script to automatically input the data and capture the flag.

## Flag

```text
boroCTF{Hum@n1y_im7o5s!ble}
```
