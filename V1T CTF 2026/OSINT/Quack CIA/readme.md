# Quack CIA

## Description

I swear I saw flag.txt in the video, but now it’s redacted—IT MUST BE THE CIA. I SWEAR… BRO, THE CIAAAAAA! https://www.youtube.com/watch?v=65wwer7yXLg

## Solution Walkthrough

Carefully watching the YouTube video, you can see the line `V1t script kiddie tool 326532`.

![alt text](image-1.png)

Searching on GitHub, you can find a [repo](https://github.com/tommypony326532/cia).

![alt text](image-2.png)

The flag above was replaced. If you `git clone` it, you can see a `.flag.txt.un~` file; you can [also view it here](https://github.com/tommypony326532/cia/blob/178b58ed916506407b5221c81beb3f81a3264964/.flag.txt.un~).

![alt text](image.png)

After base64 decoding, you get the flag.

## Flag

```text
v1t{t0mmy_scr1pt_k1dd13_1n1t}
```
