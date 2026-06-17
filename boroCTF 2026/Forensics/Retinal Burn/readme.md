# Retinal Burn

## Description

My friend Jonas Wagner sent me a challenge but I can't be bothered to do it. He was always one to be working on his own sorts of projects and stuff. You do it.

## Solution Walkthrough

The image says "too bright", so I adjusted it with PowerPoint. It can be seen that when the contrast is -55%, there is a light blue fake flag and a light yellow true flag directly above the image.

![alt text](image.png)

Then, use PowerPoint's Colors -> Set Transparent Color, choose the light blue color. This will only leave the light yellow true flag.

![alt text](image-1.png)

Next, take a screenshot and set the contrast to -55% again.

![alt text](image-2.png)

Finally, if you still can't see it clearly, go to Insert -> Shapes, select a square, and set its color to the gray of the fake flag. Then, select the screenshot you just took, use PowerPoint's Colors -> Set Transparent Color, and select white. Lastly, move it to the top layer and place it on top of the square to clearly see the flag.

![alt text](image-3.png)

## Flag

```text
BoroCTF{0W_^MY_E7ES!}
```
