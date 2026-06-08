import struct

outputs = [
    1167097856,
    1175651328,
    1177960448,
    1166821376,
    1172078592,
    1167663104,
    1181508608,
    1179558912,
    1158676480,
    1178182656,
    1159892992,
    1175258112,
    1176670208,
    1172424704,
    1178406912,
    1175258112,
    1180517376,
    1159073792,
    1161629696,
    1177092096,
    1175258112,
    1170735104,
    1158676480,
    1159073792,
    1178406912,
    1161629696,
    1159892992,
    1179324416,
    1160744960,
    1182016512,
]

def encode_char(ch):
    f = float(ord(ch))
    f = f * f

    bits = struct.unpack("<I", struct.pack("<f", f))[0]
    return bits

flag = ""

for target in outputs:
    for c in range(32, 127):
        ch = chr(c)

        if encode_char(ch) == target:
            flag += ch
            break
    else:
        flag += "?"

print(flag)