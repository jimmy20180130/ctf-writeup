# Franklin

## Description

A customized idea by me, about me, with me, for you.

## Solution Walkthrough

After receiving the file, I used `file` to check it and found that `Franklin` is a Truetype font.

So, I used fontforge to take a look, but I couldn't see the flag anywhere, so I later decided to use fontTools.ttx to view it.

I first checked to see if it was hidden in the name table, but it wasn't. After searching, I discovered that the flag was hidden inside the GSUB table.

```xml
<LigatureSet glyph="b">
    <Ligature components="o,r,o,C,T,F,braceleft,f,R,four,n,k,l,one,n,underscore,f,zero,n,seven,braceright" glyph="asterisk"/>
</LigatureSet>
```

## Flag

```text
boroCTF{fR4nkl1n_f0n7}
```
