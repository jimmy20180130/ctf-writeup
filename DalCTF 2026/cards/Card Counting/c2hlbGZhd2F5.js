const s = 1664525;
const i = 1013904223;
const o = 2147483647;
const C = 15;
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
const a = document.getElementById("game");
const c = a.getContext("2d");
c.imageSmoothingEnabled = false;
c.imageSmoothingQuality = "low";
function t() {
    a.width = window.innerWidth;
    a.height = window.innerHeight
}
t();
window.addEventListener("resize", t);
const l = new Image;
l.src = "/static/media/images/cards.png";
class u {
    constructor(t, e, n, s) {
        this.t = t;
        this.i = e;
        this.o = n;
        this.h = s
    }
    l(t) {
        return [[this.t(t), this.i(t)], this.o(t), this.h(t)]
    }
}
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
    v(t=0, e=new Float32Array(2), n=1, s=0) {
        const {u: i, canvas: o} = this;
        i.save();
        i.translate(Math.round(e[0] * o.width), Math.round(e[1] * o.height));
        i.rotate(s * 2 * Math.PI);
        i.scale(n, n);
        i.strokeStyle = "black";
        i.fillStyle = "white";
        i.lineWidth = 4;
        i.beginPath();
        i.roundRect(-this.m[0] / 2, -this.m[1] / 2, this.m[0], this.m[1], 10 * n);
        i.fill();
        i.stroke();
        i.closePath();
        i.drawImage(l, this.m[0] * t, 0, this.m[0], this.m[1], -this.m[0] / 2, -this.m[1] / 2, this.m[0], this.m[1]);
        i.restore()
    }
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
    F(t, e, n) {
        let s = 0
          , i = t.length;
        const o = n(e);
        while (s < i) {
            const r = s + i >> 1;
            if (n(t[r]) < o)
                s = r + 1;
            else
                i = r
        }
        t.splice(s, 0, e)
    }
    clear() {
        this.M = [];
        this._ = [];
        this.active.clear();
        this.g = 0;
        this.p = 0
    }
    reset() {
        this.active.clear();
        this.g = 0;
        this.p = 0
    }
    q() {
        return this._.length > 0 && this.A >= this._[this._.length - 1].end
    }
    k(t) {
        this.A = t;
        c.clearRect(0, 0, a.width, a.height);
        while (this.g < this.M.length && this.M[this.g].start <= this.A) {
            this.active.add(this.M[this.g]);
            this.g++
        }
        while (this.p < this._.length && this._[this.p].end < this.A) {
            this.active["delete"](this._[this.p]);
            this.p++
        }
        for (const e of this.active) {
            const n = (this.A - e.start) / (e.end - e.start);
            const s = e.transform.l(n);
            this.v(e.I, s[0], s[1], s[2])
        }
    }
    async S() {
        let i = this;
        return new Promise(e => {
            let n = 0;
            function s(t) {
                i.k(t - n);
                if (i.q()) {
                    e();
                    return
                }
                requestAnimationFrame(s)
            }
            function t(t) {
                n = t;
                s(t)
            }
            requestAnimationFrame(t)
        }
        )
    }
}
function n(t) {
    return (1.95 * t - 2.85 * t * t + 1.9 * t * t * t) * 1.1 - .05
}
function f(r, a) {
    return t => {
        t = Math.min(Math.max(t, 0), 1);
        const e = r;
        const n = a;
        const s = r;
        function i(t) {
            return 3 * t * t - 2 * t * t * t
        }
        if (t <= .5) {
            const o = t * 2;
            return e + (n - e) * i(o)
        } else {
            const o = (t - .5) * 2;
            return n + (s - n) * i(o)
        }
    }
}
function d(t) {
    if (t < .5)
        return .5;
    return t
}
function m(t) {
    if (t < .5)
        return .5;
    return 1 - t
}
function w(t) {
    if (t < .2)
        return t * 5;
    return 1
}
function L(t) {
    if (t < .8)
        return 1;
    return 1 - (t - .8) * 5
}
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
function O(e) {
    for (let t = 0; t < 1e3; t++) {
        e.add(t * 200, 15e3, f(-.3, .9), t => Math.cos(t * 1.6 + .2 * t * t) - .3, t => Math.max(.01, Math.cos(t * 1.6 + .2 * t * t) * .8), t => (.5 - t) * .2)
    }
}
const R = [M, y, _, g, p, v, I];
async function U() {
    let t = await fetch("/api/start_game");
    let e = await t.json();
    r = e["seed"];
    return e.deadline
}
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
let b = 0;
let F = 0;
let q = {
    D: true,
    P: false,
    $: 0
};
let A = {
    display: false
};
let k = new e;
O(k);
const S = document.getElementById("question_section");
const T = document.getElementById("retry_section");
const E = document.getElementById("flag_section");
const x = document.getElementById("answer");
const G = document.getElementById("question");
const D = document.getElementById("retry_message");
const H = document.getElementById("flag_message");
const P = document.getElementById("deadline_bar");
document.getElementById("start_button").addEventListener("click", async () => {
    q.D = false;
    document.getElementById("start_section").classList.add("hidden");
    z()
}
);
document.getElementById("retry_button").addEventListener("click", () => {
    document.getElementById("retry_section").classList.add("hidden");
    z()
}
);
async function $(t) {
    if (q.D) {
        if (k.q()) {
            k.reset();
            q.$ = t
        }
        k.k(t - q.$);
        requestAnimationFrame($)
    }
}
requestAnimationFrame($);
function J(i, o) {
    A.display = true;
    progressInterval = setInterval( () => {
        const t = Date.now();
        const e = t - i;
        const n = o - i;
        const s = Math.min(100, Math.max(0, e / n * 100));
        P.value = s;
        if (t >= o) {
            clearInterval(progressInterval);
            P.value = 100
        }
        if (!A.display) {
            clearInterval(progressInterval)
        }
    }
    , 100)
}
async function z() {
    b = 0;
    F = await U();
    B()
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
