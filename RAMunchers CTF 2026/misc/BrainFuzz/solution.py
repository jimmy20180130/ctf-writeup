
data = open('output.bin','rb').read()

chunks = [data[i:i+8] for i in range(0, len(data), 8)]
ff_chunk = bytes([0xff]*8)
non_ff = [(i, chunks[i].hex()) for i in range(len(chunks)) if chunks[i] != ff_chunk]
print(f'Non-FF chunks: {len(non_ff)} out of {len(chunks)}')

# binary: 1 = non-ff, 0 = ff
bits = [0 if c == ff_chunk else 1 for c in chunks]
print('Bits (non-ff=1, ff=0):')
print(''.join(map(str, bits)))
n = len(bits)
print(f'Num bits: {n}')
if n % 8 == 0:
    chars = []
    for i in range(0, n, 8):
        byte = int(''.join(map(str, bits[i:i+8])), 2)
        chars.append(byte)
    print(bytes(chars))

# d3f1n173ly_n07_4_53cR37_p4$$w0Rd