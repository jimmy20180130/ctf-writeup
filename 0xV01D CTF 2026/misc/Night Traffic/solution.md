# Night Traffic

## Description

The provided artifact contains everything needed to recover one valid flag.

Flag format : 0xV01D{......}

Submit the complete flag exactly as shown by the format, including the prefix 0xV01D and the braces.

## Solution Walkthrough

Open it to see part1 ~ part3:

```text
3078563031447b444e.part1.ctf.local
535f4c4142454c535f.part2.ctf.local
4152455f4c4f55447d.part3.ctf.local
```

Concatenate them:  
`3078563031447b444e535f4c4142454c535f4152455f4c4f55447d`

Convert it to ASCII to get the flag.

## Flag

```text
0xV01D{DNS_LABELS_ARE_LOUD}
```
