# Blackwall Protocol

## 題目描述

We managed to intercept a raw, unfiltered braindance (BD) datastream right before the target crossed the Blackwall. The raw feed is heavily corrupted, but our netrunners swear there's something in the machine.

## 解題思路

可以發現 `bd_tuner.py` 好像沒什麼用，此外用 file 可以發現 `david_last_moments.bd` 是一個 pcap capture file

接著用 wireshark 打開它，裡面的 UDP Stream 只會看到重複的 `ARASAKA_NEURAL_LINK_FRAME` 而已，TCP 的部分則是一個 ext4 filesystem image

嘗試了很久後來發現其實 `bd_tuner.py` 其實是有用的，其中底下這段程式碼似乎是指封包的延遲

```py
delay = random.choice([0.15, 0.65]) # Matches our timing channel delays!
```

去看了一下延遲也正好都差 0.00015 秒或是 0.00065 秒，所以就假設差 0.00015 的為 0，差 0.00065 的為 1，之後 decode 完就是 flag 了

![alt text](image.png)

## Flag

```text
boroCTF{s4nd3v1st4n_gh0st_1n_th3_m4ch1n3_8f92a}
```
