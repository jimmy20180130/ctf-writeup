# Aperture Science Test Chambers

## Description

GLaDOS has locked the flag behind twenty Aperture Science test chambers. Each chamber is an illuminated panel grid — pressing any panel toggles it and all its immediate neighbours. Find the sequence of presses that extinguishes every panel in each chamber, and she will release what you've earned.

## Solution Walkthrough

This challenge is a "Lights Out" game. The mechanism is as follows:

There are many light bulbs on a square board; some are on, and some are off. When you click a cell, the bulbs directly above, below, to the left, and to the right of it toggle their state (on turns off, off turns on). Our goal is to find a way to turn off all the bulbs.

After understanding the gameplay, you can refer to solutions found online.

## Flag

```text
bitctf{{gl4d0s_s4ys_y0u_p4ss3d_4ll_ch4mb3rs}}
```
