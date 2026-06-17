s = r"?AEAGJ8NJF,\0[d5JcE-"

def rot47(s):
    out = ""
    for c in s:
        x = ord(c)
        if 33 <= x <= 126:
            out += chr(33 + ((x - 33 + 47) % 94))
        else:
            out += c
    return out

print(rot47(s))