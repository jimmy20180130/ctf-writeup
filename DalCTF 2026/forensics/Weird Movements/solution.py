import sys
import struct
from collections import defaultdict
from PIL import Image, ImageDraw

PCAPNG_EPB = 0x00000006
PCAPNG_SHB = 0x0A0D0D0A

def s8(x):
    return x - 256 if x > 127 else x

def iter_packets(path):
    data = open(path, "rb").read()
    off = 0
    endian = "<"

    while off + 12 <= len(data):
        block_type, block_len = struct.unpack_from(endian + "II", data, off)
        if block_len <= 0:
            break

        if block_type == PCAPNG_SHB:
            bom = struct.unpack_from("<I", data, off + 8)[0]
            endian = "<" if bom == 0x1A2B3C4D else ">"

        elif block_type == PCAPNG_EPB:
            caplen = struct.unpack_from(endian + "I", data, off + 20)[0]
            pkt = data[off + 28 : off + 28 + caplen]
            yield pkt, endian

        off += block_len

def extract_mouse_reports(pcapng):
    streams = defaultdict(list)

    for pkt, endian in iter_packets(pcapng):
        if len(pkt) < 64:
            continue

        event_type = chr(pkt[8])      # 'S' submit, 'C' complete
        xfer_type = pkt[9]            # 1 = interrupt
        endpoint = pkt[10]
        dev = pkt[11]
        bus = struct.unpack_from(endian + "H", pkt, 12)[0]
        status = struct.unpack_from(endian + "i", pkt, 28)[0]
        data_len = struct.unpack_from(endian + "I", pkt, 36)[0]

        if event_type != "C":
            continue
        if xfer_type != 1:
            continue
        if not (endpoint & 0x80):     # IN endpoint
            continue
        if status != 0:
            continue
        if data_len < 3:
            continue

        payload = pkt[64 : 64 + data_len]

        # Standard mouse HID report: button, dx, dy, wheel
        if len(payload) == 4:
            streams[(bus, dev, endpoint)].append(payload)

    if not streams:
        raise RuntimeError("No USB HID mouse reports found.")

    # Pick the stream with the most reports
    key, reports = max(streams.items(), key=lambda kv: len(kv[1]))
    print(f"[+] using USB stream bus/dev/ep={key}, reports={len(reports)}")
    return reports

def draw_reports(reports, out_png):
    x = y = 0
    strokes = []
    cur = []

    for r in reports:
        buttons = r[0]
        dx = s8(r[1])
        dy = s8(r[2])

        x += dx
        y += dy

        if buttons & 1:   # left button pressed
            cur.append((x, y))
        else:
            if len(cur) > 1:
                strokes.append(cur)
            cur = []

    if len(cur) > 1:
        strokes.append(cur)

    pts = [p for stroke in strokes for p in stroke]
    if not pts:
        raise RuntimeError("No drawing strokes found.")

    min_x = min(px for px, py in pts)
    max_x = max(px for px, py in pts)
    min_y = min(py for px, py in pts)
    max_y = max(py for px, py in pts)

    scale = 4
    pad = 20
    w = (max_x - min_x) * scale + pad * 2
    h = (max_y - min_y) * scale + pad * 2

    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    for stroke in strokes:
        line = [
            ((px - min_x) * scale + pad, (py - min_y) * scale + pad)
            for px, py in stroke
        ]
        draw.line(line, fill="black", width=3)

    img.save(out_png)
    print(f"[+] saved: {out_png}")

reports = extract_mouse_reports('capture.pcapng')
draw_reports(reports, 'out.png')