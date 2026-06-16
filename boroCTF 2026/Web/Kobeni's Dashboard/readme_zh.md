# Kobeni's Dashboard

## 題目描述

Kobeni's been tasked with cataloging devil sighting evidence through Public Safety's new imaging system, but rumor has it that contract information between the Chainsaw Devil & Denji are buried somewhere in the classified archive. Report back your findings.

https://sj20riah2597.boroctf.com/

## 解題思路

這題有提示 `<!-- Processor: see response headers -->`，測試後發現是 ImageMagick，所以往 ImageMagick thumbnail pipeline 的任意檔案讀取去嘗試

所以就做了一個 a.svg，之後便成功得到 flag.png，再調整一下 y 軸即可得到 flag

## Flag

```text
boroCTF{I'v3_n3v3r_been_T0_sch00l_3ithEr}
```
