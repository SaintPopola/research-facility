#!/usr/bin/env python3
"""
Sweet Melody - Loop Lines builder (Arcade-style loops mode, v1).

Renders original 2-bar loops from the plugin's own synthesis recipes
(scripts/build_signature_bank.py presets), at the tempos/keys of the playlist
DNA (docs/12, docs/15). Each kit = 4 lanes (KEYS, BASS, PLUCK, AIR) x 4 takes,
mapped one loop per key on MIDI notes 60-75, Root = key so the sampler never
re-pitches a loop. The plugin time-stretches them to the host tempo.

Outputs:
  hise_project/ResearchFacility/Samples/LL_<kit>_<lane><take>.wav  (48k/16-bit, TPDF dither)
  hise_project/ResearchFacility/SampleMaps/LL_<kit>.xml
  hise_project/ResearchFacility/Scripts/LoopBank.js                (kit metadata)
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_signature_bank as bank  # noqa: E402
import sigbank_dsp as dsp  # noqa: E402

SR = dsp.SR
LANES = ["KEYS", "BASS", "PLUCK", "AIR"]
FIRST_NOTE = 60          # C3-D#4: the Mac keys' and Live keyboard's home octave

# progression degrees (semitones from the kit root) per bar, minor-key friendly
PROGS = {
    "i_VI": [[0, 3, 7, 10], [-4, 0, 3, 7]],          # i7 - VImaj7 (two-chord bed)
    "i_iv": [[0, 3, 7, 10], [5, 8, 12, 15]],         # i7 - iv7
}

# Kit table: id, name, bpm, root midi (for chords), progression, preset per lane, tags
KITS = [
    dict(id="night_drive", name="Night Drive", bpm=72, root=57, key="A minor", prog="i_VI",
         lanes={"KEYS": "drowned_tines", "BASS": "long_glide_808", "PLUCK": "night_celesta", "AIR": "submerged_choir"},
         tags=["underwater", "rnb", "late-night"]),
    dict(id="neon_perreo", name="Neon Perreo", bpm=98, root=54, key="F# minor", prog="i_iv",
         lanes={"KEYS": "perreo_keys", "BASS": "dembow_bass", "PLUCK": "dembow_nylon", "AIR": "neon_haze"},
         tags=["reggaeton", "dembow", "neon"]),
    dict(id="pulse_house", name="Pulse House", bpm=126, root=57, key="A minor", prog="i_VI",
         lanes={"KEYS": "dusk_poly_chords", "BASS": "disco_pulse_bass", "PLUCK": "night_pluck_arp", "AIR": "formant_night_pad"},
         tags=["house", "disco", "chorus"]),
]


# ---------------------------------------------------------------------------
# Loop kit packs: assets/packs/loop_kits/*.json, one kit per file, appended
# after the built-in KITS in file-name order. Fields: id, name, bpm, root (MIDI
# note of the chord root), key (display text), prog (a PROGS name, or a list
# of bars, each a list of semitones from root), lanes {KEYS, BASS, PLUCK, AIR:
# preset id}, tags, optional bars (2 or 4, default 2), and optional patterns
# {lane: [take1..take4]}, where each take is a list of [start_beat,
# length_beats, semitones_from_root, velocity]. A lane without patterns uses
# the built-in pattern() takes.
# ---------------------------------------------------------------------------
KIT_PACK_DIR = Path(__file__).resolve().parents[1] / "assets" / "packs" / "loop_kits"
KIT_MB_CAP = 32.0          # per kit on disk; a 2-bar kit at 72 BPM is ~15 MB at 16-bit
KIT_KEYS = {"id", "name", "bpm", "root", "key", "prog", "lanes", "tags", "bars", "patterns"}
# Retired kits: a saved Live set that names one loads its replacement (KIT_ALIASES in
# LoopBank.js, resolved by findKit). Empty until a kit is retired.
KIT_RETIRED = {}


def load_kit_packs() -> list[dict]:
    out = []
    ids = {p["id"] for p in bank.PRESETS}
    for f in bank.pack_files(KIT_PACK_DIR):
        k = json.loads(f.read_text())
        where = f"{f.name}:{k.get('id', '?')}"
        extra = set(k) - KIT_KEYS
        assert not extra, f"{where}: unknown fields {sorted(extra)}"
        for need in ("id", "name", "bpm", "root", "key", "prog", "lanes", "tags"):
            assert need in k, f"{where}: missing {need}"
        assert 60 <= k["bpm"] <= 180, f"{where}: bpm 60..180"
        assert 36 <= k["root"] <= 72, f"{where}: root MIDI 36..72"
        bars = k.get("bars", 2)
        assert bars in (2, 4), f"{where}: bars is 2 or 4"
        prog = PROGS.get(k["prog"]) if isinstance(k["prog"], str) else k["prog"]
        assert prog, f"{where}: prog must be one of {sorted(PROGS)} or a list of bars"
        assert len(prog) == bars, f"{where}: prog needs {bars} bars"
        assert set(k["lanes"]) == set(LANES), f"{where}: lanes must be {LANES}"
        for ln, pid in k["lanes"].items():
            assert pid in ids, f"{where}: lane {ln} preset {pid} not in the bank"
        for ln, takes in k.get("patterns", {}).items():
            assert ln in LANES and len(takes) == 4, f"{where}: patterns[{ln}] needs 4 takes"
            for ev in (e for tk in takes for e in tk):
                assert len(ev) == 4 and 0 <= ev[0] < bars * 4 and ev[1] > 0 and 1 <= ev[3] <= 127, f"{where}: bad event {ev}"
        k["bars"] = bars
        k["prog_bars"] = prog
        out.append(k)
    return out


def pattern(lane, take, prog, root, beats_per_bar=4):
    """Return note events [(start_beat, length_beats, midi, vel)] for 2 bars."""
    ev = []
    for bar, chord in enumerate(prog):
        b0 = bar * beats_per_bar
        notes = [root + d for d in chord]
        if lane == "KEYS":
            if take == 1:        # held chords
                ev += [(b0, 3.9, n, 70) for n in notes]
            elif take == 2:      # pushed stabs
                for s in (0, 1.5, 3):
                    ev += [(b0 + s, 0.6, n, 78) for n in notes]
            elif take == 3:      # rolled, low then top
                ev += [(b0 + k * 0.08, 3.8, n, 66 - k * 4) for k, n in enumerate(notes)]
            else:                # sparse top voice + root
                ev += [(b0, 3.8, notes[0], 64), (b0 + 2, 1.8, notes[-1] + 12, 60), (b0 + 3, 0.9, notes[2] + 12, 56)]
        elif lane == "BASS":
            r = notes[0] - 24
            if take == 1:
                ev += [(b0, 1.9, r, 100), (b0 + 2.5, 1.4, r, 92)]
            elif take == 2:      # dembow-style 3+3+2
                ev += [(b0, 0.7, r, 104), (b0 + 1.5, 0.45, r, 92), (b0 + 2, 0.7, r, 100), (b0 + 3.5, 0.45, r + 7, 90)]
            elif take == 3:      # octave pops
                for s in range(8):
                    ev.append((b0 + s * 0.5, 0.3, r + (12 if s % 2 else 0), 96 if s % 2 == 0 else 80))
            else:                # whole-note sub
                ev.append((b0, 3.9, r, 96))
        elif lane == "PLUCK":
            arp = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[3] + 12]
            if take == 1:        # 1/8 up
                for s in range(8):
                    ev.append((b0 + s * 0.5, 0.4, arp[s % 4], 84))
            elif take == 2:      # 1/16 up-down
                seq = arp + arp[::-1]
                for s in range(16):
                    ev.append((b0 + s * 0.25, 0.22, seq[s % 8], 80 if s % 4 == 0 else 66))
            elif take == 3:      # dotted-eighth motif
                for k, s in enumerate((0, 0.75, 1.5, 2.5, 3.25)):
                    ev.append((b0 + s, 0.5, arp[k % 4] + (12 if k == 2 else 0), 82))
            else:                # call and answer
                ev += [(b0, 0.9, arp[2], 84), (b0 + 1, 0.4, arp[1], 72), (b0 + 2.5, 1.2, arp[3], 80)]
        else:                    # AIR
            top = [n + 12 for n in notes[1:]]
            if take == 1:
                ev += [(b0, 4.0, n, 60) for n in top]
            elif take == 2:
                ev += [(b0 + 0.5, 3.4, top[0], 58), (b0 + 1.0, 2.9, top[2], 54)]
            elif take == 3:
                ev += [(b0, 4.0, notes[0] + 12, 62), (b0, 4.0, notes[0] + 19, 54)]
            else:
                ev += [(b0 + 2, 2.0, top[1] + 12, 56)]
    return ev


def kit_events(kit, lane, take):
    pats = kit.get("patterns", {})
    if lane in pats:
        return [(e[0], e[1], kit["root"] + e[2], e[3]) for e in pats[lane][take - 1]]
    return pattern(lane, take, kit.get("prog_bars") or PROGS[kit["prog"]], kit["root"])


# lane loudness in K-weighted, gated LUFS (ITU-R BS.1770): sparse lanes are measured on the
# notes, not on the silence between them, so they are no longer pushed into the soft knee
LANE_LUFS = {"KEYS": -12.5, "BASS": -13.5, "PLUCK": -14.0, "AIR": -16.0}   # by ear later; old loops sat near -13 dBFS RMS
_K1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585])
_K2 = ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])


def lufs(l, r):
    """BS.1770 integrated loudness at 48 kHz: K-weighting, 400 ms blocks with 75% overlap,
    absolute gate -70 LUFS, relative gate -10 LU."""
    from scipy.signal import lfilter
    zs = []
    for ch in (l, r):
        y = lfilter(*_K2, lfilter(*_K1, ch))
        zs.append(y * y)
    e = zs[0] + zs[1]
    w, hop = int(0.4 * SR), int(0.1 * SR)
    c = np.concatenate([[0.0], np.cumsum(e)])
    st = np.arange(0, max(1, len(e) - w + 1), hop)
    blk = (c[np.minimum(st + w, len(e))] - c[st]) / w
    lk = -0.691 + 10 * np.log10(blk + 1e-20)
    g = blk[lk > -70.0]
    if g.size == 0:
        return -70.0
    rel = -0.691 + 10 * math.log10(float(np.mean(g))) - 10.0
    g2 = blk[(lk > -70.0) & (lk > rel)]
    return -0.691 + 10 * math.log10(float(np.mean(g2)) + 1e-20)
FLOOR_DBFS = -66.0                 # a loop never drops to digital silence (doc 23 pattern 3)


def tempo_beats(name: str) -> float:
    """'1/8D' -> 0.75 beats (D dotted, T triplet), as the plug-in's delay reads p.dly."""
    m = re.fullmatch(r"1/(\d+)([DT]?)", name.strip())
    if not m:
        return 0.75
    beats = 4.0 / int(m.group(1))
    return beats * (1.5 if m.group(2) == "D" else (2.0 / 3.0 if m.group(2) == "T" else 1.0))


