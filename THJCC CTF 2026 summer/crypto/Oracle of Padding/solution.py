from pwn import remote

BS = 16

io = remote("chal.thjcc.org", 12000)
raw = bytes.fromhex(io.recvline().split()[1].decode())
blocks = [raw[i:i + BS] for i in range(0, len(raw), BS)]

def batch_oracle(msgs):
    io.send(b"".join(m.hex().encode() + b"\n" for m in msgs))
    return [line == b"OK" for line in io.recvlines(len(msgs))]

plaintext = b""

for bi in range(1, len(blocks)):
    prev, cur = blocks[bi - 1], blocks[bi]
    inter = [0] * BS

    for pad in range(1, BS + 1):
        pos = BS - pad
        msgs = []

        for guess in range(256):
            forged = bytearray(prev)
            for j in range(pos + 1, BS):
                forged[j] = inter[j] ^ pad
            forged[pos] = guess
            msgs.append(bytes(forged) + cur)

        hits = [i for i, ok in enumerate(batch_oracle(msgs)) if ok]
        hit = next(x for x in hits if x != prev[pos]) if pad == 1 and len(hits) > 1 else hits[0]
        inter[pos] = hit ^ pad

    plaintext += bytes(inter[i] ^ prev[i] for i in range(BS))

print(plaintext[:-plaintext[-1]].decode())
