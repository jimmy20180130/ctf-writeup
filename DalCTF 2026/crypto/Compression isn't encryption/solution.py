from decimal import Decimal

freq = """
z 0.00021
j 0.0003
q 0.00033
x 0.00051
{ 0.001
} 0.001
k 0.00207
_ 0.003
v 0.00333
b 0.00447
p 0.00546
g 0.00609
w 0.00627
y 0.00633
f 0.0069
m 0.00783
c 0.00813
u 0.00864
$ 0.011
l 0.01194
d 0.01296
7 0.0136
h 0.01776
r 0.01806
s 0.01884
6 0.02
8 0.02
9 0.02
n 0.02085
i 0.02193
o 0.02304
a 0.02436
5 0.0268
t 0.0273
! 0.029
4 0.0304
0 0.0336
e 0.03609
3 0.0640
2 0.0808
1 0.0908
""".strip()

bits = "101110101011011001101111110011011111101111011010110111110100100000100111101101001110100100001001111111011011101111000011011011011111011001001001111110010110010110101110010110110111101011110111"

nodes = []
for i, line in enumerate(freq.splitlines()):
    ch, w = line.split()
    nodes.append([Decimal(w), 1, i, ch])

idx = len(nodes)

while len(nodes) > 1:
    nodes.sort(key=lambda x: (x[0], x[1], x[2]))

    w1, _, _, n1 = nodes.pop(0)
    w2, _, _, n2 = nodes.pop(0)

    merged = (n1, n2)

    nodes.append([w1 + w2, 0, idx, merged])
    idx += 1

root = nodes[0][3]

ans = []
cur = root

for b in bits:
    cur = cur[0] if b == "0" else cur[1]

    if isinstance(cur, str):
        ans.append(cur)
        cur = root

flag = "".join(ans)
print(flag)