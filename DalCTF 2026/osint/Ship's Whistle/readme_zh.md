# Ship's Whistle Writeup

## 題目描述
```text
What coordinates was this photo taken at? Flag format is dalctf{\d+.\d{2}_\d+.\d{2}} (i.e., decimal coordinates to 2 decimal places. if the answer is negative coordinates then you need to include the negative '-' symbol).
```

[boat.png](https://dalctf2026.com/files/8a3f1719a11f3cdd728090ac0ad9d7ee/boat.png?token=eyJ1c2VyX2lkIjozMjcsInRlYW1faWQiOjE4MywiZmlsZV9pZCI6NzE1fQ.aiZCvQ.bHiDbywJsanrDLZmCUxiHjd5yfA)

## 解題思路

1. **第一步**：

    船身有明顯的BCFerries標誌，所以我就找到這家船公司的網站。

    https://www.bcferries.com/on-the-ferry/our-fleet

    在這個網頁有這家船公司的船的圖片，於是我發現題目的船應該是這一艘：

    https://www.bcferries.com/on-the-ferry/our-fleet/spirit-of-british-columbia/SOBC

    底下有一個Youtube影片，稍微看一下發現題目給的圖片剛好是0:12的位置，並且有更完整的地理資訊。

    https://www.youtube.com/watch?v=6u9SvhbYVko

2. **第二步**：

    我先打開Google Map，找到這條航道：

    ![alt text](pictures/image.png)

    沿著這條航道找到最有可能的拍攝地點，並用Google Earth確認地形：

    ![alt text](pictures/image-1.png)

    ![alt text](pictures/image-2.png)

    運氣很好，衛星有拍到船的痕跡，標在船的附近就能拿到flag。

    ![alt text](pictures/image-3.png)
    
## Flag

```text
dalctf{48.86_-123.33}
```