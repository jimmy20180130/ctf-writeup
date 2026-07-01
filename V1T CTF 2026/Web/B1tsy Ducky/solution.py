import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HMAC_SALT   = b"b1tsy-ducky-aesgcm"                 # HMAC key  @197509 (len 18)
NONCE_PREFIX = "nonce|"                             # concatstring2 input @188691
SEP          = "|"                                  # concatstring5 separator @187896
CIPHERTEXT   = bytes.fromhex(                       # hex literal @225365 (84 chars)
    "9e8c2b395bbf6bd7434230ab998c6e86"
    "f3228c503324c8660715ccd0bc74deb7"
    "d6346dfcc4a9614e58cb"
)

REFERRER = "https://b1tsy.v1t.site/"
PICKED32 = "797084dac2504482bcfaec15adc048bb"

ROOM3_TILEMAP = [
    "0,0,0,f,0,g,g,f,0,0,0,0,0,0,0,0",
    "0,0,0,g,0,g,0,g,g,g,g,0,0,0,0,0",
    "0,0,g,0,0,0,0,0,f,0,f,g,d,g,0,0",
    "0,g,d,0,0,0,0,0,0,0,0,0,0,g,g,0",
    "g,f,g,0,a,0,0,0,0,0,a,0,0,0,g,0",
    "g,0,0,a,0,0,0,a,a,0,0,0,0,0,d,0",
    "f,0,a,0,0,0,0,0,0,0,a,0,0,0,g,0",
    "g,g,0,0,0,0,a,0,a,0,0,0,0,0,g,f",
    "0,g,g,0,0,0,0,0,0,0,0,0,a,0,0,g",
    "0,d,0,0,0,a,0,0,0,0,0,0,0,0,g,g",
    "f,g,g,0,0,0,0,0,0,0,a,0,0,0,d,0",
    "g,0,0,0,0,0,0,0,0,0,0,0,0,0,g,0",
    "g,0,0,a,0,0,0,0,a,0,0,0,0,0,g,0",
    "g,f,0,0,0,0,0,0,0,g,d,g,g,g,f,0",
    "0,g,g,0,0,0,f,g,f,g,0,0,0,0,0,0",
    "0,0,0,g,f,g,0,0,0,0,0,0,0,0,0,0",
]

def serialize_room_block() -> str:
    lines = ["ROOM 3"]
    lines += ROOM3_TILEMAP
    lines.append("NAME example room copy 2")
    lines.append("EXT 4,0 2 4,15")
    lines.append("PAL 0")
    lines.append("TUNE 2")
    return "\n".join(lines)

def reveal(referrer: str, room3block: str, picked32: str) -> str:
    passwd = referrer + SEP + room3block + SEP + picked32
    key    = hmac.new(HMAC_SALT, passwd.encode(), hashlib.sha256).digest()
    nonce  = hashlib.sha256((NONCE_PREFIX + passwd).encode()).digest()[:12]
    return AESGCM(key).decrypt(nonce, CIPHERTEXT, None).decode()

room3 = serialize_room_block()
flag = reveal(REFERRER, room3, PICKED32)
print(flag) # v1t{b1tsy_t1psy_duck_w4sm}