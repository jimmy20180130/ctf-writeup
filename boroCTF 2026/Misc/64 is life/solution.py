from pathlib import Path
import base64

folder = Path("64/ctf_chunks")

parts = []

files = sorted(
    folder.iterdir(),
    key=lambda f: int(base64.b64decode(f.name).decode())
)

for f in files:
    parts.append(f.read_text().strip())

data = "".join(parts).replace("40", "")
flag = base64.b64decode(data).decode()
print(flag)