const BASE_URL = "https://dalctf-card-counting-183-64616c.instancer.dalctf2026.com";
const ROUND_COUNTS = [4, 8, 25, 80, 50, 100, 1000];

let seed = 0;
let cookie = "";

function nextValue() {
    let t = 63 & seed >> 4; // 取 seed 的第 4~9 bit，共 6 bits
    let e = t & 15; // 結果會是 0~15
    if (e > 9) e = 16 - e // 把 10~15 變回 6~1
    seed = (seed * 1664525 + 1013904223) & 0x7fffffff; // 更新 seed

    return e + 1; // 最後結果是 1~10
}

async function request(path, options = {}) {
    const headers = {
        ...(cookie ? { Cookie: cookie } : {}),
        ...(options.headers || {})
    };

    const res = await fetch(BASE_URL + path, {
        ...options,
        headers
    });

    const setCookie =
        res.headers.getSetCookie?.()?.join("; ") ||
        res.headers.get("set-cookie");

    if (setCookie) {
        cookie = setCookie
            .split(",")
            .map(x => x.split(";")[0])
            .join("; ");
    }

    return res.json();
}

async function startGame() {
    const data = await request("/api/start_game");
    seed = data.seed;
    console.log("game seed:", seed);
}

async function submitAnswer(answer) {
    const data = await request("/api/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            answer: String(answer)
        })
    });

    seed = data.seed ?? 11133334;
    return data;
}

async function solve() {
    await startGame();

    for (let round = 0; round < ROUND_COUNTS.length; round++) {
        let answer = 0;

        for (let i = 0; i < ROUND_COUNTS[round]; i++) {
            answer += nextValue();
        }

        console.log(`round ${round}, answer = ${answer}`);

        const result = await submitAnswer(answer);

        if (result.flag) {
            console.log("flag:", result.flag);
            break;
        }

        if (result.error) {
            console.error("error:", result.error);
            break;
        }

        if (result.answer) {
            console.error(`wrong answer, correct = ${result.answer}, ours = ${answer}`);
            break;
        }

        console.log(`round ${round} passed`);
    }
}

solve().catch(console.error);