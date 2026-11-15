#!/usr/bin/env python3
"""Flagship render gates (docs/27 quality bar). Runs after the bank render, on every preset
tagged 'flagship'. The bank-wide gates in check_render_qa.py still apply to them as well.

Per file
- DC below -60 dBFS (bar 12).
- Sub-20 Hz energy below -50 dB of the total (bar 12).
- One-shot ends at the floor: the last 50 ms sits at least 54 dB under the peak (bar 7).
Per preset
- Stereo: correlation of L and R in the 100 Hz band above 0.6 (bar 11).
- Mono fold: the mid signal's level within 3 dB of the louder side (bar 11).
- Velocity: soft / hard attack centroid ratio below 0.8 when there are 3+ layers (bar 4).
- Round robins: no two RR takes of one key and layer correlate above 0.999 (bar 5).
- Tuning: zones whose meta carries f0_hz are within +/-tune_c (default 1 c) (bar 9).
- L-locked loops (meta llock true): seam level step under 0.1 dB and loop-point correlation
  above 0.999 (bar 8).
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
SAMPLES = ROOT / "hise_project" / "ResearchFacility" / "Samples"
MAPS = ROOT / "hise_project" / "ResearchFacility" / "SampleMaps"
SR = 48000


def read(path):
    import wave
    with wave.open(str(path)) as w:
        ch, sw, n = w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        x = np.where(v >= 1 << 23, v - (1 << 24), v).astype(np.float64) / 8388608.0
    elif sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float64) / 32768.0
    else:
        x = np.frombuffer(raw, "<i4").astype(np.float64) / 2147483648.0
    return x.reshape(-1, ch)


def db(v):
    return 20.0 * math.log10(max(v, 1e-15))


def band(x, lo, hi):
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, [lo, hi], "bandpass", fs=SR, output="sos")
    return sosfiltfilt(sos, x)


def centroid(x):
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    return float(np.sum(sp * fr) / (np.sum(sp) + 1e-15))


def f0_of(x, guess):
    """Fundamental near a guess: FFT peak in +/-3% with parabolic interpolation (1 s window)."""
    seg = x[int(0.15 * SR): int(1.15 * SR)]
    nf = 1 << 20
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), nf))
    fr = np.fft.rfftfreq(nf, 1 / SR)
    m = (fr > guess * 0.97) & (fr < guess * 1.03)
    if not m.any():
        return None
    idx = np.nonzero(m)[0]
    k = int(idx[np.argmax(sp[idx])])
    a, b_, c = np.log(sp[k - 1:k + 2] + 1e-20)
    off = 0.5 * (a - c) / (a - 2 * b_ + c) if (a - 2 * b_ + c) != 0 else 0.0
    return (k + off) * SR / nf


def main():
    import build_signature_bank as bank
    flag = [p for p in bank.PRESETS if "flagship" in p.get("tags", [])]
    fails = []
    for p in flag:
        mp = MAPS / f"SIG_{p['id']}.xml"
        if not mp.exists():
            fails.append(f"{p['id']}: no sample map")
            continue
        xml = mp.read_text()
        zones = re.findall(r'FileName="\{PROJECT_FOLDER\}([^"]+)" Root="(\d+)".*?LoVel="(\d+)" HiVel="(\d+)" RRGroup="(\d+)"'
                           r'.*?LoopStart="(\d+)" LoopEnd="(\d+)" LoopXFade="(\d+)" LoopEnabled="(\d)"', xml, re.S)
        by_key = {}
        for fn, root, lov, hiv, rr, ls, le, xf, le_on in zones:
            x = read(SAMPLES / fn)
            meta_f = SAMPLES / (fn + ".meta.json")
            meta = json.loads(meta_f.read_text()).get("musical", {}) if meta_f.exists() else {}
            mono = x.mean(axis=1)
            pk = float(np.abs(x).max()) + 1e-15
            if abs(float(mono.mean())) > 1e-3:
                fails.append(f"{fn}: DC {db(abs(float(mono.mean()))):.1f} dBFS")
            tot = float(np.sum(mono ** 2)) + 1e-20
            sub = np.fft.rfft(mono)
            fr = np.fft.rfftfreq(len(mono), 1 / SR)
            sub_e = float(np.sum(np.abs(sub[fr < 20]) ** 2)) / (float(np.sum(np.abs(sub) ** 2)) + 1e-20)
            if sub_e > 10 ** (-50 / 10):
                fails.append(f"{fn}: sub-20 Hz energy {10 * math.log10(sub_e):.1f} dB")
            if le_on == "0":
                tail = float(np.sqrt(np.mean(mono[-int(0.05 * SR):] ** 2)))
                if db(tail / pk) > -54:
                    fails.append(f"{fn}: ends {db(tail / pk):.1f} dB under its peak (cut while sounding)")
            if meta.get("f0_hz"):
                f = f0_of(mono, meta["f0_hz"])
                tol = meta.get("tune_c", 1.0)
                if f is None or abs(1200 * math.log2(f / meta["f0_hz"])) > tol:
                    got = "none" if f is None else f"{1200 * math.log2(f / meta['f0_hz']):+.2f} c"
                    fails.append(f"{fn}: tuning {got} (tolerance {tol} c)")
            if meta.get("llock") and le_on == "1":
                ls_, le_ = int(ls), int(le)
                w = int(0.01 * SR)
                a = mono[le_ - w: le_]
                b_ = mono[ls_ - w: ls_]
                step = abs(db(float(np.sqrt(np.mean(a ** 2)))) - db(float(np.sqrt(np.mean(b_ ** 2)))))
                cc = float(np.dot(a, b_) / (np.sqrt(np.dot(a, a) * np.dot(b_, b_)) + 1e-15))
                if step > 0.1 or cc < 0.999:
                    fails.append(f"{fn}: L-lock seam {step:.2f} dB, corr {cc:.4f}")
            by_key.setdefault(int(root), []).append((int(lov), int(rr), x))
        # per-preset gates on the middle key
        if by_key:
            key = sorted(by_key)[len(by_key) // 2]
            takes = by_key[key]
            x = max(takes, key=lambda z: z[0])[2]
            l, r = x[:, 0], x[:, 1]
            if np.std(l - r) > 1e-6:
                bl, br = band(l, 70, 140), band(r, 70, 140)
                cc = float(np.dot(bl, br) / (np.sqrt(np.dot(bl, bl) * np.dot(br, br)) + 1e-15))
                if cc < 0.6:
                    fails.append(f"{p['id']}: 100 Hz L/R correlation {cc:.2f} < 0.6")
                mid = 0.5 * (l + r)
                fold = db(float(np.sqrt(np.mean(mid ** 2)))) - db(max(float(np.sqrt(np.mean(l ** 2))), float(np.sqrt(np.mean(r ** 2)))))
                if fold < -3.0:
                    fails.append(f"{p['id']}: mono fold {fold:.1f} dB")
            layers = sorted({z[0] for z in takes})
            if len(layers) >= 3:
                soft = next(z[2] for z in takes if z[0] == layers[0]).mean(axis=1)[: int(0.1 * SR)]
                hard = next(z[2] for z in takes if z[0] == layers[-1]).mean(axis=1)[: int(0.1 * SR)]
                ratio = centroid(soft) / (centroid(hard) + 1e-9)
                if ratio >= 0.8:
                    fails.append(f"{p['id']}: soft/hard attack centroid ratio {ratio:.2f} >= 0.8")
            for lv in layers:
                rrs = [z[2].mean(axis=1) for z in takes if z[0] == lv]
                for i in range(len(rrs)):
                    for j in range(i + 1, len(rrs)):
                        m = min(len(rrs[i]), len(rrs[j]))
                        a, b_ = rrs[i][:m], rrs[j][:m]
                        cc = float(np.dot(a, b_) / (np.sqrt(np.dot(a, a) * np.dot(b_, b_)) + 1e-15))
                        if cc > 0.999:
                            fails.append(f"{p['id']} key {key} layer {lv}: RR takes {i}/{j} correlate {cc:.4f}")
    print(f"flagship QA: {len(flag)} flagship presets checked")
    if fails:
        print(f"flagship QA FAILED: {len(fails)} problems")
        for f in fails[:40]:
            print("  " + f)
        return 1
    print("flagship QA: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
