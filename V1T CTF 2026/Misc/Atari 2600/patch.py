from pathlib import Path

rom = Path("v1t.bas.bin")
data = bytearray(rom.read_bytes())

new_map = bytes.fromhex(
    "FF FF FF FF "
    "80 00 00 80 "
    "80 00 00 80 "
    "80 00 00 80 "
    "80 00 00 83 "
    "80 00 00 82 "
    "80 00 00 82 "
    "FF FF FF FF"
)

data[0x48E:0x48E + 32] = new_map

Path("v1t_patched.bin").write_bytes(data)
print("patched -> v1t_patched.bin")