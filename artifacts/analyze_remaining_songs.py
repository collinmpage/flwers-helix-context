import json
from pathlib import Path
import numpy as np
import wave

names = ["Fade Gtr Parts Solo'd.wav", "Fade FULL PRACTICE TRACK.wav", "Better Than This Gtr Parts Solo'd.wav", "Better Than This FULL PRACTICE TRACK.wav", "Nothing at All Collins Parts Solo'd.wav", "Nothing at All FULL PRACTICE TRACK.wav"]
report = []
for name in names:
    with wave.open(str(Path('C:/Users/Collin/Downloads') / name), 'rb') as f:
        rate, channels, width = f.getframerate(), f.getnchannels(), f.getsampwidth()
        raw = f.readframes(f.getnframes())
    if width == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1,3).astype(np.int32)
        v = b[:,0] | b[:,1]<<8 | b[:,2]<<16
        a = np.where(v & 0x800000, v-0x1000000, v).astype(np.float32)/8388608
    else:
        a = np.frombuffer(raw, dtype={2:'<i2',4:'<i4'}[width]).astype(np.float32)/(2**(width*8-1))
    a = a.reshape(-1, channels)
    windows = []
    for start in range(0, len(a), rate * 10):
        clip = a[start:start+rate*10]
        rms = float(np.sqrt(np.mean(clip**2)))
        peak = float(np.max(abs(clip)))
        mono = clip.mean(axis=1)
        n = min(rate, len(mono))
        powers = [abs(np.fft.rfft(mono[j:j+n] * np.hanning(n)))**2 for j in range(0, len(mono)-n+1, n)]
        power = np.mean(powers, axis=0)
        freq = np.fft.rfftfreq(n, 1/rate)
        energies = [float(power[(freq >= lo) & (freq < hi)].sum()) for lo, hi in [(80,250),(250,1000),(1000,3000),(3000,8000)]]
        total = sum(energies) or 1
        windows.append(dict(second=round(start/rate), rms_dbfs=round(20*np.log10(rms+1e-12),1), peak_dbfs=round(20*np.log10(peak+1e-12),1), bands=[round(v*100/total,1) for v in energies]))
    report.append(dict(file=name, rate=rate, channels=a.shape[1], duration=round(len(a)/rate,2), windows=windows))
Path('Remaining Songs Audio Measurements.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
