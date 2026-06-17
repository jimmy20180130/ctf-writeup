#!/usr/bin/env python3
import json
import hashlib

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def parse_der(sighex):
    data = bytes.fromhex(sighex)

    assert data[0] == 0x30

    idx = 2

    assert data[idx] == 0x02
    r_len = data[idx + 1]
    r = int.from_bytes(data[idx + 2:idx + 2 + r_len], "big")
    idx += 2 + r_len

    assert data[idx] == 0x02
    s_len = data[idx + 1]
    s = int.from_bytes(data[idx + 2:idx + 2 + s_len], "big")

    return r, s


with open("transactions.json", "r") as f:
    txs = json.load(f)

records = []

for name, tx in txs.items():
    r, s = parse_der(tx["signature_der"])

    msg = f'{tx["sender"]}:{tx["recipient"]}:{tx["amount"]}'
    z = int.from_bytes(hashlib.sha256(msg.encode()).digest(), "big")

    records.append({
        "name": name,
        "flow": tx["flow"],
        "msg": msg,
        "r": r,
        "s": s,
        "z": z,
    })


for i in range(len(records)):
    for j in range(i + 1, len(records)):
        a = records[i]
        b = records[j]

        if a["r"] == b["r"]:
            print("[+] duplicate r found")
            print(a["name"], a["msg"])
            print(b["name"], b["msg"])

            r = a["r"]
            s1 = a["s"]
            s2 = b["s"]
            z1 = a["z"]
            z2 = b["z"]

            k = ((z1 - z2) * pow((s1 - s2) % N, -1, N)) % N
            d = ((s1 * k - z1) * pow(r, -1, N)) % N

            print("[+] k =", hex(k))
            print("[+] private key =", format(d, "064x"))
            print("[+] flag = boroCTF{" + format(d, "064x") + "}")