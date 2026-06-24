import hashlib, json, urllib.request

BASE_URL = "http://162.243.228.252:5000"

P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N  = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
PUB = (31075408999826857267622373589212020024719544603973655179256943732356976199204,
       95903745479717917561880478548129176548050831205073107571675088755035555146241)
PROTECTED = b"one ring to rule them all"
U = 20

def add(p, q):
    if p is None: return q
    if q is None: return p
    if p[0] == q[0] and (p[1] + q[1]) % P == 0: return None
    if p == q:
        m = (3 * p[0] * p[0]) * pow(2 * p[1], -1, P) % P
    else:
        m = (q[1] - p[1]) * pow(q[0] - p[0], -1, P) % P
    x = (m * m - p[0] - q[0]) % P
    return (x, (m * (p[0] - x) - p[1]) % P)

def mul(k, p=(Gx, Gy)):
    r = None
    while k:
        if k & 1: r = add(r, p)
        p = add(p, p); k >>= 1
    return r

def h(msg): return int(hashlib.sha256(msg).hexdigest(), 16)

def api(path, data):
    req = urllib.request.Request(BASE_URL + path,
                                 data=json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def oracle_sign(message):
    j = api("/sign", {"message": message})
    return int(j["h"]), int(j["nonce_msb"]), int(j["r"]), int(j["s"])

SIGS = [
    (107125873068076627457087917168470308992159544359252318215556110993730382558638,
     1345705611404482240910997051656082980580447527960032037647811243256875,
     15482948726620294824785901737349121380884329415834039699617336203385060698878,
     41581174235528323427257642410187520726774306953125111411937983658013715886832),
    (76693128649361230887255815150935942254957981220639293541855317788799281990094,
     64530364736000551952059762696230574387642343636258856368109848182380901,
     89983050630410276238361987121908177652883307648625520391588878921648694180365,
     86608461229591304191071280427918977121530678458476952254116370523164382276263),
]

def recover_d(sigs):
    (h1, m1, r1, s1), (h2, m2, r2, s2) = sigs[0], sigs[1]
    A1, A2 = m1 << U, m2 << U
    a, b = (r2 * s1) % N, (r1 * s2) % N
    C = (r1 * s2 * A2 - r1 * h2 - r2 * s1 * A1 + r2 * h1) % N
    binv = pow(b, -1, N)
    for e1 in range(1 << U):
        e2 = (a * e1 - C) * binv % N
        if e2 < (1 << U):
            d = (s1 * (A1 + e1) - h1) * pow(r1, -1, N) % N
            if mul(d) == PUB:
                return d

def sign(d, msg, k=0x1337):
    z = h(msg) % N
    r = mul(k)[0] % N
    s = pow(k, -1, N) * (z + r * d) % N
    return r, s

if __name__ == "__main__":
    sigs = [oracle_sign("msg1"), oracle_sign("msg2")] if BASE_URL else SIGS
    d = recover_d(sigs)
    assert mul(d) == PUB, "private key does not match public key"
    r, s = sign(d, PROTECTED)
    z = h(PROTECTED) % N
    w = pow(s, -1, N)
    R = add(mul(z * w % N), mul(r * w % N, PUB))
    assert R is not None and R[0] % N == r, "forged signature invalid"
    print("private key d =", d)
    print("forged sig on protected_message:")
    print("  r =", r)
    print("  s =", s)
    if BASE_URL:
        print("flag:", api("/verify", {"r": r, "s": s}))
    else:
        print("set BASE_URL and rerun, or POST {r, s} to /verify to get the flag")