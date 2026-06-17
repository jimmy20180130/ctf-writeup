# Franklin

## 題目描述

A customized idea by me, about me, with me, for you.

## 解題思路

拿到以後用 file 看了一下發現 `Franklin` 是 Truetype font

所以就用 fontforge 看了一下，結果都沒看到 flag，所以後來決定用 fontTools.ttx 來看

我先看他會不會在 name 藏，結果沒有，經過搜尋過後，我發現 flag 藏在 GSUB 裡面

```xml
<LigatureSet glyph="b">
    <Ligature components="o,r,o,C,T,F,braceleft,f,R,four,n,k,l,one,n,underscore,f,zero,n,seven,braceright" glyph="asterisk"/>
</LigatureSet>
```

## Flag

```text
boroCTF{fR4nkl1n_f0n7}
```
