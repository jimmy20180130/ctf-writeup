import base64
import gzip

chunks = [
    "d6fqqaacoygguax7go",
    "uaqmzqosuu5sjlrzhs",
    "wswmjuwy4l2kjuvm3t",
    "bjrex4ssenf7fc6lkj",
    "rxh4rt2nvucqb3wbxo",
    "zcsaaaaa",
]

encoded = "".join(chunks).upper()
compressed = base64.b32decode(encoded + "======")
flag = gzip.decompress(compressed)

print(flag.decode())