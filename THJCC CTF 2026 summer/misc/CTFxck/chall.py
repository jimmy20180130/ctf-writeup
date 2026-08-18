# 101001100001111010100110110001100001010010010110011101100000111010101110001011100001010010010100100101
# .$[2|2]
# EOF
# print(open("chall.py").read(), dict(__import__("os").environ))

#!/usr/bin/env python3
import builtins
import signal
import sys
from collections import deque

MAX_SRC = 110
MAX_STEPS = 1 << 20
MAX_OUT = 64

DUP, POP, INPUT, OUTPUT, PUSH, JMP = range(6)
DIGITS = "0123456789"


def parse_int(src, i, end):
    n = 0
    while True:
        if i >= len(src):
            raise ValueError(f"expected {end!r} or a digit, found EOF")
        c = src[i]
        i += 1
        if c == end:
            return n, i
        if c not in DIGITS:
            raise ValueError(f"unexpected {c!r} while parsing a conditional")
        n = n * 10 + int(c)


def translate(src):
    prog, line = [], [0]
    i = 0
    while i < len(src):
        c = src[i]
        i += 1
        if c == "\n":
            line.append(len(prog))
        elif c == ":":
            prog.append((DUP, None))
        elif c == "$":
            prog.append((POP, None))
        elif c == "0":
            prog.append((PUSH, 0))
        elif c == "1":
            prog.append((PUSH, 1))
        elif c == ",":
            prog.append((INPUT, None))
        elif c == ".":
            prog.append((OUTPUT, None))
        elif c == "[":
            if_, i = parse_int(src, i, "|")
            else_, i = parse_int(src, i, "]")
            prog.append((JMP, (if_, else_)))

    def goto(n, here):
        if n == 0:
            return here + 1
        if n > len(line):
            return len(prog)
        return line[n - 1]

    resolved = []
    for pc, (op, arg) in enumerate(prog):
        if op == JMP:
            arg = (goto(arg[0], pc), goto(arg[1], pc))
        resolved.append((op, arg))
    return resolved


def interpret(prog, stdin=b""):
    queue = deque()
    out = bytearray()
    byte = bits = 0
    read = 0
    pc = steps = 0

    while pc < len(prog) and steps < MAX_STEPS:
        steps += 1
        op, arg = prog[pc]

        if op == PUSH:
            queue.append(arg)
        elif op == INPUT:
            b = stdin[read >> 3] if read >> 3 < len(stdin) else 0
            queue.append(b >> (read & 7) & 1)
            read += 1
        elif op == OUTPUT:
            if not queue:
                break
            byte |= queue[0] << bits
            bits += 1
            if bits == 8:
                out.append(byte)
                byte = bits = 0
                if len(out) >= MAX_OUT:
                    break
        elif op == JMP:
            if not queue:
                break
            pc = arg[0] if queue[0] else arg[1]
            continue
        elif op == POP:
            if not queue:
                break
            queue.popleft()
        elif op == DUP:
            if not queue:
                break
            queue.append(queue[0])

        pc += 1

    if bits and len(out) < MAX_OUT:
        out.append(byte)

    return bytes(out)


def read_program():
    sys.stdin.reconfigure(errors="replace")
    src = []
    while True:
        chunk = sys.stdin.readline()
        if not chunk:
            break
        chunk = chunk.rstrip("\r\n")
        if chunk == "EOF":
            break
        src.append(chunk)
    return "\n".join(src)


def main():
    signal.alarm(60)
    sys.stdout.write(">>> ")
    sys.stdout.flush()

    src = read_program()
    if len(src) > MAX_SRC:
        sys.exit("nope")

    try:
        prog = translate(src)
    except Exception:
        sys.exit("nope")

    out = interpret(prog)
    sys.stdout.flush()

    signal.alarm(600)
    try:
        exec(out, {"__builtins__": builtins})
    except BaseException:
        sys.exit("nope")


if __name__ == "__main__":
    main()
