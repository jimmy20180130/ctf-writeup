def rng(y):
    return pow(int((175*y + 17) / 14 + 45), 15, 4294967295)

X = 71303168 // ord('D')

for x in range(10000):
    if rng(x) == X:
        print(x)
        break