def note_env(n, hold, atk, rel):
    """Preset attack (raised cosine) and release (to -60 dB over rel), plus a 5 ms end fade."""
    env = np.ones(n)
    a = max(int(0.001 * SR), min(int(atk * SR), n))
    env[:a] = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, a))
    if hold < n:
        t = np.arange(n - hold) / SR
        env[hold:] *= np.exp(-6.907755 * t / max(rel, 0.02))
    fo = min(n, int(0.005 * SR))
    env[-fo:] *= np.linspace(1.0, 0.0, fo)
    return env


def cadd(buf, s0, v):
    """Add v into the circular buffer at s0 (negative starts and long tails wrap)."""
    nb_ = len(buf)
    s0 %= nb_
    e = s0 + len(v)
    if e <= nb_:
        buf[s0:e] += v
    else:
        k = nb_ - s0
        buf[s0:] += v[:k]
        buf[: e - nb_] += v[k:]


def voice_lane(p, l, r, n_loop, rng):
    """The lane through its preset's own voicing, as the plug-in's master FX would play it
    (doc 23 pattern 1): GRIT, TONE (ladder LP), WIDTH (chorus on mono lanes), ECHO at the
    preset's tempo division, SPACE. Run over repeated loops and keep the last one, so every
    tail wraps onto beat 1 in steady state."""
    m, v = p["m"], p["v"]
    tone, width, space, echo, grit = m[0], m[3], m[4], m[5], m[6]
    reps = int(min(10, 1 + math.ceil(6.0 * SR / n_loop)))
    L = np.tile(l, reps)
    R = np.tile(r, reps)
    if grit > 0.01:
        L = dsp.saturate(L, grit * 0.85, min(1.0, grit * 1.6))
        R = dsp.saturate(R, grit * 0.85, min(1.0, grit * 1.6))
    if tone < 19000:
        q = float(np.clip((v["reso"] - 0.7) * 0.5, 0.0, 0.4))
        L = dsp.lp24(L, tone, q)
        R = dsp.lp24(R, tone, q)
    mono = float(np.max(np.abs(l - r))) < 1e-6
    if mono or width > 0.3:
        # chorus rate rounded to whole cycles per loop: the seam stays continuous
        loop_s = n_loop / SR
        rate = max(1, round(0.35 * loop_s)) / loop_s
        cl, cr = dsp.short_chorus((L + R) * 0.5, rng, depth_ms=1.5 + 3.0 * width, rate=rate)
        mix = 0.5 if mono else 0.25 * width
        L = L * (1.0 - mix) + cl * mix
        R = R * (1.0 - mix) + cr * mix
    spb = 60.0 / p["_bpm"]
    if echo > 0.01:
        L, R = dsp.tempo_delay(L, R, tempo_beats(v["dly"]) * spb, 0.15 + echo * 0.4, 0.12 + echo * 0.38, echo * 0.45)
    if space > 0.01:
        tn = float(np.clip((math.log(tone) - 4.38) / 5.52, 0.0, 1.0))
        L, R = dsp.juce_reverb(L, R, 0.45 + space * 0.5, 0.75 + (0.25 - 0.75) * tn, space * 0.55, dry=0.9,
                               width=min(1.0, 0.4 + width * 0.6))
    return L[-n_loop:], R[-n_loop:]


