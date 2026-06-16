from scapy.all import rdpcap, IP, TCP
import sys
import math

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} chronos.pcap")
    sys.exit(1)

pcap = sys.argv[1]

SRC = "10.10.10.5"
DST = "192.168.1.20"
SPORT = 4444
DPORT = 80

# 0.25 -> 0, 0.75 -> 1
THRESHOLD = 0.5

pkts = rdpcap(pcap)

times = []

for p in pkts:
    if IP in p and TCP in p:
        if (
            p[IP].src == SRC and
            p[IP].dst == DST and
            p[TCP].sport == SPORT and
            p[TCP].dport == DPORT
        ):
            times.append(float(p.time))

bits = []

# first packet: use fractional part
first_delta = times[0] - math.floor(times[0])
bits.append("1" if first_delta > THRESHOLD else "0")

for i in range(1, len(times)):
    delta = times[i] - times[i - 1]
    bits.append("1" if delta > THRESHOLD else "0")

bitstr = "".join(bits)

msg = ""
for i in range(0, len(bitstr), 8):
    b = bitstr[i:i+8]
    if len(b) == 8:
        msg += chr(int(b, 2))

print(msg)