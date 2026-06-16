# Lazing Around

## 題目描述

Get back to work!

## 解題思路

從題目下載下來的 chal 用 file 查看以後發現是一個 ext4 filesystem data，，接著 mount 以後可以看到裡面有 `entry_log` 以及 `exit_log` 等 txt file，裡面均沒有 flag (其中 mnt.zip 是我把這些 log 全部包成一個 zip 檔案)

我們知道 ext4 的 block size 通常是 4096 bytes，而查看了每個 log，他們的大小都小於一個 block，而 ext4 會以 block 為單位分配空間，因此 EOF 到該 block 結尾之間可能存在 file slack

所以推斷這題可能就是把 flag 藏在 slack space 裡面，於是就在 AI 輔助下寫一個 python 腳本，步驟大概是先從 mnt.zip 取得每個 log 的正常內容，接著在 raw image 中搜尋該內容的位置，讀取該檔案 EOF 到下一個 block boundary 之間的資料，去掉尾端的 null byte 後，將非空 slack 依照 image offset 排序拼接，即可得到 flag

## Flag

```text
boroCTF{C0u!D_yo8_cuT_m3_Som4_sL@ck}
```
