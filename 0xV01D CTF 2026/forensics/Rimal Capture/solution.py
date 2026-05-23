import re
import struct
import sys

NORMAL = {
    **{i + 4: chr(ord('a') + i) for i in range(26)},
    0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4', 0x22: '5',
    0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n', 0x2B: '\t', 0x2C: ' ', 0x2D: '-', 0x2E: '=',
    0x2F: '[', 0x30: ']', 0x31: '\\', 0x33: ';', 0x34: "'",
    0x35: '`', 0x36: ',', 0x37: '.', 0x38: '/',
}

SHIFT = {
    **{i + 4: chr(ord('A') + i) for i in range(26)},
    0x1E: '!', 0x1F: '@', 0x20: '#', 0x21: '$', 0x22: '%',
    0x23: '^', 0x24: '&', 0x25: '*', 0x26: '(', 0x27: ')',
    0x28: '\n', 0x2B: '\t', 0x2C: ' ', 0x2D: '_', 0x2E: '+',
    0x2F: '{', 0x30: '}', 0x31: '|', 0x33: ':', 0x34: '"',
    0x35: '~', 0x36: '<', 0x37: '>', 0x38: '?',
}

BACKSPACE = 0x2A
FLAG_RE = re.compile(r'0xV01D\{[^}\n]+\}')


def udp_payloads_from_pcap(data):
    if data[:4] == b'\xd4\xc3\xb2\xa1':
        endian = '<'
    elif data[:4] == b'\xa1\xb2\xc3\xd4':
        endian = '>'
    else:
        return

    pos = 24
    while pos + 16 <= len(data):
        _, _, incl_len, _ = struct.unpack_from(endian + 'IIII', data, pos)
        pos += 16
        pkt = data[pos:pos + incl_len]
        pos += incl_len

        if len(pkt) < 42 or pkt[12:14] != b'\x08\x00':
            continue

        ip = 14
        ihl = (pkt[ip] & 0x0F) * 4
        proto = pkt[ip + 9]
        if proto != 17 or len(pkt) < ip + ihl + 8:
            continue

        udp = ip + ihl
        udp_len = struct.unpack('!H', pkt[udp + 4:udp + 6])[0]
        yield pkt[udp + 8:udp + udp_len]


def iter_hid_reports(data):
    found = False

    for payload in udp_payloads_from_pcap(data) or []:
        if payload.startswith(b'HID') and len(payload) >= 11:
            found = True
            yield payload[3:11]

    if found:
        return

    try:
        text = data.decode(errors='ignore')
        raw = bytes.fromhex(re.sub(r'[^0-9a-fA-F]', '', text))
    except ValueError:
        raw = data

    i = 0
    while True:
        i = raw.find(b'HID', i)
        if i == -1:
            break
        if i + 11 <= len(raw):
            yield raw[i + 3:i + 11]
        i += 11


def decode_hid(reports):
    out = []
    prev_keys = set()

    for report in reports:
        modifier = report[0]
        keycodes = [k for k in report[2:] if k]
        current_keys = set(keycodes)
        table = SHIFT if modifier & 0x22 else NORMAL

        for key in keycodes:
            if key in prev_keys:
                continue
            if key == BACKSPACE:
                if out:
                    out.pop()
            elif key in table:
                out.append(table[key])

        prev_keys = current_keys

    return ''.join(out)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            data = f.read()
    else:
        data = sys.stdin.buffer.read()

    text = decode_hid(iter_hid_reports(data))
    flags = FLAG_RE.findall(text)

    real = None
    for line in text.splitlines():
        if line.startswith('flag='):
            match = FLAG_RE.search(line)
            if match:
                real = match.group(0)
                break

    print(real or flags[-1])


main()