def render_loop(kit, lane, take):
    pid = kit["lanes"][lane]
    p = dict(next(x for x in bank.PRESETS if x["id"] == pid))
    p["_bpm"] = kit["bpm"]
    spb = 60.0 / kit["bpm"]
    n_loop = int(round(kit.get("bars", 2) * 4 * spb * SR))
    v = p["v"]
    atk = min(1.5, v["atk"] / 1000.0)
    rel = min(4.0, v["rel"] / 1000.0)
    gen_atk = float(p["gp"].get("attack", 0.0) or 0.0)
    # slow swells start early so they bloom on the beat (doc 23 pattern 7)
    pre = 0.6 * (gen_atk + atk) if lane == "AIR" and gen_atk + atk >= 0.25 else 0.0
    max_note = 8.5 + pre
    n_wraps = 1 + int(math.ceil(max_note * SR / n_loop))
    n_buf = n_loop * n_wraps
    buf_l = np.zeros(n_buf)
    buf_r = np.zeros(n_buf)
    soft_gp = bank.soften(p["gen"], p["gp"])
    for i, (start, length, note, vel) in enumerate(kit_events(kit, lane, take)):
        # every event its own voice (doc 23 pattern 6: 39% replayed one identical sample)
        rng = np.random.default_rng(bank.seed_for(f"{kit['id']}:{lane}:{take}:{i}", int(note)))
        hold_s = length * spb
        dur = min(hold_s + rel + 0.15, 8.5)
        n = int(dur * SR)
        gp = soft_gp if vel < 80 else p["gp"]          # quiet notes are darker, not only quieter
        detune = float(rng.normal(0.0, 0.03))           # about 3 cents
        l, r = bank.render_voice(p, gp, note + detune, n, rng)
        env = note_env(n, int(hold_s * SR), atk, rel)
        g = (vel / 127.0) ** 1.4
        jit = int(rng.uniform(-0.0015, 0.0015) * SR)
        s0 = int((start * spb - pre) * SR) + jit
        cadd(buf_l, s0, l * env * g)
        cadd(buf_r, s0, r * env * g)
    loop_l = buf_l.reshape(n_wraps, n_loop).sum(axis=0)
    loop_r = buf_r.reshape(n_wraps, n_loop).sum(axis=0)
    vrng = np.random.default_rng(bank.seed_for(f"{kit['id']}:{lane}:{take}:fx", 0))
    loop_l, loop_r = voice_lane(p, loop_l, loop_r, n_loop, vrng)
    # HISE's time-stretch output is x0.5 (doc 15), hence the hot targets
    gain = 10 ** ((LANE_LUFS[lane] - lufs(loop_l, loop_r)) / 20.0)
    pk = max(float(np.abs(loop_l).max()), float(np.abs(loop_r).max()), 1e-9)
    gain = min(gain, 1.25 / pk)                   # peaks at most ~2 dB into the knee: sparse plucks stay clean
    out_l, out_r = soft_knee(loop_l * gain), soft_knee(loop_r * gain)
    # a floor of soft hiss: the loop never drops to digital silence
    frng = np.random.default_rng(bank.seed_for(f"{kit['id']}:{lane}:{take}:floor", 0))
    fl = 10 ** (FLOOR_DBFS / 20.0)
    for ch in (out_l, out_r):
        hiss = dsp.svf(frng.standard_normal(n_loop), 5000.0, 0.6, 0)
        ch += hiss / (float(np.std(hiss)) + 1e-12) * fl
    return out_l, out_r


