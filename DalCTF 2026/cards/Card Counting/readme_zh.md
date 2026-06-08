# Card Counting

## 題目描述

Try your luck at our card counting mini-game! Get through every level to earn youself the flag!

## 解題思路

進到網站後可以發現他遊戲開始時都會跟伺服器取得 seed，而且 seed 好像跟生牌非常有關聯，於是就開始分析他前端的 js 程式碼

首先是分析他有幾輪，以及每一輪有幾張牌，可以先發現當按下開始遊戲時，會呼叫 `z()`，`z()` 裡面的 `U()` 是取得 seed，遊戲的整個邏輯都在 `B()` 裡面

```js
document.getElementById("start_button").addEventListener("click", async () => {
    q.D = false;
    document.getElementById("start_section").classList.add("hidden");
    z()
});

async function z() {
    b = 0;
    F = await U();
    B()
}
```

可以看到 `B()` 裡面有使用 `R[b](k);`，其中 Array `R` 裡面的每個東西都是函式，而且都長得很像，感覺是發牌的邏輯

可以注意到 `[M, y, _, g, p, v, I]` 這幾個函式都有迴圈，分別為 `4, 8, 25, 80, 50, 100, 1000`，且我真人在玩的時候第一關就是發四張牌，故可以推之 `R` 代表每輪會發的牌的數量，而 `e.add()` 和 `t.add()` 等等是發牌的函式

```js
const R = [M, y, _, g, p, v, I];

function M(e) {
    for (let t = 0; t < 4; t++) {
        e.add(t * 1500 + 1e3, 3e3, n, f(.8, .4), t => 1, t => 0)
    }
}
function y(e) {
    for (let t = 0; t < 8; t++) {
        e.add(t * 1500, 1500, t % 2 == 0 ? d : m, (t >> 1) % 2 == 0 ? d : m, w, t => 0)
    }
}
function _(t) {
    for (let e = 0; e < 25; e++) {
        t.add(e * 500, 1500, t => (e * .2 + .1) % 1, f(e % 10 < 5 ? 1.2 : -.2, .5), t => 1, t => 0)
    }
}
function g(n) {
    for (let t = 0; t < 16; t++) {
        for (let e = 0; e < 5; e++) {
            n.add(t * 500, 8e3, t => e % 2 == 0 ? -.2 + t * 1.4 : 1.2 - t * 1.4, t => e * .2 + .1, t => .5, t => 0)
        }
    }
}
function p(t) {
    for (let s = 0; s < 50; s++) {
        let e = Math.cos(s * .5);
        let n = Math.random() * 1.6 + .2;
        t.add(s * 200, 2e3, t => -.2 + 1.4 * t, t => .5 + t * e, t => (1 - t) * 1 + t * n, t => t + .21 * s)
    }
}
function v(s) {
    let i = f(0, 1);
    for (let t = 0; t < 100; t++) {
        let e = Math.random() * .8 + .1;
        let n = Math.random() * .8 + .1;
        s.add(t * 100, 1e3, t => e, t => n, t => Math.max(0, i(t)), t => 0)
    }
}
function I(f) {
    for (let u = 0; u < 1e3; u++) {
        let e = u * .1 * Math.PI + Math.random() * .3;
        let t = .2;
        let n = 2.5;
        let s = .5 + Math.cos(e) * t;
        let i = .5 + Math.sin(e) * t;
        let o = .5 + Math.cos(e) * n;
        let r = .5 + Math.sin(e) * n;
        let a = t => s + (o - s) * t * t;
        let c = t => i + (r - i) * t * t;
        let h = t => .3 - t * .25;
        let l = t => t * 2 + e;
        f.add(u * 10, 2e3, a, c, h, l)
    }
}

async function B() {
    k.clear();
    R[b](k);
    await k.S();
    J(Date.now(), F);
    x.value = "";
    x.focus();
    S.classList.remove("hidden")
}
```

可以看到發牌的函式都會傳入 `k`，而他就是 `class e`，呼叫 `add()` 以後會到 `h()` 也就是發牌的邏輯

至於 `add()` 的其他邏輯是呈現動畫用的，這裡不需要看

```js
const s = 1664525;
const i = 1013904223;
const o = 2147483647;
let r = 1117122227;
function h() {
    let t = 63 & r >> 4;
    let e = t & 15;
    if (e > 9) {
        e = 16 - e
    }
    let n = 3 & t >> 4;
    r = r * s + i & o;
    return (n + e * 4 + 16) % 40
}

let k = new e;

class e {
    constructor() {
        this.canvas = a;
        this.u = c;
        this.m = [222, 323];
        this.M = [];
        this._ = [];
        this.active = new Set;
        this.g = 0;
        this.p = 0
    }

    ...

    add(t, e, n, s, i, o) {
        const r = h();
        const a = new u(n,s,i,o);
        const c = {
            I: r,
            transform: a,
            start: t,
            end: t + e
        };
        this.F(this.M, c, t => t.start);
        this.F(this._, c, t => t.end)
    }

    ...
    
    clear() {
        this.M = [];
        this._ = [];
        this.active.clear();
        this.g = 0;
        this.p = 0
    }
    ...
}
```

觀察 `h()` 可以看到他會以 seed 來算他該發哪張牌，此外也會更新 seed

```js
function nextCard() {
    let t = 63 & seed >> 4; // 取 seed 的第 4~9 bit，共 6 bits
    let e = t & 15; // 結果會是 0~15
    if (e > 9) {
        e = 16 - e // 把 10~15 變回 6~1
    }
    let n = 3 & t >> 4; // 只會是，0~3
    seed = (seed * 1664525 + 1013904223) & 0x7fffffff; // 更新 seed

    return (r + e * 4 + 16) % 40;
}
```

知道發牌邏輯以後我們就可以算出總和了，接著看怎麼把答案傳給伺服器，仔細觀察的話可以看到 `j()`

他就是把前端 form 裡面的答案傳到後端伺服器，拿到答案以後判斷是否正確或是是否為 flag，並看要結束還是繼續

```js
async function j() {
    let t = document.getElementById("submit_form");
    let e = new FormData(t);
    let n = await fetch("/api/submit", {
        method: "POST",
        headers: {
            T: "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(e)
    });
    let s = await n.json();
    r = s?.["seed"] ?? 11133334;
    return [s["flag"], s["deadline"], s["answer"], s["error"]]
}

async function K(t) {
    t.preventDefault();
    let[e,n,s,i] = await j();
    A.display = false;
    S.classList.add("hidden");
    if (i) {
        D.innerText = i;
        T.classList.remove("hidden")
    } else if (s) {
        D.innerText = `The correct answer was ${s}`;
        T.classList.remove("hidden")
    } else if (n) {
        F = n;
        b += 1;
        B()
    } else if (e) {
        H.innerText = `The flag is ${e}`;
        E.classList.remove("hidden")
    } else {
        console.error("Invalid response from the server");
        D.innerText = `Better luck next time`;
        T.classList.remove("hidden")
    }
}
```

```html
<form id="submit_form" onsubmit="K(event)">
    <div class="input_background">
    <progress id="deadline_bar" value="0" max="100"></progress>
    <label id="question" for="answer">What was the sum of all cards?</label>
    <div style="display: flex;gap:0.5em">
        <input id="answer" name="answer" type="number">
        <input type="submit" id="submit_button" value="➤">
    </div>
    </div>
</form>
```

綜合上述的資訊我們就可以寫一個腳本來自動算出牌的總和並取得 flag

## Flag

```text
dalctf{y0vre_re@dy_for_p0k3r}
```
