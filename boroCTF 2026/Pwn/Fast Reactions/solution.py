from pwn import *
import re

context.log_level = "info"

host = "tnkemaq46125.boroctf.com"
port = 56354

p = remote(host, port)

while True:
    try:
        data = p.recvuntil(b"characters!", timeout=3)
    except EOFError:
        print(p.recvall(timeout=1).decode(errors="ignore"))
        break

    print(data.decode(errors="ignore"), end="")

    m = re.search(rb"0x([0-9a-fA-F]+) characters", data)
    if not m:
        rest = p.recvall(timeout=1)
        print(rest.decode(errors="ignore"))
        break

    n = int(m.group(1), 16)
    log.info(f"sending {n} chars")

    p.sendline(b"A" * n)