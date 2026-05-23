# Rimal Capture

## 題目描述

An incident capture mixes routine traffic with one operator session. The final text was not entered as cleanly as the first pass suggests.

## 解題思路

首先用 Wireshark 開啟封包，可以看到假的 flag

```text
GET / HTTP/1.1
User-Agent: 0xV01D{http_user_agent_is_bait}
```

接著觀察其他封包，可以發現有一批 UDP 封包送往 `31337` port，payload 都以 `HID` 開頭，後面接著 8 bytes 的資料。例如：

```text
HID 00 00 11 00 00 00 00 00
HID 00 00 00 00 00 00 00 00
HID 00 00 12 00 00 00 00 00
```

這種格式很像 USB HID keyboard report。每筆 report 中，第 1 byte 是 modifier，例如 Shift；第 3 byte 開始是 keycode。因此可以把這些 HID report 依照鍵盤對應表轉回實際輸入的字元。

不過題目提示 `final text was not entered as cleanly`，代表不能只把 keycode 直接串起來，還要處理像 Backspace 這類修正輸入的按鍵。HID keyboard 中 Backspace 的 keycode 是 `0x2a`，遇到時需要刪掉目前結果的最後一個字元。
實際觀察以後也可以發現他包含了一個 backspace

```text
hid_backspacx[Backspace]es_are_evidence
```

## Flag

```text
0xV01D{hid_backspaces_are_evidence}
```
