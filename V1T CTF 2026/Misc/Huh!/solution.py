raw = open("Huh.wav", "rb").read()[44:]
bits = [b & 1 for b in raw]

hidden = bytes(
    int("".join(map(str, bits[i:i+8])), 2)
    for i in range(0, len(bits) - 7, 8)
)

hidden = hidden.decode().replace('##', '') # 他會輸出一堆 #，mega 連結也有 #，所以就兩兩一組 replace

print(hidden) # https://mega.nz/file/DohSlCpB#3CQyY1OUnmmAgCOKLKPesgsGX3Mr2-t_qG9H3J1OGuE