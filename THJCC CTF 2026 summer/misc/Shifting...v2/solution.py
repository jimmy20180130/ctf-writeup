import itertools
import string
import time
import requests

INVALID = ("paste not found", "this paste has been removed", "unavailable for legal reasons")
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

for a, b in itertools.product(string.ascii_letters + string.digits, repeat=2):
    url = f"https://pastebin.com/D15r3g{a}{b}"
    print(f"trying: {url}")
    r = session.get(url, timeout=10)
    if r.status_code == 200 and not any(x in r.text.lower() for x in INVALID):
        print(f"found: {url}")
        break
    time.sleep(0.2)
