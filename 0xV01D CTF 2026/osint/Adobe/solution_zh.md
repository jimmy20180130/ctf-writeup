# Adobe

## 題目描述

He was just trying to get Adobe Premiere Pro for free. A cracked version. A quick download… nothing unusual.

The installer looked legit. Everything seemed to work fine.

But behind the scenes… something else was installed.

No warnings. No pop-ups. No second chances.

An infostealer silently took control.

Credentials were harvested. Browser sessions were extracted. Sensitive data was exposed.

By the time he realized what happened… it was already too late.

The only thing left behind is a small piece of evidence.

Sometimes the smallest details leave the biggest traces.

🎯 Your Mission

Find the hidden username.

Then track its digital footprint across the internet.

Somewhere along the way, you will uncover leaked data related to a malware infection.

Within that data lies a malicious directory identifier.

⚠️ Submit only the directory identifier (NOT the full path)

Flag Format:

> 0xV01D{GUID}

## 解題思路

用 exiftool 可以看到 author 是 its.fares09  
接著使用 [這個網站](https://www.hudsonrock.com/threat-intelligence-cybercrime-tools) 找

https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username=its.fares09

```json
{
  "message": "This username is associated with a computer that was infected by an info-stealer, all the credentials saved on this computer are at risk of being accessed by cybercriminals. Visit https://www.hudsonrock.com/free-tools to discover additional free tools and Infostealers related data.",
  "stealers": [
    {
      "total_corporate_services": 1,
      "total_user_services": 79,
      "date_compromised": "2025-03-27T00:00:00.000Z",
      "stealer_family": "Vidar",
      "computer_name": "DESKTOP-STFPTF5 (fares)",
      "operating_system": "Windows 11",
      "malware_path": " C:\\Users\\fares\\AppData\\Roaming\\{2433FA03-903D-4A5B-B193-FB971B0015FF}\\tsengine.exe",
      "antiviruses": [
        "Disabled"
      ],
      "ip": "176.29.***.***",
      "top_passwords": [
        "F***********@",
        "f***********2",
        "f**********2",
        "f***********@",
        "F**********2"
      ],
      "top_logins": [
        "f**********@gmail.com",
        "s************@gmail.com",
        "s**********@social-code.shop",
        "a******0",
        "i*********9"
      ]
    }
  ],
  "total_corporate_services": 1,
  "total_user_services": 79
}
```

## Flag

```text
0xV01D{2433FA03-903D-4A5B-B193-FB971B0015FF}
```
