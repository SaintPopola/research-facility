#!/usr/bin/env python3
"""
Sweet Melody - Loop Lines builder (Arcade-style loops mode, v1).

Renders original 2-bar loops from the plugin's own synthesis recipes
(scripts/build_signature_bank.py presets), at the tempos/keys of the playlist
DNA (docs/12, docs/15). Each kit = 4 lanes (KEYS, BASS, PLUCK, AIR) x 4 takes,
mapped one loop per key on MIDI notes 48-63, Root = key so the sampler never
re-pitches a loop. The plugin time-stretches them to the host tempo.

Outputs:
  hise_project/ResearchFacility/Samples/LL_<kit>_<lane><take>.wav  (48k/16-bit, TPDF dither)
  hise_project/ResearchFacility/SampleMaps/LL_<kit>.xml
  hise_project/ResearchFacility/Scripts/LoopBank.js                (kit metadata)
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_signature_bank as bank  # noqa: E402
import sigbank_dsp as dsp  # noqa: E402

SR = dsp.SR
LANES = ["KEYS", "BASS", "PLUCK", "AIR"]
FIRST_NOTE = 48

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


def load_kit_packs() -> list[dict]:
    out = []
    ids = {p["id"] for p in bank.PRESETS}
    for f in sorted(KIT_PACK_DIR.glob("*.json")):
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


def render_loop(kit, lane, take):
    pid = kit["lanes"][lane]
    p = next(x for x in bank.PRESETS if x["id"] == pid)
    spb = 60.0 / kit["bpm"]
    n_loop = int(round(kit.get("bars", 2) * 4 * spb * SR))
    n_buf = n_loop * 2                         # one extra loop of room for tails
    buf_l = np.zeros(n_buf)
    buf_r = np.zeros(n_buf)
    cache = {}
    for start, length, note, vel in kit_events(kit, lane, take):
        dur = min(length * spb + 1.5, 6.0)
        n = int(dur * SR)
        key = (note, n)
        if key not in cache:
            rng = np.random.default_rng(bank.seed_for(pid + "_loop", note))
            cache[key] = bank.render_voice(p, p["gp"], note, n, rng)
        l, r = cache[key]
        hold = int(length * spb * SR)
        env = np.ones(n)
        rel = int(min(0.25, 0.6 * length * spb + 0.05) * SR)
        if hold + rel < n:
            env[hold:hold + rel] = np.linspace(1.0, 0.0, rel)
            env[hold + rel:] = 0.0
        g = (vel / 127.0) ** 1.4
        s0 = int(start * spb * SR)
        e0 = min(n_buf, s0 + n)
        buf_l[s0:e0] += l[: e0 - s0] * env[: e0 - s0] * g
        buf_r[s0:e0] += r[: e0 - s0] * env[: e0 - s0] * g
    # fold the tail onto the head: seamless loop, beat 1 at sample 0
    loop_l = buf_l[:n_loop] + buf_l[n_loop:]
    loop_r = buf_r[:n_loop] + buf_r[n_loop:]
    rms = math.sqrt(float(np.mean((loop_l ** 2 + loop_r ** 2) * 0.5))) + 1e-12
    gain = 0.22 / rms                           # +6 dB: HISE time-stretch output is x0.5 (doc 15)
    loop_l *= gain
    loop_r *= gain
    peak = max(np.abs(loop_l).max(), np.abs(loop_r).max())
    if peak > 0.9:
        loop_l *= 0.9 / peak
        loop_r *= 0.9 / peak
    return loop_l, loop_r


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
          "// Loop Lines kits: 4 lanes x 4 takes on MIDI notes 48-63 (lane = (note-48)/4).",
          "const var LOOP_LANES = " + json.dumps(LANES) + ";",
          "const var LOOP_FIRST_NOTE = " + str(FIRST_NOTE) + ";",
          "const var LOOP_KITS = " + json.dumps(kits_meta) + ";"]
    (bank.SCRIPTS / "LoopBank.js").write_text("\n".join(js) + "\n")
    print("LoopBank.js written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
