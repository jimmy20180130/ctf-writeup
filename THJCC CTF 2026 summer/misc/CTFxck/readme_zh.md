# CTFxck

## 題目描述

I only run CTFuck.

This is the interpreter: https://github.com/pro465/ctfuck/blob/9f343df145455f3c2604bbb79789d0b3aa32c601/src/main.rs

Send your program, end it with a line saying EOF.

`nc chal.thjcc.org 9002`

## 解題思路

`main.rs` 讀完之後語意大概是這樣：`0` / `1` push 一個 bit 到 queue 尾端，`,` 從 stdin 讀 1 個 bit (EOF 當 0)，`:` 把最前面的 bit 複製到尾端，`$` pop 掉最前面的 bit，`.` 輸出最前面的 bit 但不取走 (每 8 個 bit 以 little-endian 湊成一個 byte)，`[a|b]` 看最前面的 bit，是 1 跳第 a 行、是 0 跳第 b 行。另外兩個之後會用到的細節是 queue 空掉時 `.` `$` `:` `[` 會直接中止整個直譯器，還有程式結束時沒湊滿 8 bit 的殘餘會補 0 之後 flush 出去

連上去嘗試了一下，送完程式再送一行 `EOF`，回應只有 `nope` 或什麼都不回。奇怪的是本地驗證過會輸出 `ls` 的程式送上去也是 `nope`，亂試一陣子之後發現他有長度限制，超過 110 字元就直接 `nope`，跟程式輸出什麼無關

壓短之後再測就看得出輸出的用途了，`x=1` 這種 statement 沒報錯代表是 `exec()` 不是 `eval()`，`1/0` 回 `nope` 代表例外被 catch 起來印 `nope`，所以程式的輸出會被丟進 python 執行，這才是真正的目標。`print(dir())` 剛好 12 bytes (104 字元) 塞得下，回 `['__builtins__']`，確認是 `exec(out, {"__builtins__": builtins})`

所以問題變成用 110 個字元的 CTFuck 印出一段有意義的 Python。每個 bit 寫 `1.$ ` 是 32 字元/byte，run-length 的 `1....$` 大約 17 字元/byte，都不夠。真正能用的是 queue dump loop，第一行把整個 payload 的 bit 一個字元一個 bit 全部 push 進 queue，第二行 `.$[2|2]` 印一個、pop 一個、跳回自己，不需要計數器或終止符，因為 queue 空掉時 `.` 會直接中止直譯器，成本壓到 8 字元/byte + 8

`exec(input())` 是 13 bytes，而它最後一個字元 `)` = `0x29`，little-endian 的最高兩個 bit 是 0，結束時的 flush 本來就會補 0，那兩個 bit 可以不寫，`13 * 8 - 2 + 1 (換行) + 7 (loop) = 110` 正好卡在上限。而 `input()` 讀的是 harness 自己的 stdin，也就是 socat 掛上來的我們的 socket，所以 `EOF` 那行之後再送一行 Python 就會被執行

flag 在 `/hereisasupersecretfile/flag.txt`

## Flag

```text
THJCC{h4lt1ng_1s_4_c0ntr0l_fl0w_pr1m1t1v3}
```
