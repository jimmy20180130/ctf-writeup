seed = ""

def rng(y):
    x = pow(int((175*y + 17) / 14 + 45), 15, 4294967295)
    return x

en = []

with open("output.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            en.append(int(line))


x = 324

for i in range(0, len(seed)):
    x += ord(seed[i])

flag = ""

for t in en:
    x = rng(x)
    ch = t // x
    flag += chr(ch)

print(flag)