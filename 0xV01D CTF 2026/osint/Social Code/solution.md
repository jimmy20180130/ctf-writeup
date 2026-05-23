# Social Code

## Description

Before Kali Team… there was another project.

A small online store called "Social-Code".

The store disappeared. The website is no longer online.

A billing invoice related to this project has been recovered. However, some details were lost during transfer.

but nothing truly disappears from the internet.

Your mission is to travel back in time,

find the archived version of the website,
locate the Instagram logo displayed on the homepage,
and extract the exact file name of that image.
⚠️ Only submit the image file name, including the extension.

Flag format:

> 0xV01D{filename.png}

Author: [F4R3S](https://instagram.com/fares_almahsery)

## Solution Walkthrough

Based on the challenge description, we can see that it is a shop named "social-code".

I referred to [this website](https://www.collegesidekick.com/study-docs/16331200) and found that a standard 3-letter domain extension (such as `.org`) looks like the receipt shown in the image below:

Upon closer inspection of the image provided in the challenge, the letter "D" is shifted back by one position. This indicates that the domain extension should be `.shop` instead of other common ones like `.com`.

Next, I searched for it on the [Wayback Machine](https://web.archive.org/web/20250329141912/http://social-code.shop/) and was able to find the image name.

## Flag

```text
0xV01D{1_c15cd605-362b-4f64-91f0-085ad2805b3f.png}
```
