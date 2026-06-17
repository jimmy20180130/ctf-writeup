# The Shattered Needle

## Description

Man I hate haystacks. Where is my needle!!!

## Solution Walkthrough

You can see that there are 100 folders in the compressed file, from `dir_1` to `dir_100`. Inside each of these folders, there are another 100 folders, from `sub_1` to `sub_100`. Inside each of those, there are ten files, from `data_1.txt` to `data_10.txt`.

Searching manually would take too much time, so I wrote a script to scan them, which allowed me to obtain the flag.

## Flag

```text
boroCTF{gr3p_1s_y0ur_b3st_fr13nd_f0r_1nc1d3nt_r3sp0ns3}
```
