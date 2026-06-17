# Phantom

## 題目描述

We managed to tap the line between Apex Renewable Energy's DMZ and their internal database segment.

Find out what is really governing Apex Energy's internal routing and recover the exfiltrated flag.

Do you get the gist of this challenge?

## 解題思路

用 wireshark 打開以後可以發現有非常多 TCP 封包，且每個的 data 都是 junk_traffic，此外也有 AX4000 的封包，但也都沒意義

接著滑到最底下可以發現 21 筆可疑的封包，仔細看他們雖然都沒正常的 payload，但是 TCP option 裡面的 Timestamps 都不一樣

![alt text](image.png)

提取出來可以得到 `48 45 58 45 69 7e 6c 51 67 1b 44 4e 75 5e 42 19 75 6d 1e 7a 57`，接下來就不知道能幹麻了，問 AI 以後他說可能是被 XOR，所以我用 [cyberchef](https://cyberchef.io/#recipe=From_Hex('Auto')XOR_Brute_Force(1,100,0,'Standard',false,true,false,'')&input=NDg0NTU4NDU2OTdlNmM1MTY3MWI0NDRlNzU1ZTQyMTk3NTZkMWU3YTU3) 的 XOR brute force 以後就得到 flag 了

![alt text](image-1.png)

## Flag

```text
boroCTF{M1nd_th3_G4P}
```
