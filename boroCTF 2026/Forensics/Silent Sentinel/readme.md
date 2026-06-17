# Silent Sentinel

## Description

We intercepted a packet capture containing a mix of modern station telemetry and an anomalous TCP file transfer. Analysts believe the rogue uplink successfully recovered an image of an iconic historical spacecraft where the crime must have taken place originally.

> Flag Format: boroCTF{satellite_name_with_underscores}

## Solution Walkthrough

Open it with Wireshark, and you can see both UDP and TCP traffic. First, follow the UDP packets, but no meaningful data is found; they are all like `{"sensor": "ALT", "altitude_km": 421.9709}`.

Following the TCP stream, you can see a JPG header. Exporting it results in `out.jpg`.

![alt text](image.png)

Finally, using exiftool, you can see that the comment contains the satellite name: `Satellite, Vanguard 1, Backup (A19761019000)`.

## Flag

```text
boroCTF{Vanguard_1}
```
