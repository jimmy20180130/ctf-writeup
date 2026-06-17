from PIL import Image

img = Image.open("dance.png").convert("RGB")

w, h = img.size
cols = 4
rows = 3

for y in range(rows):
    row = []
    for x in range(cols):
        # 取每個色塊的中心點
        px = int((x + 0.5) * w / cols)
        py = int((y + 0.5) * h / rows)

        r, g, b = img.getpixel((px, py))
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        row.append(hex_color)

    print(row)

colors = [
    "#626f72", "#6f4354", "#467b6e", "#457633",
    "#725f6c", "#302465", "#5f596f", "#55345f",
    "#426540", "#747d00", "#000000", "#000000",
]

text = ""

for color in colors:
    hex_part = color[1:]
    data = bytes.fromhex(hex_part)
    text += data.decode(errors="ignore")

print(text)