# Kobeni's Dashboard

## Description

Kobeni's been tasked with cataloging devil sighting evidence through Public Safety's new imaging system, but rumor has it that contract information between the Chainsaw Devil & Denji are buried somewhere in the classified archive. Report back your findings.

https://sj20riah2597.boroctf.com/

## Solution Walkthrough

This challenge gives a hint: `<!-- Processor: see response headers -->`. After testing, it turned out to be ImageMagick, so I tried targeting the ImageMagick thumbnail pipeline for arbitrary file readout.

Therefore, I created an `a.svg` file and successfully obtained `flag.png`. After adjusting the Y-axis slightly, I got the flag.

## Flag

```text
boroCTF{I'v3_n3v3r_been_T0_sch00l_3ithEr}
```
