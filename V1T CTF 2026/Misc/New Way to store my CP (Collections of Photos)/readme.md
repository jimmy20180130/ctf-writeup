# New Way to store my CP (Collections of Photos)

## Description

Recently, I put all my money into 1xbet and now I'm broke af. I found a good way to store my 36GB CP and I will share u guys below. https://pastebin.com/899yXPGK

## Solution Walkthrough

![alt text](image-2.png)

Clicking on the provided website reveals a text file containing a YouTube link. Furthermore, scrolling to the bottom of this text file, you can see a very sus string: `MY ⁤⁡⁢‌⁣⁡‍‍⁤‌⁤⁡‌⁣⁡‌⁡⁢⁣‌‌‌⁢⁡⁤⁢⁡⁢⁡‌⁡⁤‌⁤⁣‌‌⁡⁤‍⁡‌⁢‍⁡‍⁢⁣‍‌‍⁡‍⁡⁢⁡‍‌‌⁡‍‌‍NEW CLOAK HEHEHE`

Since the string contains "cloak," I went to `https://stegcloak.surge.sh` and entered the string, which resulted in `5h0ut_0ut_t0_Brandon`.

![alt text](image.png)

Seeing the YouTube link mentioned earlier, I recalled [this project](https://github.com/PulseBeat02/yt-media-storage). I downloaded the video from YouTube at **highest quality** (using lower quality will cause it to fail) and used the command `./media_storage decode --input cp.mp4 --output flag.txt --password 5h0ut_0ut_t0_Brandon`.

![alt text](image-1.png)

Afterward, you can see a file full of "Quack," and by scrolling down, you can find the flag.

![alt text](image-3.png)

## Flag

```text
V1T{Quack_Quack_Quack_1_l0ve_Qu4cking_r34l_much_br}
```
