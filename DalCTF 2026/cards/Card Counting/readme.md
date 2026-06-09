# Card Counting

## Description

Try your luck at our card counting mini-game! Get through every level to earn youself the flag!

## Solution Walkthrough

Upon entering the website, we can observe that it retrieves a seed from the server whenever the game starts. This seed seems highly correlated with how the cards are generated, so we begin analyzing its frontend JavaScript code.

First, we analyze how many rounds there are and how many cards are dealt in each round. We notice that when the start button is clicked, `z()` is called. Within `z()`, `U()` fetches the seed, and the entire game logic resides inside `B()`.

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

Inside `B()`, `R[b](k);` is utilized, where every element inside the array `R` is a function. Since they all look very similar, it likely represents the card-dealing logic.

Notice that the loops in functions `[M, y, _, g, p, v, I]` run `4, 8, 25, 80, 50, 100, 1000` times, respectively. When playing the game firsthand, the first level deals exactly 4 cards. Therefore, we can deduce that `R` represents the number of cards dealt in each round, while `e.add()` and `t.add()` are the functions that deal the cards.

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

We can see that the card-dealing functions always pass `k` as an argument, which is an instance of `class e`. Calling `add()` eventually routes to `h()`, which contains the actual logic for dealing a card.

The rest of the logic inside `add()` is purely for rendering animations and can be ignored here.

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

By observing `h()`, we can see that it uses the seed to calculate which card should be dealt, and it also updates the seed afterwards.

```js
function nextCard() {
    let t = 63 & seed >> 4; // Extract bits 4~9 of the seed, 6 bits in total
    let e = t & 15; // Result will be 0~15
    if (e > 9) {
        e = 16 - e // Convert 10~15 back to 6~1
    }
    let n = 3 & t >> 4; // Will only be 0~3
    seed = (seed * 1664525 + 1013904223) & 0x7fffffff; // Update the seed

    return (r + e * 4 + 16) % 40;
}
```

Now that we understand the card-dealing logic, we can calculate the total sum. Next, let's examine how the answer is transmitted to the server. Looking closely, we can find `j()`.

It sends the answer from the frontend form to the backend server. Once it receives the response, it determines whether the answer is correct or if it is the flag, and decides whether to terminate or proceed.

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

Combining the information above, we can write a script to automatically calculate the sum of the cards and retrieve the flag.

## Flag

```text
dalctf{y0vre_re@dy_for_p0k3r}
```
