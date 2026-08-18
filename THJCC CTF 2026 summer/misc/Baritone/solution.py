import numpy as np
import soundfile as sf

y, sr = sf.read("baritone.mp3", dtype="float32")
if y.ndim > 1:
    y = y.mean(axis=1)

n = int(sr * 0.5)
flag = ""

for start in range(0, len(y) - n, n):
    chunk = y[start:start + n]
    if np.sqrt(np.mean(chunk ** 2)) < 5e-4:
        continue
    spectrum = np.abs(np.fft.rfft((chunk - chunk.mean()) * np.hanning(n)))
    freq = np.fft.rfftfreq(n, 1 / sr)[np.argmax(spectrum)]
    flag += chr(round(69 + 12 * np.log2(freq / 440)))

print(flag)
