from PIL import Image

img = Image.open("challenge.png").convert("RGB")

bits = [b & 1 for r, g, b in img.getdata()]

bits = bits[0::5]

out = []
for i in range(0, len(bits) - 7, 8):
    v = 0
    for bit in bits[i:i+8]:
        v = (v << 1) | bit
    out.append(v ^ 0x5A)

msg = bytes(out)
flag = msg[:msg.index(b"}") + 1]
print(flag.decode())