# 78CT

## Description

Rawr and I used to spend hours at a lake right in the heart of our hometown during high school. It was our favorite spot to chill and just clear our minds when the afternoon breeze rolled in after those endless school days. There is also something interesting nearby. If you take a closer look from above, you might notice that a park next to the lake has a shape that resembles a dragon. Can you find the place and figure out what I left behind at the lake?

## Solution Walkthrough

First, use Google Translate to translate "越南 龍公園" to "Công viên Rồng Việt Nam", then search for it. You can see [this website](https://nguoiquansat.vn/cong-vien-rong-nha-ngoc-o-mien-trung-viet-nam-rong-gan-60-000m2-co-den-5-cay-cau-108935.html).

![alt text](image.png)

Use "Công viên ‘rồng nhả ngọc’" to search on Google Maps to find the location in the image.

![alt text](image-1.png)

Next, click on nearby attractions, and you can see a very sus comment in ``.

![alt text](image-2.png)

```text
traVelers MAjESTIC reFlections sUrface LAKeSIDE sh1mering ScENERY AMAzING eXpanse lak3front glImmering BREEzES suNlit harGor ExPLORERS DREAMsCAPE LAKeVIEW riVerside 9 CALMsNESS harMor higHway hazY AMAzINGLY eXplore MAzEWORK BROAdWAY HARBoR sunMist tranTquil loVely OFfERS ARcHITECTS gleaminG MEADOwS harb0r skYline HAzE suNset 9
#v1tnamese
```

Extract the special characters from the comment. For example, extract `V` from `traVelers` and `j` from `MAjESTIC`. Afterward, you will get a base64 encoded string: `VjFUe1czX3IzNGxseV9sMHYzXzdoMTVfcGw0YzN9`. Decode it to get the flag.

## Flag

```text
V1T{W3_r34lly_l0v3_7h15_pl4c3}
```
