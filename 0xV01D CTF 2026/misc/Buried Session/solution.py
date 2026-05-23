from pathlib import Path
import zlib, re

data = Path("artifact.bin").read_bytes()

for key in range(256):
    x = bytes(b ^ key for b in data)

    for off in range(len(x) - 2):
        if x[off:off+2] in (b"\x78\x01", b"\x78\x9c", b"\x78\xda"):
            try:
                out = zlib.decompress(x[off:])
            except zlib.error:
                continue

            m = re.search(rb"0xV01D\{[^}]+\}", out)
            if m:
                print(hex(key), off, m.group().decode())