from PIL import Image

data = open('code_fixed').read().strip()
rows = [r for r in data.split('0A')]

W = H = 66
img = Image.new('RGB', (W, H))
px = img.load()
for y, r in enumerate(rows):
    for x in range(W):
        c = r[x*6:x*6+6]
        px[x, y] = (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

img.resize((W*12, H*12), Image.NEAREST).save('code.png')

print('saved code.png')