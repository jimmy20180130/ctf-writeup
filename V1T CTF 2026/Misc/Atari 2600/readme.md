# Atari 2600

## Description

Can you get that prize ?

## Solution Walkthrough

The challenge title is Atari 2600, and it provides a bin file, so we can run the game using an emulator.

The dot on the left is the object controlled by the player. If it hits a wall, the game stops. I suspect that reaching the dot in the bottom-right corner will grant the flag; however, it is surrounded by walls, so it is theoretically impossible to beat the game.

![alt text](image.png)

I did some research and used DiStella to generate a `v1t.asm` (because the Windows version had issues, I built it on Linux and ran `./distella -pafs v1t.bas.bin > v1t.asm`).

There are a few ways to solve this: one is to modify the map, and the other is to figure out the logic for printing the flag. I thought modifying the map would be easier because, to be honest, I couldn't really read the `v1t.asm` file. So, I used Stella's built-in debugger to find where the map data is stored.

```text
.\Stella.exe -debug .\v1t.bas.bin
```

After pressing step an unknown number of times, I discovered that the program seems to read data from `Lf48e`, so I investigated whether that was indeed the map.

![alt text](image-1.png)

```text
LF48E: .byte $FF,$FF,$FF,$FF,$80,$00,$00,$80,$80,$00,$00,$80,$80,$00,$00,$80
       .byte $80,$00,$FF,$83,$80,$00,$80,$82,$80,$00,$80,$82,$FF,$FF,$FF,$FF
```

After rearranging it, it can be turned into this:

```text
FF FF FF FF
80 00 00 80
80 00 00 80
80 00 00 80
80 00 FF 83
80 00 80 82
80 00 80 82
FF FF FF FF
```

We can infer that FF represents the ceiling and floor, 80 represents walls, and I'm not sure what 82 and 83 are. Although it doesn't match the full dimensions, I decided to try it anyway. I also inferred that the lines below are the obstacles.

```text
80 00 FF 83
80 00 80 82
80 00 80 82
```

Anyway, after changing it to the following, you can see that half of the walls have been cleared.

```text
FF FF FF FF
80 00 00 80
80 00 00 80
80 00 00 80
80 00 00 83
80 00 00 82
80 00 00 82
FF FF FF FF
```

![alt text](image-3.png)

The method to modify it is to find the original map data in `v1t.bas.bin` and then edit it. I created a Python script for this.

![alt text](image-4.png)

After reaching the dot in the bottom-right corner, you can get the flag.

![alt text](image-2.png)

I later asked an AI why the map size was different, and it told me that the program expands the map after reading it.

## Flag

```text
v1t{0_0}
```
