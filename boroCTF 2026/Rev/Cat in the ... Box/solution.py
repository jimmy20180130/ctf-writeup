def main():
    off_4020 = [
        "a1b2c3", "x7y8z9", "q1w2e3", "r4t5y6", "z9y8x7", "p4ssw0", "9m8n7b",
        "v3r1fy", "t3st12", "85u4rm", "lmnopq", "abc123", "qwerty", "zxcvbn",
        "nm7k3l", "g5h6j7", "s4m2pl", "r2nd0m", "b7g6h5", "k1l2m3", "7h8g6f",
        "j3k4l5", "h4x0r1", "w1n2g3", "y6t5r4", "u7i8o9", "o9p8l7", "e3r4t5",
        "n0p9q8", "ymweyc", "m5n6b7", "f2g3h4", "d8c7b6", "s1a2m3", "t0r9q8",
        "p9o8i7", "z1x2c3", "v0b9n8", "l3k2j1", "i7u6y5", "o5p4i3", "h6g5f4",
        "e1w2q3", "r8t7y6", "s9d8f7", "g4h3j2", "p0u9l8", "b2n3m4", "golden", "silver"
    ]

    for i in off_4020:
        result = connect(i)

        if 'http' in result:
            print(result)
            break

def connect(a1):
    v7 = [0] * 128
    v8 = [0] * 128

    byte_2010 = [
        0x11, 0x19, 0x03, 0x15, 0x0A, 0x59, 0x56, 0x42, 0x11, 0x0C, 0x15,
        0x06, 0x0A, 0x43, 0x14, 0x04, 0x0D, 0x01, 0x16, 0x15, 0x59, 0x08, 0x16,
        0x06, 0x56
    ]

    byte_2029 = [
        0x57, 0x19, 0x0F, 0x11
    ]

    for i in range(25):
        v7[i] = ord(a1[i % len(a1)]) ^ byte_2010[i]

    v7 = ''.join(chr(x) for x in v7)

    for j in range(4):
        v8[j] = ord(a1[j % len(a1)]) ^ byte_2029[j]

    v8 = ''.join(chr(x) for x in v8)

    return f'{v7}{a1}{v8}'

main()