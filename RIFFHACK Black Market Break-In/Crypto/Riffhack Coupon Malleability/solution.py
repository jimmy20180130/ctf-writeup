from pwn import *
import base64
import itertools
import time
import os

HOST = "104.131.248.65"
PORT = 1337

nonce_hex = "47c03be4b9dd4162a5e90f8c5527d130"
blob_b64 = "AT7WU7O2/Oj+QY/SrVLv2OCXh8Jd+YVSRoWCw0BSYOiWi4iZGgoaBqjDQZw5UCs0pszMZrP26BqavD/DBFBZKA=="

BLOCK = 16
iv0 = bytes.fromhex(nonce_hex)
ct0 = base64.b64decode(blob_b64)

context.log_level = "error"

def padded_len(n):
    return n + (BLOCK - n % BLOCK)

def blocks_of(off, length):
    return set(range(off // BLOCK, (off + length - 1) // BLOCK + 1))

def corrupted_by_editing_value(off, length):
    out = set()
    for pos in range(off, off + length):
        b = pos // BLOCK
        if b > 0:
            out.add(b - 1)
    return out

def forge_direct(pt):
    ptb = pt.encode()

    if padded_len(len(ptb)) != len(ct0):
        return None

    iv = bytearray(iv0)
    ct = bytearray(ct0)

    for old, new in [(b"retail", b"vendor"), (b"trial", b"admin")]:
        off = ptb.index(old)

        for i, (a, b) in enumerate(zip(old, new)):
            pos = off + i
            blk = pos // BLOCK
            idx = pos % BLOCK
            delta = a ^ b

            if blk == 0:
                iv[idx] ^= delta
            else:
                ct[(blk - 1) * BLOCK + idx] ^= delta

    return iv.hex(), base64.b64encode(bytes(ct)).decode()

def score_plaintext(pt):
    grp_off = pt.index("grp=retail")
    tier_off = pt.index("tier=trial")
    retail_off = pt.index("retail")
    trial_off = pt.index("trial")

    needed = (
        blocks_of(grp_off, len("grp=retail")) |
        blocks_of(tier_off, len("tier=trial"))
    )

    corrupted = (
        corrupted_by_editing_value(retail_off, len("retail")) |
        corrupted_by_editing_value(trial_off, len("trial"))
    )

    bad = bool(needed & corrupted)
    return bad, needed, corrupted

def block_layout(pt):
    lines = []
    for i in range(0, len(pt), 16):
        lines.append(f"P{i//16}: {pt[i:i+16]!r}")
    return "\n".join(lines)

def gen_candidates():
    field_sets = [
        (
            "short_product_all_fields",
            {
                "issuer": "issuer=riffhack-labs",
                "product": "product=SilentCart",
                "grp": "grp=retail",
                "tier": "tier=trial",
            },
        ),
    ]

    out = []

    for set_name, fields in field_sets:
        names = list(fields.keys())

        for perm in itertools.permutations(names):
            pt = ";".join(fields[k] for k in perm)

            forged = forge_direct(pt)
            if forged is None:
                continue

            bad, needed, corrupted = score_plaintext(pt)
            nonce, blob = forged

            out.append({
                "set": set_name,
                "perm": perm,
                "pt": pt,
                "bad": bad,
                "needed": needed,
                "corrupted": corrupted,
                "nonce": nonce,
                "blob": blob,
            })

    out.sort(key=lambda c: (c["bad"], len(c["corrupted"]), c["set"], c["perm"]))
    return out

def submit(nonce, blob):
    io = remote(HOST, PORT, timeout=8)

    io.recvuntil(b">>", timeout=8)
    io.sendline(nonce.encode())

    io.recvuntil(b">>", timeout=8)
    io.sendline(blob.encode())

    data = io.recvall(timeout=8)
    io.close()
    return data.decode(errors="replace")

def main():
    candidates = gen_candidates()

    try_bad = os.getenv("TRY_BAD", "0") == "1"
    delay = float(os.getenv("DELAY", "2.0"))

    for idx, c in enumerate(candidates, 1):
        if c["bad"] and not try_bad:
            continue

        print("=" * 80)
        print(f"[{idx}] set={c['set']} perm={c['perm']}")
        print(f"bad/self-clobber = {c['bad']}")
        print(f"needed blocks     = {sorted(c['needed'])}")
        print(f"corrupted blocks  = {sorted(c['corrupted'])}")
        print(block_layout(c["pt"]))
        print()
        print("nonce =", c["nonce"])
        print("blob  =", c["blob"])
        print()

        try:
            res = submit(c["nonce"], c["blob"])
        except Exception as e:
            print("[!] connection/error:", repr(e))
            time.sleep(delay)
            continue

        print(res)

        if "rejected" not in res.lower():
            print("[+] possible success!")
            break

        time.sleep(delay)

if __name__ == "__main__":
    main()