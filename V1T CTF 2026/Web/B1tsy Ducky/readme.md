# B1tsy Ducky

## 題目描述

You need to enter your name then play to able to solve else it gonna error

https://b1tsy.v1t.site/

## 解題思路

This is a small game. Basically, you need to find the item the duck wants, and then go back to the duck.

![alt text](image.png)

You can see that the third room should be the special room, because I cannot reach the duck at all.

![alt text](image-1.png)

Looking at the HTML, we can see that the third room looks like this:

```text
ROOM 3
0,0,0,f,0,g,g,f,0,0,0,0,0,0,0,0
0,0,0,g,0,g,0,g,g,g,g,0,0,0,0,0
0,0,g,0,0,0,0,0,f,0,f,g,d,g,0,0
0,g,d,0,0,0,0,0,0,0,0,0,0,g,g,0
g,f,g,0,a,0,0,0,0,0,a,0,0,0,g,0
g,0,0,a,0,0,0,a,a,0,0,0,0,0,d,0
f,0,a,0,0,0,0,0,0,0,a,0,0,0,g,0
g,g,0,0,0,0,a,0,a,0,0,0,0,0,g,f
0,g,g,0,0,0,0,0,0,0,0,0,a,0,0,g
0,d,0,0,0,a,0,0,0,0,0,0,0,0,g,g
f,g,g,0,0,0,0,0,0,0,a,0,0,0,d,0
g,0,0,0,0,0,0,0,0,0,0,0,0,0,g,0
g,0,0,a,0,0,0,0,a,0,0,0,0,0,g,0
g,f,0,0,0,0,0,0,0,g,d,g,g,g,f,0
0,g,g,0,0,0,f,g,f,g,0,0,0,0,0,0
0,0,0,g,f,g,0,0,0,0,0,0,0,0,0,0
NAME example room copy 2
EXT 4,0 2 4,15
PAL 0
TUNE 2
```

We can infer that `0` represents a place where the player can move freely. So if we modify the map into the version below, we can reach the duck.

```text
ROOM 3
0,0,0,f,0,g,g,f,0,0,0,0,0,0,0,0
0,0,0,g,0,g,0,g,g,0,g,0,0,0,0,0
0,0,g,0,0,0,0,0,f,0,f,g,d,g,0,0
0,g,d,0,0,0,0,0,0,0,0,0,0,g,g,0
g,f,g,0,a,0,0,0,0,0,a,0,0,0,g,0
g,0,0,a,0,0,0,a,a,0,0,0,0,0,d,0
f,0,a,0,0,0,0,0,0,0,a,0,0,0,g,0
g,g,0,0,0,0,a,0,a,0,0,0,0,0,g,f
0,g,g,0,0,0,0,0,0,0,0,0,a,0,0,g
0,d,0,0,0,a,0,0,0,0,0,0,0,0,g,g
f,g,g,0,0,0,0,0,0,0,a,0,0,0,d,0
g,0,0,0,0,0,0,0,0,0,0,0,0,0,g,0
g,0,0,a,0,0,0,0,a,0,0,0,0,0,g,0
g,f,0,0,0,0,0,0,0,g,d,g,g,g,f,0
0,g,g,0,0,0,f,g,f,g,0,0,0,0,0,0
0,0,0,g,f,g,0,0,0,0,0,0,0,0,0,0
NAME example room copy 2
EXT 4,0 2 4,15
PAL 0
TUNE 2
```

![alt text](image-2.png)

However, even after reaching the duck, we still cannot get the flag, because it checks the `referrer` and also checks `!isPlayerTalkingToSpecialDuck()`.

