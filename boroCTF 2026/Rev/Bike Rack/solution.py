table = "AweQbLpMnorTyUioZxcvbnmCQwertyuioTqwFer{TyUiopasRd@fghjknLzXcvbnmdQwerty0u0IopasdMFghjklzxc_VbnmqwerYCvbnZMqw4e2RtyuiopasuFghjklzx%SdfyGhjklzmNbmqwerty}"

dest = "1927591750185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:238"

# memmove(dest, &dest[8], v3 - 7);
# strncat(dest, "187773102385012356629012836224235219768597857", 0xBu);
dest = dest[8:]
dest += "187773102385012356629012836224235219768597857"[:0xB]

pin = dest[::4]

v6 = 0
out = ""

for c in pin:
    v6 += ord(c) - ord('0')
    out += table[v6 - 1]
    if out.endswith("}"):
        break

print(pin)
print(out)