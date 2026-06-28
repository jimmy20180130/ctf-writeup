import re

raw = open("Huh.wav", "rb").read()[44:]
bits = [b & 1 for b in raw]

hidden = bytes(
    int("".join(map(str, bits[i:i+8])), 2)
    for i in range(0, len(bits) - 7, 8)
)

print(re.search(
    rb"https://mega\.nz/file/[A-Za-z0-9_-]+#[A-Za-z0-9_-]+",
    hidden
).group().decode())