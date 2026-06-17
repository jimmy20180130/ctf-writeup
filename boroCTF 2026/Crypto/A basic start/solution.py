# step 1 - base64
import base64

string = "VXNlcjE6IEhleSwgSSB0aGluayB0aGUgQm9ybyB0ZWFtIGlzIG9udG8gdXMhClVzZXIyOiBObyBXYXkhIFRoZXkncmUgZ29pbmcgdG8gc2VuZCB0aGUgQ1RGIHBhcnRpY2lwYW50cyBhZnRlciB1cyEKVXNlcjM6IEl0J2xsIGJlIG9rYXksIHdlJ2xsIG1vdmUgdG8gYW5vdGhlciBiYXNlIGVuY29kaW5nIQ=="
string = base64.b64decode(string)
print(string)

# step 2 - base91

s = "j2_1+iZB_6AveF[p/Uxg,WT[#F]4pE&m:%gZ6=0{8!Z%F.0Dj2_1rjZB!8O;R@RnqM_1:WGk$yV%J_;mz2gZY^rN$F90axFl]UgZk>;N%y60;mYiSP8=SH)S<Ry*yCrbVu_15Wy{L%;EU,fr&A2N|ir}XxI(pBZ%w<d9P"

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'

def b91decode(data):
    v = -1
    b = 0
    n = 0
    out = bytearray()

    for ch in data:
        c = alphabet.index(ch)

        if v < 0:
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14

            while n > 7:
                out.append(b & 255)
                b >>= 8
                n -= 8

            v = -1

    if v + 1:
        out.append((b | v << n) & 255)

    return bytes(out)

print(b91decode(s).decode())