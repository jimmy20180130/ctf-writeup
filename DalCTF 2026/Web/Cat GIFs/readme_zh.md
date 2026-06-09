# Cat GIFs

## 題目描述

I made a website to store my cat gifs :3

## 解題思路

這題看起來就是 php webshell 的題目，檢查了一下發現他不會檢查副檔名，但是會將上傳後的檔案進行 imagegif()

GIF 本身是 palette-based image，可以有一張 Global Color Table，每個顏色由 3 bytes 的 RGB 組成。而 `imagegif()` 在重新輸出 GIF 時，會保留圖片實際使用到的 palette entries，因此只要把 PHP payload 塞進 palette 裡，再讓圖片的 pixel index 引用到這些顏色，就可以讓 payload 留在輸出的 GIF 檔案中

這裡 payload 長度需要是 3 的倍數，因為 GIF palette 是以 RGB 三個 byte 為一組。putdata(list(range(n))) 則是讓每個 palette entry 都被圖片實際使用到，避免在轉換或重新輸出時被最佳化掉

所以我們要做的是將 php webshell 塞進一個合法的 gif 裡面，並不被 imagegif() 截斷，那就是用 Pillow 建一張 `P` mode 的 GIF，也就是 paletted image，然後把 payload 放進 palette，好了以後上傳完去 `/uploads/shell.php?c=cat%20/flag.txt` 即可看到 flag

## Flag

```text
dalctf{m30w_m3333333000w}
```
