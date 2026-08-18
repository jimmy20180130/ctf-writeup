import hashlib
from multiprocessing import Pool
from pathlib import Path

import numpy as np

CHAL = Path("chal/お昼はサイゼリヤに行こうニャ！")

# K1~K3 = ヤニ子/ヤク子/アル子 的年紀，K4 = ハメ子 的訂閱數 10.8 万
K = (21, 20, 24, 108000)

CS = np.array([ord(c) for c in "yaniko"], np.uint32)
PWLEN, TRUNC = 14, 8
CHAIN_LEN = 24576
NSP = 6 ** PWLEN
NUM_CHAINS = NSP // CHAIN_LEN
ENDBITS = (6 ** TRUNC - 1).bit_length()
M40 = np.uint64((1 << 40) - 1)
RMIX1, RMIX2 = 0x5851F42D4C95, np.uint64(0xF1357AEA2E63)
POW6 = (6 ** np.arange(PWLEN)).astype(np.uint64)


def rotl32(v, r):
    return (v << r) | (v >> (32 - r))


def yani40(msg):
    n = msg.shape[1]
    a = np.full(n, (K[0] ^ 0x9E3779B9) & 0xFFFFFFFF, np.uint32)
    b = np.full(n, (K[1] + 0x85EBCA6B) & 0xFFFFFFFF, np.uint32)
    c = np.full(n, (K[2] ^ 0xC2B2AE35) & 0xFFFFFFFF, np.uint32)
    d = np.full(n, (K[3] + 0x27D4EB2F) & 0xFFFFFFFF, np.uint32)
    for p in range(3):
        for x in msg:
            a ^= x
            a *= 0x01000193
            b = rotl32(b + a, 13) ^ c
            c = (c * np.uint32(5) + np.uint32(0xF00D)) ^ b
            d = rotl32(d ^ a, 7) + b
            a += d
        a ^= (p * 0x7FEB352D) & 0xFFFFFFFF
    for _ in range(4):
        a = (a ^ (b >> 15)) * np.uint32(0x2545F491)
        b = (b ^ (c >> 13)) * np.uint32(0x9E3779B1)
        c = (c ^ (d >> 11)) * np.uint32(0x85EBCA77)
        d = (d ^ (a >> 16)) * np.uint32(0xC2B2AE3D)
    return ((a ^ c).astype(np.uint64) << np.uint64(32) | (b ^ d).astype(np.uint64)) & M40


def reduce_at(h, i, dig, msg):
    x = (h + np.uint64(RMIX1) * i) & M40
    x = ((x << np.uint64(21)) | (x >> np.uint64(19))) & M40
    x = (x * RMIX2) & M40
    x ^= x >> np.uint64(23)
    x %= np.uint64(NSP)
    for k in range(PWLEN):
        dig[k] = x % np.uint64(6)
        msg[k] = CS[dig[k]]
        x //= np.uint64(6)


def new_pw(idx):
    dig = np.empty((PWLEN, len(idx)), np.uint8)
    msg = np.empty((PWLEN, len(idx)), np.uint32)
    x = idx.copy()
    for k in range(PWLEN):
        dig[k] = x % np.uint64(6)
        msg[k] = CS[dig[k]]
        x //= np.uint64(6)
    return dig, msg


def pw_to_val(dig):
    return (dig[:TRUNC].astype(np.uint64) * POW6[:TRUNC, None]).sum(0)


def load_table(path):
    bits = np.unpackbits(np.fromfile(path, np.uint8), bitorder="little")
    bits = bits[: NUM_CHAINS * ENDBITS].reshape(NUM_CHAINS, ENDBITS)
    return (bits * (1 << np.arange(ENDBITS, dtype=np.uint32))).sum(1, dtype=np.uint32)


ENDS = load_table(CHAL / "nyan.tbl")
ORDER = np.argsort(ENDS, kind="stable").astype(np.uint32)
ENDS_SORTED = ENDS[ORDER]


def crack(hexdigest):
    h = int(hexdigest, 16)
    dig = np.empty((PWLEN, CHAIN_LEN), np.uint8)
    msg = np.empty((PWLEN, CHAIN_LEN), np.uint32)
    reduce_at(np.full(CHAIN_LEN, h, np.uint64),
              np.arange(CHAIN_LEN, dtype=np.uint64), dig, msg)
    for i in range(1, CHAIN_LEN):
        reduce_at(yani40(msg[:, :i]), np.uint64(i), dig[:, :i], msg[:, :i])

    val = pw_to_val(dig).astype(np.uint32)
    lo = np.searchsorted(ENDS_SORTED, val, "left")
    hi = np.searchsorted(ENDS_SORTED, val, "right")
    cand_c = np.concatenate([ORDER[a:b] for a, b in zip(lo, hi)])
    cand_j = np.repeat(np.arange(CHAIN_LEN, dtype=np.uint64), hi - lo)
    o = np.argsort(cand_j, kind="stable")
    cand_c, cand_j = cand_c[o], cand_j[o]

    dig, msg = new_pw(cand_c.astype(np.uint64))
    at = 0
    for i in range(CHAIN_LEN):
        end = np.searchsorted(cand_j, i, "right")
        if end > at:
            hit = np.nonzero(yani40(msg[:, at:end]) == h)[0]
            if len(hit):
                return "".join("yaniko"[d] for d in dig[:, at + hit[0]])
            at = end
        if at >= len(cand_c):
            break
        reduce_at(yani40(msg[:, at:]), np.uint64(i), dig[:, at:], msg[:, at:])
    return None


def main():
    hashes = [line.split(":")[1] for line in (CHAL / "shadow.txt").read_text().split()]
    with Pool(len(hashes)) as pool:
        pws = pool.map(crack, hashes)
    key = hashlib.sha256("|".join(pws).encode()).digest()
    ct = (CHAL / "flag.enc").read_bytes()[16:]
    ks = b"".join(hashlib.sha256(key + b"YANI-CTR" + i.to_bytes(4, "big")).digest()
                  for i in range(len(ct) // 32 + 1))
    print(bytes(a ^ b for a, b in zip(ct, ks)).decode())


if __name__ == "__main__":
    main()
