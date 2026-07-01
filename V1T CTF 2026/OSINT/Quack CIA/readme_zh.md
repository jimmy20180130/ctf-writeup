# Quack CIA

## 題目描述

I swear I saw flag.txt in the video, but now it’s redacted—IT MUST BE THE CIA. I SWEAR… BRO, THE CIAAAAAA! https://www.youtube.com/watch?v=65wwer7yXLg

## 解題思路

仔細看 youtube 影片可以看到這行字 `V1t script kiddie tool 326532`

![alt text](image-1.png)

Github 上面查就可以看到一個 [repo](https://github.com/tommypony326532/cia)

![alt text](image-2.png)

上面的 flag 被替換掉了，把他 git clone 下來可以看到有一個 `.flag.txt.un~`，也[可以去這裡看](https://github.com/tommypony326532/cia/blob/178b58ed916506407b5221c81beb3f81a3264964/.flag.txt.un~)

![alt text](image.png)

base64 decode 以後即為 flag

## Flag

```text
v1t{t0mmy_scr1pt_k1dd13_1n1t}
```