```js
Object.defineProperty(window, "__bdx_17a", {
    configurable: true,
    enumerable: false,
    writable: false,
    value: function () {
        if (!isPlayerTalkingToSpecialDuck()) {
            alert("quack");
            return;
        }

        window.__duckWasmReady.then(function () {
            var room3Block = serializeRoomBlock("3");
            var referrer = document.referrer || "";
            var picked32 = pick32();

            if (!room3Block || !picked32) {
                alert("some thing go wrong go to start again");
                return;
            }

            if (typeof window.duckWasmReveal !== "function") {
                alert("some thing go wrong go to start again");
                return;
            }

            var flag_decrypt = window.duckWasmReveal(referrer, room3Block, picked32);
            if (flag_decrypt === "some thing go wrong go to start again") {
                alert(flag_decrypt);
                return;
            }

            window.flag = flag_decrypt;
            window.close();
        }).catch(function (err) {
            alert("WASM load failed: " + err);
        });
    }
});
```

Change the `referrer` to `https://b1tsy.v1t.site/`, and remove the `!isPlayerTalkingToSpecialDuck()` check. ~~Then we can get the flag~~ Actually, no.

```js
Object.defineProperty(window, "__bdx_17a", {
    configurable: true,
    enumerable: false,
    writable: false,
    value: function () {
        window.__duckWasmReady.then(function () {
            var room3Block = serializeRoomBlock("3");
            var referrer = "https://b1tsy.v1t.site/";
            var picked32 = pick32();

            if (!room3Block || !picked32) {
                alert("some thing go wrong go to start again");
                return;
            }

            if (typeof window.duckWasmReveal !== "function") {
                alert("some thing go wrong go to start again");
                return;
            }

            var flag_decrypt = window.duckWasmReveal(referrer, room3Block, picked32);
            if (flag_decrypt === "some thing go wrong go to start again") {
                alert(flag_decrypt);
                return;
            }

            window.flag = flag_decrypt;
            window.close();
        }).catch(function (err) {
            alert("WASM load failed: " + err);
        });
    }
});
```

After observing more carefully, it turns out that the decryption failed because we had modified `room3`. I used `console.log` to check the result of `serializeRoomBlock("3")`, and it turned out to be the following:

```text
ROOM 3
0,0,0,f,0,g,g,f,0,0,0,0,0,0,0,0
0,0,0,g,0,g,0,g,g,0,g,0,0,0,0,0
0,0,g,0,0,0,0,0,f,0,f,g,d,g,0,0
0,g,d,0,0,0,0,0,0,0,0,0,0,g,g,0
g,f,g,0,a,0,0,0,0,0,a,0,0,0,g,0
g,0,0,a,0,0,0,a,a,0,0,0,0,0,d,0
f,0,a,0,0,0,0,0,0,0,a,0,0,0,g,0
g,g,0,0,0,0,a,0,a,0,0,0,0,0,g,f
0,g,g,0,0,0,0,0,0,0,0,0,a,0,0,g
0,d,0,0,0,a,0,0,0,0,0,0,0,0,g,g
f,g,g,0,0,0,0,0,0,0,a,0,0,0,d,0
g,0,0,0,0,0,0,0,0,0,0,0,0,0,g,0
g,0,0,a,0,0,0,0,a,0,0,0,0,0,g,0
g,f,0,0,0,0,0,0,0,g,d,g,g,g,f,0
0,g,g,0,0,0,f,g,f,g,0,0,0,0,0,0
0,0,0,g,f,g,0,0,0,0,0,0,0,0,0,0
NAME example room copy 2
EXT 4,0 2 4,15
PAL 0
TUNE 2
```

So replacing `0,0,0,g,0,g,0,g,g,0,g,0,0,0,0,0` with `0,0,0,g,0,g,0,g,g,g,g,0,0,0,0,0` ~~should solve it~~ still does not give us the flag.

After that, I asked AI, and it said this was because the program originally expected the decrypted flag to have a length of 28, but the real flag length was only 26. As a result, it returns `something went wrong`. The solution is to write our own Python script.

## Flag

```text
v1t{b1tsy_t1psy_duck_w4sm}
```
