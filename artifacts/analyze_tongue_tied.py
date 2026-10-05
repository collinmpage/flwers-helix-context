import wave, json
import numpy as np

files = [r"C:/Users/Collin/Downloads/Tongue Tied Gtr Parts Solo'd.wav", r"C:/Users/Collin/Downloads/tongue tied MSTR02 (CD 16b44.1k).wav"]
report = []
for path in files:
    with wave.open(path, 'rb') as f:
        rate, channels, width = f.getframerate(), f.getnchannels(), f.getsampwidth()
        raw = f.readframes(f.getnframes())
    if width == 2:
        samples = np.frombuffer(raw, dtype='<i2').astype(float) / 32768
    elif width == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:,0] | b[:,1] << 8 | b[:,2] << 16
        samples = np.where(v & 0x800000, v - 0x1000000, v).astype(float) / 8388608
    else:
        raise ValueError(f'Unsupported PCM width {width}')
    samples = samples.reshape(-1, channels)
    entry = dict(file=path, sample_rate=rate, channels=channels, duration=len(samples)/rate, sections=[])
    times = [51, 64, 76, 87] if 'Solo' in path else [120]
    for second in times:
        clip = samples[int(second*rate):int((second+5)*rate)]
        mono = clip.mean(axis=1)
        n = min(len(mono), rate)
        powers = []
        for start in range(0, len(mono)-n+1, max(1,n//2)):
            powers.append(abs(np.fft.rfft(mono[start:start+n]*np.hanning(n)))**2)
        power = np.mean(powers, axis=0)
        freq = np.fft.rfftfreq(n, 1/rate)
        bands = [(80,250),(250,1000),(1000,3000),(3000,8000)]
        energy = [float(power[(freq>=lo)&(freq<hi)].sum()) for lo,hi in bands]
        total = sum(energy)
        entry['sections'].append(dict(second=second, rms_dbfs=round(float(20*np.log10(np.sqrt(np.mean(clip**2))+1e-12)),2), peak_dbfs=round(float(20*np.log10(np.max(abs(clip))+1e-12)),2), band_percent=[round(100*v/total,1) for v in energy]))
    report.append(entry)
with open('Tongue Tied Audio Measurements.json','w') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
