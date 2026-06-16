from scapy.all import rdpcap, IP, UDP
import sys
import math

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} david_last_moments.pcap")
    sys.exit(1)

pcap = sys.argv[1]

SRC = "192.168.77.1"
DST = "192.168.77.2"
SPORT = 4444
DPORT = 5555

# (0.00015 + 0.00065) / 2 = 0.0004
THRESHOLD = 0.0004

pkts = rdpcap(pcap)

times = []

for p in pkts:
    if IP in p and UDP in p:
        if (
            p[IP].src == SRC and
            p[IP].dst == DST and
            p[UDP].sport == SPORT and
            p[UDP].dport == DPORT
        ):
            times.append(float(p.time))

bits = []

# 0.00015s -> 0, 0.00065s -> 1
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