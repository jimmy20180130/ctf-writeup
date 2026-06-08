# War Chants

## 題目描述

My friend Carlos sent me this "war chant" audio, but I swear there was supposed to be a video with it. Can you help me find where was it recorded? The flag will be the name of the location where it was recorded separated by underscores in the format DalCTF{place_of_recording} (for example, DalCTF{wanderer_grounds} if it was recorded in the Wanderer Grounds stadium in halifax)

## 解題思路

拿到音檔以後我因為聽不懂葡萄牙文，所以就去找一個工具把歌詞提取出來 (大概是 `vamo que vamo meu inter`)，接下來去 google 搜尋，因為題目有說他是一段影片

![alt text](image.png)

接著我就找到了[一段 instagram 影片](https://www.instagram.com/reels/DVEFLE1kbSN/)，可以看到影片上方有一段文字

![alt text](image-1.png)

以圖搜圖以後可以看到[在類似地點拍的影片](https://www.tiktok.com/@gauchaesportes/video/7614961056774884628)，同時也提供了更多資訊，所以可以推斷出影片主題是 2026 Gauchão 決賽 Gre-Nal 前，訪問 Inter 球迷的影片

好所以可以推斷很明顯應該就是在他們主場附近 (我用主場當 flag 結果是錯的)，用 `Beira-Rio nearby park` 查了一下發現[一個網站](https://www.tripadvisor.com/AttractionsNear-g303546-d2365562-Estadio_Beira_Rio-Porto_Alegre_State_of_Rio_Grande_do_Sul.html)介紹附近的景點，其中 `parque marinha do brasil` 就在裡面

## Flag

```text
DalCTF{parque_marinha_do_brasil}
```
