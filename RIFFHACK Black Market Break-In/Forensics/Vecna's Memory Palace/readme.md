# Vecna's Memory Palace

## Description

After a Hawkins Lab blackout, responders recovered a corrupted memory snapshot. Find the final token to close the incident.

## Solution Walkthrough

```text
=== HAWKINS_LAB_VOLATILE_CAPTURE ===
proc=svchost.exe pid=1948 parent=services.exe
driver=.tmp\mindflayer\resident.sys state=orphaned
radio_tag=UNJX
tv_tag=VAF
clockface=13
DEC0Y_PIPE=Vecna\Clock_One\ringbuffer
noise_0:nInxPHet2cbSHn2yPVL0NCqS
memfrag[4]=UklEPTR8UE9TPTR8U0laRT01M3xCTE9CPTcxNjA3ZDc5N2I2YjdkNzIzMjJmN2U3ZDMxNzA3MTZlMmE2YjYyNzEzZDJmM2IyNDJhMjUw
cache_shadow[0]=UklEPTh8UE9TPTR8U0laRT0xMnxCTE9CPWRlYWRjYWZlYmFiZQ==
noise_1:U054PXwLexPCKEBhiR7xLzJy
memfrag[1]=UklEPTF8UE9TPTN8U0laRT01M3xCTE9CPTY2OTczNmM2NDJlNzgzNDc5MmIyZjY3MmQ3OTZmMmQ3MTdjNjQyYzc3NjY3ZDc5N2E2Njdk
cache_shadow[1]=UklEPTJ8UE9TPTl8U0laRT0xMHxCTE9CPTQxNDE0MTQxNDE=
noise_2:oiYVPQ5rAO3V7GS2Vqy9h1Wl
memfrag[5]=UklEPTV8UE9TPTJ8U0laRT01M3xCTE9CPTNhM2EzMjNhMjIzODNlM2IzYTBjMjYyODMwMjMzZDNkM2IyMTI3MjM2OTY1NmMyMDIwMjA2
noise_3:cc8fSspC/O0rb1rOzSkfa56K
memfrag[0]=UklEPTB8UE9TPTF8U0laRT01M3xCTE9CPWIyMTE3MmQzODJhMmQyYjIxNjYyNTNiMjc2YjYyNzEyYjIwM2EzYjI4MjczNDI2NjM2ZDY5
noise_4:G/BuWOA3uS9HoKXY12jIk5US
memfrag[2]=UklEPTJ8UE9TPTV8U0laRT01M3xCTE9CPWMzYzJlM2MyZTI3NmM2OTZhMTIxNDA0MDYxZTAwNjUwMDFmMDQxMDYzNjI3MTc5NjI2OTM0
noise_5:bQbZGWckADMyJzMrxwhQ9NNp
memfrag[3]=UklEPTN8UE9TPTB8U0laRT01M3xCTE9CPTMzNjMzNjM5M2QyNzM1MjkyMjIzMTQyNzJmM2UyZDYzNmQ2OTI0MjczZDJjMjczYjJhMzAy
diag=heap snapshot complete
analyst_note=fragment metadata survived even when the slab order did not
=== END_CAPTURE ===
```

First, you can see `clockface 13`, which suggests ROT13. After trying all possibilities, I found that `UNJX` -> `HAWK` and `VAF` -> `INS`, so it must be `HAWKINS`.

Next, I sorted the `memfrag` pieces in order, base64 decoded them, and then reordered them according to the `POS` values. As for `noise` and `cache_shadow`, they were useless and just there to mislead.

```text
RID=0|POS=1|SIZE=53|BLOB=b21172d382a2d2b2166253b276b62712b203a3b28273426636d69
RID=1|POS=3|SIZE=53|BLOB=669736c642e7834792b2f672d796f2d717c642c77667d797a667d
RID=2|POS=5|SIZE=53|BLOB=c3c2e3c2e276c696a121404061e0065001f041063627179626934
RID=3|POS=0|SIZE=53|BLOB=336336393d273529222314272f3e2d636d6924273d2c273b2a302
RID=4|POS=4|SIZE=53|BLOB=71607d797b6b7d72322f7e7d3170716e2a6b62713d2f3b242a250
RID=5|POS=2|SIZE=53|BLOB=3a3a323a22383e3b3a0c262830233d3d3b21272369656c2020206
```

After sorting and keeping only the blobs, it looks like this:

```text
336336393d273529222314272f3e2d636d6924273d2c273b2a302
b21172d382a2d2b2166253b276b62712b203a3b28273426636d69
3a3a323a22383e3b3a0c262830233d3d3b21272369656c2020206
669736c642e7834792b2f672d796f2d717c642c77667d797a667d
71607d797b6b7d72322f7e7d3170716e2a6b62713d2f3b242a250
c3c2e3c2e276c696a121404061e0065001f041063627179626934
```

Once sorted, I combined the contents and performed an XOR operation with `HAWKINS` to obtain a JSON string.

```json
{"artifact_name":"mindflayer_loader.dll","campaign":"starcourt_nightshift","sha1":"7f9c2ba4e88f827d616045507605853ed73b809a","unlock_token":"SCOOPS-AHOY-1985"}
```

With this information, I sent it to the server and obtained the flag.

## Flag

```text
bitctf{{v3cn45_m3m0ry_p4l4c3_br34ch}}
```