def soft_knee(x, knee=0.5, ceil=0.95):
    """Peaks above the knee bend smoothly toward the ceiling (tanh), below it nothing changes.
    A hard peak cap after RMS normalisation left peaky one-shot lanes (cowbell, plucks) 7-10 dB
    under sustained lanes; the knee keeps their loudness and only rounds the transient tips."""
    a = np.abs(x)
    over = a > knee
    y = x.copy()
    y[over] = np.sign(x[over]) * (knee + (ceil - knee) * np.tanh((a[over] - knee) / (ceil - knee)))
    return y


def main() -> int:
    kits_meta = []
    all_kits = KITS + load_kit_packs()
    assert len({k["id"] for k in all_kits}) == len(all_kits), "duplicate loop kit id"
    for kit in all_kits:
        entries = []
        for li, lane in enumerate(LANES):
            for take in range(1, 5):
                note = FIRST_NOTE + li * 4 + (take - 1)
                fname = f"LL_{kit['id']}_{lane.lower()}{take}.wav"
                l, r = render_loop(kit, lane, take)
                rng = np.random.default_rng(bank.seed_for(fname, note))
                bank.write_wav16(bank.SAMPLES / fname, l, r, rng)     # 16-bit: 60+ kits must fit on disk
                (bank.SAMPLES / (fname + ".meta.json")).write_text(json.dumps({
                    "filename": fname,
                    "source": {"license": "research-facility-original", "uploader": "Research Facility procedural synthesis",
                               "url": "", "generator": "scripts/build_loop_lines.py"},
                    "musical": {"kit": kit["name"], "lane": lane, "take": take, "bpm": kit["bpm"], "key": kit["key"]},
                }, indent=2))
                n = len(l)
                entries.append(
                    f'  <sample ID="{len(entries)}" FileName="{{PROJECT_FOLDER}}{fname}" Root="{note}" HiKey="{note}"\n'
                    f'          LoKey="{note}" LoVel="0" HiVel="127" RRGroup="1" Volume="0" Pan="0"\n'
                    f'          Normalized="0" Pitch="0" SampleStart="0" SampleEnd="{n}" SampleStartMod="0"\n'
                    f'          LoopStart="0" LoopEnd="{n}" LoopXFade="0" LoopEnabled="1"\n'
                    f'          LowerVelocityXFade="0" UpperVelocityXFade="0" SampleState="0"\n'
                    f'          NormalizedPeak="-1" Duplicate="0"/>')
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n\n'
               f'<samplemap ID="LL_{kit["id"]}" SaveMode="1" RRGroupAmount="1.0" MicPositions=";"\n'
               '           CrossfadeGamma="1.0">\n' + "\n".join(entries) + "\n</samplemap>\n")
        (bank.MAPS / f"LL_{kit['id']}.xml").write_text(xml)
        kits_meta.append({"id": kit["id"], "name": kit["name"], "bpm": kit["bpm"], "key": kit["key"],
                          "map": f"LL_{kit['id']}", "quarters": kit.get("bars", 2) * 4, "tags": kit["tags"],
                          "lanes": [kit["lanes"][ln] for ln in LANES]})
        kit_mb = sum((bank.SAMPLES / f"LL_{kit['id']}_{ln.lower()}{tk}.wav").stat().st_size
                     for ln in LANES for tk in range(1, 5)) / 1e6
        assert kit_mb <= KIT_MB_CAP, f"kit {kit['id']}: {kit_mb:.1f} MB > {KIT_MB_CAP} MB cap (fewer bars or faster tempo)"
        print(f"kit {kit['name']}: 16 loops at {kit['bpm']} BPM, {kit_mb:.1f} MB", flush=True)
    js = ["// AUTO-GENERATED by scripts/build_loop_lines.py - do not edit by hand.",
          "// Loop Lines kits: 4 lanes x 4 takes on MIDI notes 60-75 (lane = (note-60)/4).",
          "const var LOOP_LANES = " + json.dumps(LANES) + ";",
          "const var LOOP_FIRST_NOTE = " + str(FIRST_NOTE) + ";",
          "const var KIT_ALIASES = " + json.dumps(KIT_RETIRED) + ";",
          "const var LOOP_KITS = " + json.dumps(kits_meta) + ";"]
    (bank.SCRIPTS / "LoopBank.js").write_text("\n".join(js) + "\n")
    print("LoopBank.js written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
