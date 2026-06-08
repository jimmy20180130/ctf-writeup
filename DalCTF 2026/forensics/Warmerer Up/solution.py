import re, base64
from pathlib import Path

data = Path("rules2.pdf").read_bytes()

chunks = []
for m in re.finditer(rb"@@(\d+):(.*?)@@", data, re.S):
    idx = int(m.group(1))
    chunk = m.group(2)
    chunks.append((idx, chunk))

chunks.sort()
b64 = b"".join(chunk for _, chunk in chunks)
zip_data = base64.b64decode(b64)

Path("hidden.zip").write_bytes(zip_data)