# Cat GIFs

## Description

I made a website to store my cat gifs :3

## Solution Walkthrough

This question looks just like a PHP webshell challenge. I checked and found it doesn't check file extensions, but it runs `imagegif()` on the uploaded file.

GIF itself is a palette-based image, which can have a Global Color Table where each color is made of 3 bytes of RGB. When `imagegif()` re-outputs the GIF, it keeps the palette entries that are actually used by the image. So, as long as we stuff the PHP payload into the palette and have the image's pixel indices reference these colors, we can keep the payload in the output GIF file.

Here, the payload length needs to be a multiple of 3 because the GIF palette is grouped in 3 bytes of RGB. `putdata(list(range(n)))` is to make sure every palette entry is actually used by the image, avoiding it getting optimized away during conversion or re-output.

So what we need to do is stuff the PHP webshell into a valid GIF without getting truncated by `imagegif()`. That means using Pillow to build a `P` mode GIF—which is a paletted image—and then putting the payload into the palette. Once that's done and uploaded, just go to `/uploads/shell.php?c=cat%20/flag.txt` and you can see the flag.

## Flag

```text
dalctf{m30w_m3333333000w}
```
