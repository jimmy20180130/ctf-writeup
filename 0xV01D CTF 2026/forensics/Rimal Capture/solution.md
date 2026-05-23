# Rimal Capture

## Description

An incident capture mixes routine traffic with one operator session. The final text was not entered as cleanly as the first pass suggests.

## Solution Walkthrough

First, open the packet capture file using Wireshark, where you will spot a fake flag:

```text
GET / HTTP/1.1
User-Agent: 0xV01D{http_user_agent_is_bait}
```

Next, observing the other packets reveals a stream of UDP packets sent to port `31337`. Their payloads all start with `HID`, followed by 8 bytes of data. For example:

```text
HID 00 00 11 00 00 00 00 00
HID 00 00 00 00 00 00 00 00
HID 00 00 12 00 00 00 00 00

```

This format strongly resembles a USB HID keyboard report. In each report, the 1st byte represents the modifier (such as Shift), and the keycodes start from the 3rd byte. Therefore, we can map these HID reports back to the actual typed characters using a keyboard layout lookup table.

However, the challenge hint states that `final text was not entered as cleanly`. This means we cannot simply concatenate the keycodes directly; we also need to handle keystrokes that modify the input, such as Backspace. In HID keyboard reports, the keycode for Backspace is `0x2a`. Whenever this is encountered, the last character of the current result must be deleted.

Upon closer inspection of the data, you can see that it indeed contains a backspace:

```text
hid_backspacx[Backspace]es_are_evidence
```

## Flag

```text
0xV01D{hid_backspaces_are_evidence}
```
