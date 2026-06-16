# Meeting Location

## 題目描述

I've got the network traffic from a well-known athlete. We don't know who the athlete is yet, but we'll address that after we confirm where they are meeting the other party. You know he will pay big bucks if we can get pictures of this athlete and why they are there for him. They're definitely talking in code about a secret meeting place in these packets. Take a look when you have a second. If you can figure out where they are heading, there's 200 boroPoints in it for you. This could be the end of all our suffering if we figure this out.

Note: the flag will NOT be wrapped with boroCTF{}

## 解題思路

先從 ICMP 開始看，可以看到大部分的封包都沒什麼有用的資訊

![alt text](image.png)

然而底下有一堆 payload 都只有 1 byte 的封包，而且還有順序

![alt text](image-1.png)

把那些 payload 串在一起可以得到 `WWFzX01hcmluYV9DaXJjdWl0`， base64 decode 以後可以得到 `Yas_Marina_Circuit`，加上 boroCTF{} 以後即為 flag

## Flag

```text
boroCTF{Yas_Marina_Circuit}
```
