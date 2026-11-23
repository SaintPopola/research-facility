#!/usr/bin/env python3
"""
Research Facility - Signature Bank builder.

Renders the factory "Signature Bank": 41 original, melody-ready instruments
(keys, pads, plucks, leads, bells, vox, bass) inspired by the production
styles documented in docs/SIGNATURE_SOUNDS_RESEARCH.md. Every sample is
synthesised from scratch by scripts/sigbank_dsp.py: no recordings, no
third-party presets, no producer or artist names in preset names.

Outputs (all deterministic, seeded per preset):
  hise_project/ResearchFacility/Samples/SIG_<id>_<note>.wav (+ .meta.json)
  hise_project/ResearchFacility/SampleMaps/SIG_<id>.xml      (multisample map)
  hise_project/ResearchFacility/Scripts/FactoryBank.js       (embedded browser data)
  assets/presets/signature_bank.json                          (docs / storefront)

Usage:
  python3 scripts/build_signature_bank.py              # render everything
  python3 scripts/build_signature_bank.py --data-only  # only rewrite FactoryBank.js + json
  python3 scripts/build_signature_bank.py --only drowned_tines
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import wave
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sigbank_dsp as dsp  # noqa: E402
import flagship_dsp as fdsp  # noqa: E402  (docs/27 flagship generators)

dsp.GENERATORS["moog_core"] = fdsp.gen_moog_core
dsp.GENERATORS["poly_divide"] = fdsp.gen_poly_divide
dsp.GENERATORS["tine_v2"] = fdsp.gen_tine_v2
dsp.GENERATORS["fork"] = fdsp.gen_fork
dsp.GENERATORS["cs_dual"] = fdsp.gen_cs_dual
dsp.GENERATORS["easel_cx"] = fdsp.gen_easel_cx
dsp.GENERATORS["tape_frame"] = fdsp.gen_tape_frame

SR = dsp.SR
ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "hise_project" / "ResearchFacility"
SAMPLES = PROJ / "Samples"
MAPS = PROJ / "SampleMaps"
SCRIPTS = PROJ / "Scripts"
ASSETS = ROOT / "assets" / "presets"

DEFAULT_PRESET = "drowned_tines"

# Browser categories (order = tab order) and their display names.
CATEGORIES = [
    ("keys", "KEYS"), ("chords", "CHORDS"), ("pads", "PADS"), ("guitar", "GUITAR"),
    ("plucks", "PLUCKS"), ("leads", "LEADS"), ("bells", "BELLS"), ("vox", "VOX"),
    ("bass", "BASS"), ("archive", "ARCHIVE"),
]

# Vibe chips shown in the browser (must appear in preset tags).
VIBES = ["underwater", "rnb", "lofi", "slowed", "reggaeton", "house",
         "future-bass", "808", "chorus", "dark", "lush", "vocal-chop"]

# ---------------------------------------------------------------------------
# Preset table.
#   m   = macros [TONE Hz, BODY, MOTION, WIDTH, SPACE, ECHO, GRIT, PUMP] (0..1 except TONE)
#   v   = voicing: atk/rel ms, reso (filter Q), vel (velocity depth 0..1),
#         lfo (filter LFO Hz), dly (echo tempo), subdec ms / subsus dB (sub
#         layer envelope), trim dB
#   z   = zones (lowest root, highest root, step semitones)
#   dur = seconds per sample, loop = sustain loop
# ---------------------------------------------------------------------------

def P(id, name, cat, tags, gen, gp, m, v, z, dur, loop, desc, vl=1, d=None, mod=None, rr=1):
    """vl = velocity layers (1 or 2). Layer 1 (soft) is rendered with a gentler
    excitation from soften(); layer 2 is the recipe as written.
    d = optional SHAPE-page values {componentId: value}, checked against
    scripts/deep_params.json (missing ids keep the registry default).
    mod = optional mod-matrix rows [{"Source", "Target", "Intensity", "Mode", "Inverted"}]."""
    return dict(id=id, name=name, cat=cat, tags=tags, gen=gen, gp=gp, m=m, v=v,
                z=z, dur=dur, loop=loop, desc=desc, vl=vl, d=d or {}, mod=mod or [], rr=rr)


def V(atk=5, rel=600, reso=0.9, vel=0.5, lfo=0.2, dly="1/8D", subdec=1200, subsus=-30, trim=0.0):
    return dict(atk=atk, rel=rel, reso=reso, vel=vel, lfo=lfo, dly=dly,
                subdec=subdec, subsus=subsus, trim=trim)


PRESETS = [
    # ================================================================ SWEET MELODY P1
    # docs/12_playlist_presets.json priority 1, interim synth recipes. Velocity
    # layer 1 is a softened render; one gain per instrument; 48 kHz / 24-bit.
    P("drowned_tines", "Drowned Tines", "keys", ["underwater", "rnb", "late-night", "lofi", "two-chord"],
      "tine_ep", dict(t60=6.0, bark=0.9, tine=0.15, tine_ratio=7.11, pickup=0.30, wow=5.0, lp=2200,
                      decim=11025, decim_drive=0.08, post_hp=220),
      [2200, 0.15, 0.35, 0.60, 0.60, 0.30, 0.10, 0.0],
      V(atk=6, rel=1300, reso=0.9, vel=0.55, lfo=0.15, dly="1/4D", subdec=1600, subsus=-30),
      (36, 96, 6), 4.5, False,
      "Tine piano with highs and lows cut, slow tape wobble and a dark halo. Two-chord beds.", vl=2),
    P("half_speed_keys", "Half-Speed Keys", "keys", ["slowed", "reverb", "tape", "dreamy"],
      "tine_ep", dict(t60=7.0, bark=0.8, tine=0.12, pickup=0.25, wow=8.0, wow_rate=0.3, lp=2600, slow=0.85),
      [2000, 0.20, 0.25, 0.70, 0.75, 0.20, 0.10, 0.0],
      V(atk=8, rel=2000, reso=0.9, vel=0.5, lfo=0.1, dly="1/4D", subsus=-30),
      (36, 96, 6), 4.5, False,
      "Keys printed to tape at 0.85x: slower wobble, darker top. Sits with slowed tracks.", vl=2),
    P("hushed_felt_grand", "Hushed Felt Grand", "keys", ["piano", "romantic", "ballad", "late-night"],
      "felt_piano", dict(hardness=0.25, t60=7.0, unison_c=1.0, lp=4200, wow=1.5, post_shelf=(7000, -3.0)),
      [5000, 0.0, 0.05, 0.50, 0.45, 0.08, 0.0, 0.0],
      V(atk=3, rel=1000, reso=0.7, vel=0.75, lfo=0.1, dly="1/8D", subsus=-40),
      (24, 108, 4), 5.5, False,
      "Soft, close felt piano with the top rolled off. Ballads and slow trap-soul.", vl=2),
    P("syrup_tine", "Syrup Tine", "keys", ["rnb", "neo-soul", "warm", "chorus"],
      "tine_ep", dict(t60=5.0, bark=1.3, tine=0.22, pickup=0.45, wow=2.5, lp=4500),
      [3500, 0.20, 0.45, 0.65, 0.35, 0.12, 0.20, 0.0],
      V(atk=3, rel=700, reso=0.8, vel=0.65, lfo=0.25, dly="1/8D", subsus=-30),
      (36, 96, 6), 4.0, False,
      "Warm, barky tine piano with chorus and light drive. Neo-soul comping.", vl=2),
    P("dusk_poly_chords", "Dusk Poly Chords", "chords", ["synth-pop", "chorus", "stabs", "analog"],
      "supersaw", dict(voices=2, pulse=1, detune_c=8, sub=0.25, lp=2200, reso=0.15, keytrack=0.4,
                       attack=0.008, decay=0.6, sustain=0.6),
      [2200, 0.25, 0.40, 0.80, 0.35, 0.12, 0.10, 0.20],
      V(atk=5, rel=350, reso=1.0, vel=0.45, lfo=0.25, dly="1/8D", subsus=-12),
      (36, 96, 6), 3.0, True,
      "Saw plus pulse plus sub with thick chorus. Chord stabs or held beds.", vl=2),
    P("pump_saw_stab", "Pump Saw Stab", "chords", ["future-beats", "supersaw", "house", "future-bass"],
      "supersaw", dict(voices=7, detune_c=22, lp=1200, keytrack=0.5, fenv=4500, fenv_t=0.30, t60=1.8, attack=0.003),
      [9000, 0.15, 0.35, 0.85, 0.35, 0.18, 0.30, 0.60],
      V(atk=1, rel=300, reso=0.9, vel=0.45, lfo=0.3, dly="1/8D"),
      (36, 96, 6), 2.5, False,
      "Wide supersaw stab with a snappy filter, ducking to the beat. House chords.", vl=2),
    P("chorus_jangle_clean", "Chorus Jangle Clean", "guitar", ["jangle", "bedroom", "clean", "chorus"],
      "karplus", dict(t60=2.4, bright=5000, damp=0.4, pos=0.15, body=0.35, chorus=1, post_shelf=(5000, 1.5)),
      [6000, 0.0, 0.40, 0.60, 0.30, 0.15, 0.10, 0.0],
      V(atk=1, rel=400, reso=0.8, vel=0.7, lfo=0.2, dly="1/8D", subsus=-40),
      (40, 88, 3), 3.0, False,
      "Clean single-coil style guitar through soft chorus and a plate. Bedroom-pop jangle.", vl=2),
    P("five_take_steel", "Five-Take Steel Acoustic", "guitar", ["acoustic", "steel", "stacked", "indie-folk"],
      "karplus", dict(t60=3.0, bright=7000, damp=0.25, pos=0.12, chorus=1),
      [9000, 0.0, 0.10, 0.85, 0.25, 0.05, 0.0, 0.0],
      V(atk=1, rel=700, reso=0.7, vel=0.7, lfo=0.15, dly="1/4D", subsus=-40),
      (40, 88, 4), 3.5, False,
      "Picked steel-string guitar spread wide, open strings ringing. Verse to big chorus.", vl=2),
    P("porch_nylon", "Porch Nylon", "guitar", ["nylon", "sad-trap", "latin", "warm"],
      "karplus", dict(t60=2.6, bright=3200, body=0.6, pos=0.22, chorus=1),
      [5500, 0.0, 0.20, 0.50, 0.30, 0.15, 0.05, 0.0],
      V(atk=1, rel=500, reso=0.8, vel=0.65, lfo=0.2, dly="1/8", subsus=-40),
      (40, 88, 4), 3.0, False,
      "Warm nylon pluck with a woody body. Sad-trap loops and Latin ostinatos.", vl=2),
    P("spring_surf_strum", "Spring Surf Strum", "guitar", ["surf", "punk", "spring", "bright"],
      "karplus", dict(t60=1.8, bright=6500, damp=0.3, pos=0.12, chorus=0),
      [7000, 0.0, 0.10, 0.45, 0.30, 0.05, 0.30, 0.0],
      V(atk=1, rel=250, reso=0.8, vel=0.7, lfo=0.2, dly="1/8", subsus=-40),
      (40, 88, 4), 2.5, False,
      "Bright, slightly driven guitar for fast surf punk and bedroom indie.", vl=2),
    P("night_celesta", "Night Celesta", "bells", ["celesta", "glass", "late-night", "rnb"],
      "modal", dict(modes=[(1, 1, 1), (4.0, 0.22, 0.3), (10.0, 0.05, 0.08)], t60=2.4, strike=0.2, lp=7000, post_hp=200),
      [9000, 0.0, 0.25, 0.70, 0.50, 0.25, 0.0, 0.0],
      V(atk=1, rel=1000, reso=0.7, vel=0.6, lfo=0.2, dly="1/8D", subsus=-40),
      (48, 96, 6), 3.0, False,
      "Glassy celesta, bright but small. Sparse high arpeggios above the vocal.", vl=2),
    P("boogie_keytar", "Boogie Keytar", "leads", ["boogie", "funk", "keytar", "lead"],
      "supersaw", dict(voices=2, pulse=1, detune_c=7, lp=900, reso=0.2, fenv=2600, fenv_t=0.38,
                       attack=0.003, decay=0.6, sustain=0.8),
      [5000, 0.0, 0.30, 0.40, 0.20, 0.20, 0.25, 0.0],
      V(atk=3, rel=150, reso=1.1, vel=0.5, lfo=0.3, dly="1/8D", subsus=-20),
      (36, 96, 6), 2.5, True,
      "Saw-plus-pulse lead with a snappy filter. Boogie answer phrases.", vl=2),
    P("bubble_reed_call", "Bubble Reed Call", "leads", ["sax", "reed", "echo", "call"],
      "voice", dict(singers=1, vowels=["o"], vib_c=12, vib_delay=0.3, breath=0.22, attack=0.04, lp=3200),
      [4000, 0.0, 0.25, 0.55, 0.55, 0.50, 0.20, 0.0],
      V(atk=40, rel=350, reso=0.9, vel=0.5, lfo=0.2, dly="1/4D", subsus=-20),
      (48, 84, 4), 3.0, True,
      "Breathy sax-like call soaked in ping-pong echo.", vl=2),
    P("velvet_swell_strings", "Velvet Swell Strings", "pads", ["strings", "cinematic", "swell", "emotional"],
      "supersaw", dict(voices=7, detune_c=12, drift_c=4, lp=2800, keytrack=0.5, hp=160, attack=0.6, sustain=1.0,
                       vib_c=8, vib_rate=5.2, vib_delay=0.8),
      [3000, 0.15, 0.30, 0.80, 0.60, 0.05, 0.0, 0.0],
      V(atk=600, rel=1800, reso=0.8, vel=0.4, lfo=0.15, dly="1/8D", subsus=-12),
      (36, 96, 6), 5.0, True,
      "Ensemble saw strings with a slow swell, delayed vibrato and a soft top."),
    P("wonky_analog_poly", "Wonky Analog Poly", "pads", ["french-touch", "chorus", "detuned", "house"],
      "supersaw", dict(voices=3, detune_c=16, drift_c=9, lp=2600, keytrack=0.5, attack=0.08, decay=1.0, sustain=0.75),
      [2500, 0.20, 0.50, 0.85, 0.40, 0.15, 0.15, 0.35],
      V(atk=30, rel=600, reso=1.1, vel=0.4, lfo=0.3, dly="1/8D", subsus=-12),
      (36, 96, 6), 3.5, True,
      "Slightly out-of-tune, heavily chorused brassy poly that ducks to the beat."),
    P("angel_stretch_cloud", "Angel Stretch Cloud", "vox", ["vocal", "stretched", "cloud", "lush"],
      "voice", dict(singers=3, vowels=["a", "o"], vib_c=6, spread_c=6, breath=0.08, attack=0.7, lp=5500),
      [5500, 0.0, 0.35, 0.85, 0.70, 0.35, 0.05, 0.0],
      V(atk=250, rel=1800, reso=0.8, vel=0.3, lfo=0.1, dly="1/4D", subsus=-30),
      (55, 86, 3), 6.0, True,
      "Stretched, floating 'ooh-ah' cloud. In cloud rap it is the lead instrument.", vl=2),
    P("voice_memo_chop", "Voice-Memo Chop", "vox", ["vocal-chop", "house", "fragment", "pitched"],
      "voice", dict(singers=1, vowels=["a", "o"], t60=0.45, attack=0.003, vib_c=0, breath=0.03, post_hp=250),
      [8000, 0.0, 0.15, 0.50, 0.30, 0.20, 0.05, 0.30],
      V(atk=1, rel=120, reso=0.8, vel=0.5, lfo=0.3, dly="1/8D"),
      (48, 84, 3), 1.0, False,
      "Short pitched 'ah' chop. Play it like a lead for house hooks.", vl=2),
    P("long_glide_808", "Long Glide 808", "bass", ["808", "trap", "glide", "sub"],
      "808", dict(drop_st=7, drop_t=0.045, t60=3.0, drive=1.6, click=0.12),
      [18000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0],
      V(atk=1, rel=250, reso=0.7, vel=0.35, lfo=0.1, subdec=200, subsus=-40),
      (24, 60, 6), 3.5, False,
      "Clean, long sine 808 with a short pitch thump and soft drive."),
    P("disco_pulse_bass", "Disco Pulse Bass", "bass", ["disco", "boogie", "funk", "house"],
      "reese", dict(detune_c=3, lp=450, reso=0.3, sub=0.5, drive=1.6, attack=0.002, decay=0.25, sustain=0.4),
      [4000, 0.10, 0.0, 0.0, 0.0, 0.0, 0.30, 0.20],
      V(atk=1, rel=80, reso=1.2, vel=0.6, lfo=0.1, dly="1/8", subdec=200, subsus=-40),
      (24, 60, 3), 2.5, True,
      "Busy plucky bass with a short filter snap. Disco, boogie and house.", vl=2),

    # ================================================================ SWEET MELODY P2 / P3
    P("phone_808", "Phone 808", "bass", ["808", "distorted", "plugg", "lofi"],
      "808", dict(drop_st=12, drop_t=0.04, t60=2.5, drive=3.0, click=0.2, decim=16000, decim_drive=0.1),
      [9000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.0],
      V(atk=1, rel=220, reso=0.7, vel=0.35, lfo=0.1, subdec=200, subsus=-40),
      (24, 60, 6), 3.0, False, "Saturated, slightly crushed 808 that reads on small speakers. Plugg and lo-fi.", vl=2),
    P("dotted_echo_arp", "Dotted Echo Arp", "plucks", ["delay", "arpeggio", "anthem", "clean"],
      "karplus", dict(t60=2.0, bright=5500, damp=0.4, pos=0.15, body=0.3, chorus=1),
      [6500, 0.0, 0.30, 0.70, 0.40, 0.75, 0.10, 0.0],
      V(atk=1, rel=500, reso=0.8, vel=0.65, lfo=0.2, dly="1/8D", subsus=-40),
      (40, 88, 4), 2.5, False, "Clean guitar arp multiplied by a dotted-eighth echo into a cascade.", vl=2),
    P("night_pluck_arp", "Night Pluck Arp", "plucks", ["house", "arp", "pluck", "nocturnal"],
      "supersaw", dict(voices=2, pulse=1, detune_c=4, lp=700, fenv=4000, fenv_t=0.18, t60=0.7, attack=0.001),
      [2500, 0.0, 0.30, 0.70, 0.45, 0.35, 0.05, 0.30],
      V(atk=1, rel=250, reso=0.9, vel=0.55, lfo=0.3, dly="1/8D"),
      (36, 96, 6), 1.2, False, "Hollow square pluck for 1/16 arpeggios in melodic house.", vl=2),
    P("round_walking_sub", "Round Walking Sub", "bass", ["sub", "afrobeats", "cumbia", "round"],
      "sub", dict(h2=0.12, sustain=0.85, drive=1.0),
      [12000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.10, 0.15],
      V(atk=3, rel=120, reso=0.7, vel=0.4, lfo=0.1, subdec=200, subsus=-40),
      (24, 60, 6), 2.0, True, "Round sine-plus-harmonic sub that follows the roots. Afrobeats, cumbia, bedroom pop.", vl=2),
    P("wood_bass_pluck", "Wood Bass Pluck", "bass", ["upright", "pizzicato", "fingered", "organic"],
      "karplus", dict(t60=2.0, bright=1200, damp=0.55, body=0.8, pos=0.2, lp=2500),
      [2500, 0.10, 0.0, 0.0, 0.10, 0.0, 0.15, 0.0],
      V(atk=1, rel=200, reso=0.8, vel=0.65, lfo=0.1, dly="1/8", subsus=-40),
      (28, 60, 3), 2.5, False, "Woody plucked low string: a thump, then a soft decay. Upright or fingered bass.", vl=2),
    P("cloud_fm_bell", "Cloud FM Bell", "bells", ["fm", "plugg", "cloud", "digital"],
      "fm_bell", dict(ratio=3.5, index=2.5, index_t=0.45, t60=3.5, beat_c=2.0, partial2=0.2, decim=22050),
      [6000, 0.0, 0.30, 0.75, 0.60, 0.35, 0.05, 0.0],
      V(atk=1, rel=1200, reso=0.7, vel=0.6, lfo=0.2, dly="1/4D", subsus=-40),
      (48, 96, 6), 4.0, False, "FM bell at a 3.5 ratio with light digital grain. Cloud-rap motifs.", vl=2),
    P("bakelite_upright", "Bakelite Upright", "keys", ["vintage", "radio", "mono", "lounge"],
      "felt_piano", dict(hardness=0.3, t60=6.0, lp=3000, wow=7.0, decim=8000, decim_drive=0.2, post_hp=300),
      [3800, 0.0, 0.20, 0.05, 0.20, 0.0, 0.45, 0.0],
      V(atk=4, rel=900, reso=0.8, vel=0.6, lfo=0.1, dly="1/8D", subsus=-40),
      (36, 96, 6), 4.0, False, "A piano heard through an old radio: narrow band, mono, wow.", vl=2),
    P("lounge_drawbar_organ", "Lounge Drawbar Organ", "keys", ["organ", "soul", "combo", "vibrato"],
      "organ", dict(bars=[(0.5, 0.4), (1, 1), (2, 0.55), (3, 0.35), (4, 0.2)], wow=3.0, lp=4000),
      [4000, 0.10, 0.60, 0.40, 0.25, 0.05, 0.30, 0.0],
      V(atk=8, rel=120, reso=0.8, vel=0.25, lfo=0.3, dly="1/8", subsus=-12),
      (36, 96, 6), 3.0, True, "Soft soul drawbar organ with vibrato and gentle drive. Pumping stabs."),
    P("wobble_reed_keys", "Wobble Reed Keys", "keys", ["bedroom", "reed", "tape", "soft-rock"],
      "reed_ep", dict(t60=3.5, wow=6.0, drive=1.6, lp=2600, decim=12000, decim_drive=0.05),
      [2600, 0.15, 0.50, 0.55, 0.40, 0.15, 0.25, 0.0],
      V(atk=3, rel=600, reso=1.0, vel=0.6, lfo=0.22, dly="1/8D"),
      (36, 96, 6), 3.5, False, "Reed piano with bite, tape wow and a dull top. Bedroom-pop and soft-rock chords.", vl=2),
    P("brass_sigh_lead", "Brass Sigh Lead", "leads", ["brass", "trumpet", "counter-melody", "soft"],
      "supersaw", dict(voices=2, detune_c=5, lp=800, fenv=1800, fenv_t=0.25, drive=1.6, attack=0.03, sustain=0.9,
                       vib_c=10, vib_rate=5.5, vib_delay=0.5),
      [3500, 0.0, 0.20, 0.40, 0.40, 0.25, 0.30, 0.0],
      V(atk=25, rel=200, reso=1.0, vel=0.55, lfo=0.2, dly="1/4", subsus=-20),
      (48, 84, 6), 3.0, True, "Soft trumpet-like brass with a slow swell and delayed vibrato. Counter-melodies.", vl=2),
    P("fat_mono_line", "Fat Mono Line", "leads", ["mono", "analog", "resonant", "synth-pop"],
      "supersaw", dict(voices=2, detune_c=7, lp=700, reso=0.35, fenv=2400, fenv_t=0.3, drive_pre=1.5,
                       attack=0.002, sustain=0.7),
      [3000, 0.20, 0.10, 0.25, 0.15, 0.08, 0.30, 0.0],
      V(atk=2, rel=80, reso=1.4, vel=0.5, lfo=0.2, dly="1/8", subsus=-10),
      (36, 84, 6), 2.0, True, "Fat two-saw mono line with resonant bite. Counter-melodies and bass doubles.", vl=2),
    P("formant_night_pad", "Formant Night Pad", "pads", ["formant", "ethereal", "vowel", "air"],
      "voice", dict(singers=5, vowels=["u", "o", "a"], vib_c=8, breath=0.12, attack=1.0, lp=2600),
      [2600, 0.10, 0.45, 0.85, 0.65, 0.25, 0.0, 0.0],
      V(atk=900, rel=2500, reso=0.8, vel=0.3, lfo=0.12, dly="1/4D", subsus=-20),
      (36, 84, 6), 6.0, True, "Breathy pad whose vowels morph over time. Ethereal beds."),
    P("ghost_swarm_bed", "Ghost Swarm Bed", "pads", ["cloud", "ambient", "dark", "drone"],
      "glass_pad", dict(attack=1.2, air=0.06, partials=[(1, 1.0), (2, 0.3), (3, 0.12), (4.02, 0.06)], decim=16000),
      [1200, 0.25, 0.40, 0.90, 0.80, 0.20, 0.0, 0.0],
      V(atk=1200, rel=3000, reso=0.8, vel=0.2, lfo=0.08, dly="1/4D", subsus=-20),
      (36, 84, 6), 6.0, True, "Dark drifting additive bed with airy noise. Two-chord drones."),
    P("shoegaze_haze_wall", "Shoegaze Haze Wall", "pads", ["shoegaze", "fuzz", "wall", "dream-pop"],
      "supersaw", dict(voices=6, detune_c=22, drive=2.2, lp=3000, attack=0.12, sustain=0.95),
      [3000, 0.20, 0.30, 0.90, 0.65, 0.25, 0.60, 0.0],
      V(atk=120, rel=1500, reso=0.9, vel=0.35, lfo=0.12, dly="1/4D", subsus=-12),
      (36, 84, 6), 4.0, True, "Driven, detuned saw wall standing in for fuzzed guitars, long dark tails."),
    P("frozen_halo", "Frozen Halo", "pads", ["freeze", "choir", "shimmer", "dream"],
      "voice", dict(singers=4, vowels=["u", "o"], vib_c=6, breath=0.10, attack=0.9, lp=3000, decim=14000),
      [3000, 0.0, 0.35, 0.90, 0.85, 0.20, 0.0, 0.0],
      V(atk=800, rel=3000, reso=0.8, vel=0.25, lfo=0.1, dly="1/4D", subsus=-20),
      (36, 84, 6), 6.0, True, "Wordless choir wash that hangs in place between vocal phrases."),
    P("lcr_ooh_choir", "L/C/R Ooh Choir", "vox", ["choir", "falsetto", "stacked", "lush"],
      "voice", dict(singers=6, vowels=["u"], vib_c=14, breath=0.05, attack=0.35),
      [7000, 0.0, 0.30, 0.90, 0.60, 0.10, 0.0, 0.0],
      V(atk=400, rel=2000, reso=0.8, vel=0.35, lfo=0.12, dly="1/4D", subsus=-30),
      (48, 84, 6), 4.0, True, "Stacked soft 'ooh' choir, triple-tracked wide. Intros and hooks."),
    P("reverse_ghost_chop", "Reverse Ghost Chop", "vox", ["reverse", "riser", "transition", "vocal-chop"],
      "voice", dict(singers=2, vowels=["a", "o"], t60=1.2, attack=0.004, vib_c=0, breath=0.06, reverse=True),
      [4500, 0.0, 0.20, 0.75, 0.65, 0.30, 0.0, 0.0],
      V(atk=5, rel=400, reso=0.8, vel=0.5, lfo=0.2, dly="1/8"),
      (48, 84, 4), 1.6, False, "Reversed vocal swells for transitions and circular motifs.", vl=2),
    P("garage_reese_floor", "Garage Reese Floor", "bass", ["reese", "garage", "warped", "dark"],
      "reese", dict(detune_c=12, lp=450, sub=0.7, sustain=0.9, drive=1.4),
      [2500, 0.30, 0.35, 0.15, 0.05, 0.0, 0.25, 0.30],
      V(atk=3, rel=200, reso=1.2, vel=0.3, lfo=0.25, subsus=-6),
      (24, 60, 6), 3.0, True, "Detuned saw reese over a sine with a slow warble. Garage drops."),
    P("tropic_mallet", "Tropic Mallet", "plucks", ["marimba", "tropical", "ostinato", "latin"],
      "modal", dict(modes=[(1, 1, 1), (3.99, 0.35, 0.25), (9.9, 0.12, 0.08)], t60=1.4, strike=0.25),
      [8000, 0.0, 0.10, 0.50, 0.40, 0.25, 0.0, 0.0],
      V(atk=1, rel=400, reso=0.8, vel=0.7, lfo=0.2, dly="1/8D"),
      (48, 96, 6), 2.0, False, "Soft-mallet marimba for tropical ostinatos and answer phrases.", vl=2),
    P("cassette_hiss_bed", "Cassette Hiss Bed", "pads", ["tape", "hiss", "bedroom", "texture"],
      "breath", dict(pitch=0.2, vowels=["u"], attack=0.4, decim=11025),
      [3000, 0.0, 0.50, 0.80, 0.50, 0.10, 0.20, 0.0],
      V(atk=400, rel=2000, reso=0.8, vel=0.2, lfo=0.15, dly="1/4D", subsus=-30),
      (36, 84, 12), 6.0, True, "Pitched tape hiss and breath that glues bedroom tracks together."),
    P("feedback_drone", "Feedback Drone", "pads", ["feedback", "drone", "unease", "shoegaze"],
      "glass_pad", dict(partials=[(1, 1), (2, 0.6), (3, 0.45), (4.01, 0.3), (5.02, 0.2)], air=0.1, attack=1.5),
      [1800, 0.0, 0.50, 0.70, 0.60, 0.10, 0.70, 0.0],
      V(atk=1500, rel=2500, reso=1.6, vel=0.2, lfo=0.25, dly="1/4D", subsus=-30),
      (36, 72, 6), 8.0, True, "Beating tuned drone in the style of amp feedback. Swells under a section turn."),

    # ================================================================ CLASSIC SYNTHS + PECULIAR PIANOS
    # Original renders in the spirit of classic workstation/analog synths and odd
    # pianos. Model names stay internal; preset names describe the sound.
    P("warehouse_stab_piano", "Warehouse Stab Piano", "keys", ["house", "piano", "90s", "stab"],
      "felt_piano", dict(hardness=0.95, t60=3.0, unison_c=2.0, post_shelf=(3000, 3.0), post_hp=90),
      [12000, 0.10, 0.20, 0.60, 0.30, 0.15, 0.10, 0.20],
      V(atk=1, rel=400, reso=0.8, vel=0.6, lfo=0.2, dly="1/8", subsus=-40),
      (36, 96, 6), 3.0, False, "Bright, hard-hammered piano for 90s house chord stabs.", vl=2),
    P("club_organ_stab", "Club Organ Stab", "chords", ["house", "organ", "90s", "stab"],
      "organ", dict(bars=[(1, 1), (2, 0.85), (3, 0.6), (4, 0.5), (6, 0.35), (8, 0.2)], wow=1.0, lp=6000),
      [8000, 0.15, 0.25, 0.50, 0.30, 0.15, 0.15, 0.25],
      V(atk=2, rel=150, reso=0.8, vel=0.4, lfo=0.3, dly="1/8", subsus=-12),
      (36, 96, 6), 3.0, True, "Hollow, punchy organ for house bass-lines and chord stabs."),
    P("ensemble_poly_six", "Ensemble Poly Six", "chords", ["analog", "poly", "chorus", "80s"],
      "supersaw", dict(voices=2, detune_c=6, lp=3200, reso=0.1, attack=0.005, decay=0.8, sustain=0.7),
      [3500, 0.15, 0.55, 0.85, 0.35, 0.12, 0.05, 0.0],
      V(atk=4, rel=400, reso=0.9, vel=0.45, lfo=0.25, dly="1/8D", subsus=-12),
      (36, 96, 6), 3.0, True, "Six-voice analog poly with a thick ensemble chorus. Chords that glow.", vl=2),
    P("glassline_poly", "Glassline Poly", "chords", ["analog", "poly", "modern", "pluck"],
      "supersaw", dict(voices=2, pulse=1, detune_c=9, lp=900, fenv=3500, fenv_t=0.25, t60=1.5, attack=0.002),
      [7000, 0.10, 0.35, 0.75, 0.35, 0.25, 0.10, 0.15],
      V(atk=1, rel=350, reso=1.0, vel=0.5, lfo=0.3, dly="1/8D"),
      (36, 96, 6), 2.2, False, "Modern analog poly pluck with a glassy pulse edge.", vl=2),
    P("twin_filter_scream", "Twin Filter Scream", "leads", ["aggressive", "resonant", "lead", "analog"],
      "supersaw", dict(voices=1, lp=1800, reso=0.8, drive_pre=2.5, hp=300, attack=0.005, sustain=0.9),
      [6000, 0.0, 0.25, 0.40, 0.25, 0.20, 0.40, 0.0],
      V(atk=3, rel=150, reso=1.6, vel=0.5, lfo=0.3, dly="1/8", subsus=-20),
      (36, 96, 6), 2.5, True, "Screaming high-pass plus low-pass lead with resonant bite.", vl=2),
    P("ladder_mono_bass", "Ladder Mono Bass", "bass", ["analog", "mono", "funk", "fat"],
      "supersaw", dict(voices=3, detune_c=4, sub=0.3, lp=400, reso=0.3, fenv=2200, fenv_t=0.2, drive_pre=1.6,
                       attack=0.002, decay=0.4, sustain=0.7),
      [3500, 0.15, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0],
      V(atk=1, rel=90, reso=1.3, vel=0.6, lfo=0.1, subdec=200, subsus=-40),
      (24, 60, 6), 2.5, True, "Three-oscillator ladder bass with a punchy filter snap.", vl=2),
    P("ladder_lead", "Ladder Lead", "leads", ["analog", "mono", "solo", "vibrato"],
      "supersaw", dict(voices=2, detune_c=6, lp=1500, reso=0.25, fenv=3000, fenv_t=0.3, drive_pre=1.4,
                       vib_c=8, vib_delay=0.5, attack=0.003, sustain=0.85),
      [5000, 0.10, 0.20, 0.40, 0.30, 0.25, 0.20, 0.0],
      V(atk=3, rel=180, reso=1.2, vel=0.5, lfo=0.2, dly="1/4D", subsus=-20),
      (36, 96, 6), 2.5, True, "Fat ladder-filter solo lead with delayed vibrato.", vl=2),
    P("brass_memory_poly", "Brass Memory Poly", "chords", ["analog", "brass", "poly", "80s"],
      "supersaw", dict(voices=3, detune_c=10, lp=1200, fenv=2400, fenv_t=0.35, attack=0.04, sustain=0.85, drive_pre=1.2),
      [4500, 0.20, 0.30, 0.80, 0.40, 0.10, 0.15, 0.0],
      V(atk=30, rel=500, reso=1.0, vel=0.5, lfo=0.2, dly="1/8D", subsus=-12),
      (36, 96, 6), 3.0, True, "Big analog poly brass with a swelling filter.", vl=2),
    P("prepared_bolt_piano", "Prepared Bolt Piano", "keys", ["prepared", "experimental", "percussive", "film"],
      "prepared", dict(t60=5.0, hardness=0.35, metal_mix=0.5, rattle=0.2),
      [9000, 0.0, 0.15, 0.60, 0.45, 0.15, 0.10, 0.0],
      V(atk=1, rel=900, reso=0.8, vel=0.65, lfo=0.15, dly="1/4D", subsus=-40),
      (36, 96, 6), 4.0, False, "Piano with bolts and paper on the strings: metal partials and a buzz.", vl=2),
    P("toy_box_piano", "Toy Box Piano", "keys", ["toy", "music-box", "nursery", "lofi"],
      "modal", dict(modes=[(1, 1, 1), (3.92, 0.45, 0.3), (9.58, 0.2, 0.12), (16.1, 0.08, 0.06)], t60=1.8, strike=0.35, beat_c=6.0),
      [9000, 0.0, 0.20, 0.55, 0.40, 0.20, 0.05, 0.0],
      V(atk=1, rel=500, reso=0.8, vel=0.6, lfo=0.2, dly="1/8D", subsus=-40),
      (60, 102, 6), 2.5, False, "Tiny struck rods, a little out of tune. Nursery and lo-fi motifs.", vl=2),
    P("saloon_tack_piano", "Saloon Tack Piano", "keys", ["honky-tonk", "tack", "vintage", "saloon"],
      "prepared", dict(hardness=0.85, unison_c=14.0, t60=4.0, metal_mix=0.2, rattle=0.12, rattle_hz=60.0),
      [10000, 0.0, 0.10, 0.50, 0.30, 0.05, 0.10, 0.0],
      V(atk=1, rel=600, reso=0.8, vel=0.7, lfo=0.15, dly="1/8", subsus=-40),
      (36, 96, 6), 3.5, False, "Detuned strings and tacks on the hammers. Saloon and ragtime colour.", vl=2),
    P("leaning_upright", "Leaning Upright", "keys", ["detuned", "upright", "lofi", "warm"],
      "felt_piano", dict(hardness=0.5, unison_c=5.0, t60=6.0, wow=3.0, tape=dict(wow_c=4, hiss=0.003, lp=9000)),
      [7000, 0.0, 0.10, 0.50, 0.40, 0.10, 0.05, 0.0],
      V(atk=2, rel=900, reso=0.7, vel=0.7, lfo=0.1, dly="1/8D", subsus=-40),
      (36, 96, 6), 4.5, False, "An old upright nobody tunes, recorded to tape. Warm and wonky.", vl=2),
    P("stage_electric_grand", "Stage Electric Grand", "keys", ["electric-grand", "80s", "ballad", "bright"],
      "felt_piano", dict(hardness=0.75, t60=3.0, lp=7000, post_shelf=(2500, 3.0), post_hp=120),
      [9000, 0.0, 0.40, 0.70, 0.35, 0.15, 0.05, 0.0],
      V(atk=1, rel=600, reso=0.8, vel=0.65, lfo=0.2, dly="1/8D", subsus=-40),
      (36, 96, 6), 3.5, False, "Thin, bright stage piano with pickup shimmer. 80s ballads.", vl=2),
    P("sticky_reed_keys", "Sticky Reed Keys", "keys", ["60s", "reed", "plucky", "vintage"],
      "reed_ep", dict(t60=1.2, drive=1.2, lp=3500),
      [5000, 0.0, 0.30, 0.50, 0.30, 0.15, 0.10, 0.0],
      V(atk=1, rel=250, reso=0.9, vel=0.6, lfo=0.25, dly="1/8"),
      (36, 96, 6), 2.0, False, "Short plucked reeds with a sticky attack. 60s pop keys.", vl=2),
    P("funk_pick_clav", "Funk Pick Clav", "keys", ["funk", "clav", "rhythmic", "bright"],
      "karplus", dict(t60=1.2, bright=9000, damp=0.7, pos=0.06, body=0.0, post_hp=150),
      [9000, 0.0, 0.25, 0.40, 0.15, 0.10, 0.15, 0.0],
      V(atk=1, rel=120, reso=1.0, vel=0.7, lfo=0.3, dly="1/16"),
      (36, 84, 4), 1.8, False, "Bright plucked-string keys for tight funk rhythm parts.", vl=2),
    P("tape_strip_strings", "Tape Strip Strings", "pads", ["tape", "strings", "60s", "psych"],
      "supersaw", dict(voices=3, detune_c=6, lp=3500, attack=0.15, sustain=1.0,
                       tape=dict(wow_c=9, flutter_c=4, hiss=0.006, lp=5000, length_s=8.0)),
      [4000, 0.0, 0.20, 0.60, 0.45, 0.05, 0.10, 0.0],
      V(atk=60, rel=400, reso=0.8, vel=0.4, lfo=0.15, dly="1/4D", subsus=-20),
      (36, 84, 6), 8.5, False, "Strings on 8-second tape strips: wobble, hiss, and they run out."),
    P("tape_strip_flute", "Tape Strip Flute", "leads", ["tape", "flute", "psych", "lofi"],
      "flute", dict(vib_c=10, breath=0.3, tape=dict(wow_c=10, flutter_c=4, hiss=0.006, lp=5000, length_s=8.0)),
      [6000, 0.0, 0.20, 0.50, 0.45, 0.15, 0.10, 0.0],
      V(atk=40, rel=300, reso=0.7, vel=0.45, lfo=0.2, dly="1/4D", subsus=-20),
      (48, 96, 6), 8.5, False, "Breathy flute on a worn tape strip. Psych intros."),
    P("optical_disc_organ", "Optical Disc Organ", "keys", ["lofi", "organ", "novelty", "crackle"],
      "organ", dict(wow=6.0, lp=4000, decim=11025, tape=dict(wow_c=6, crackle=3.0, hiss=0.01, lp=4000)),
      [3500, 0.10, 0.40, 0.40, 0.35, 0.10, 0.25, 0.0],
      V(atk=8, rel=200, reso=0.8, vel=0.25, lfo=0.3, dly="1/8D", subsus=-12),
      (36, 90, 6), 3.0, True, "Home organ read off a scratched optical disc. Crackle and wow."),
    P("digital_glass_ep", "Digital Glass EP", "keys", ["fm", "80s", "glassy", "ballad"],
      "fm_bell", dict(ratio=1.0, index=1.8, index_t=0.35, partial2=0.3, ratio2=14.0, t60=4.0, beat_c=3.0),
      [10000, 0.0, 0.40, 0.70, 0.40, 0.15, 0.0, 0.0],
      V(atk=1, rel=900, reso=0.7, vel=0.65, lfo=0.2, dly="1/8D", subsus=-40),
      (36, 96, 6), 4.0, False, "Glassy digital FM electric piano with a bright tine ping. 80s ballads.", vl=2),

    # ================================================================ SIGNATURE BANK v0.2
    # ------------------------------------------------------------ KEYS
    P("night_drive_keys", "Night Drive Keys", "keys", ["underwater", "rnb", "late-night", "dark", "lofi"],
      "tine_ep", dict(t60=6.0, bark=1.0, tine=0.18, pickup=0.30, wow=6.0, lp=2600, decim=8000, decim_drive=0.15),
      [950, 0.35, 0.30, 0.55, 0.55, 0.22, 0.12, 0.0],
      V(atk=6, rel=1100, reso=1.1, vel=0.55, lfo=0.18, dly="1/8D", subdec=1600, subsus=-24),
      (36, 96, 6), 4.0, False,
      "Low-passed tine keys with tape wobble and a dark room. Slow late-night chords."),
    P("velvet_tines", "Velvet Tines", "keys", ["rnb", "warm", "smooth", "classic"],
      "tine_ep", dict(t60=6.5, bark=1.4, tine=0.28, pickup=0.40),
      [5200, 0.25, 0.45, 0.70, 0.30, 0.10, 0.08, 0.0],
      V(atk=3, rel=700, reso=0.8, vel=0.65, lfo=0.25),
      (36, 96, 6), 4.0, False,
      "Clean, round electric piano with a gentle chorus. Neo-soul voicings."),
    P("submerged_felt", "Submerged Felt", "keys", ["underwater", "piano", "intimate", "lofi", "melancholy"],
      "felt_piano", dict(t60=6.5, hardness=0.20, lp=1900, wow=4.0, decim=11025, decim_drive=0.05),
      [1150, 0.30, 0.15, 0.60, 0.60, 0.20, 0.05, 0.0],
      V(atk=8, rel=1400, reso=0.9, vel=0.6, lfo=0.15, dly="1/4D"),
      (36, 96, 6), 4.5, False,
      "Felt piano heard through a wall: muffled hammers, warm wobble, long tail."),
    P("moonlit_upright", "Moonlit Upright", "keys", ["piano", "warm", "melancholy", "emotional"],
      "felt_piano", dict(t60=7.5, hardness=0.45, unison_c=1.2),
      [9000, 0.20, 0.05, 0.50, 0.40, 0.0, 0.0, 0.0],
      V(atk=3, rel=900, reso=0.7, vel=0.7, lfo=0.1),
      (36, 96, 6), 4.5, False,
      "Soft upright with a little detune between strings. Honest and close."),
    P("perreo_keys", "Perreo Keys", "keys", ["reggaeton", "bright", "rhythmic", "latin"],
      "tine_ep", dict(t60=2.4, bark=1.8, tine=0.35, pickup=0.50),
      [7000, 0.15, 0.25, 0.50, 0.20, 0.25, 0.15, 0.25],
      V(atk=1, rel=300, reso=0.8, vel=0.6, lfo=0.3, dly="1/8"),
      (36, 96, 6), 2.6, False,
      "Bright, barky stab keys that sit on a dembow groove. Pump locked to the beat."),
    P("glass_room_ep", "Glass Room EP", "keys", ["dreamy", "airy", "rnb", "shimmer"],
      "tine_ep", dict(t60=5.5, bark=0.8, tine=0.60, tine_ratio=8.3, pickup=0.20),
      [8000, 0.10, 0.50, 0.85, 0.60, 0.30, 0.0, 0.0],
      V(atk=4, rel=1200, reso=0.8, vel=0.55, lfo=0.2, dly="1/4D"),
      (36, 96, 6), 4.0, False,
      "Tine piano with the bell partial pushed forward, wide and glassy."),
    P("tape_organ", "Tape Organ", "keys", ["lofi", "vintage", "gospel", "warm"],
      "organ", dict(wow=7.0, lp=2600),
      [2000, 0.30, 0.35, 0.50, 0.45, 0.10, 0.20, 0.0],
      V(atk=8, rel=350, reso=0.8, vel=0.25, lfo=0.3, subsus=-12),
      (36, 90, 6), 3.0, True,
      "Soft drawbar organ printed to a worn tape. Sustains forever."),
    P("hazy_reed_keys", "Hazy Reed Keys", "keys", ["lofi", "gritty", "warm", "underwater"],
      "reed_ep", dict(t60=3.5, wow=5.0, drive=1.8, lp=2400, decim=9000, decim_drive=0.1),
      [1800, 0.30, 0.30, 0.50, 0.45, 0.18, 0.25, 0.0],
      V(atk=3, rel=600, reso=1.0, vel=0.6, lfo=0.22),
      (36, 96, 6), 3.5, False,
      "Reed electric piano with bite on the attack, then a hazy low-passed body."),

    # ------------------------------------------------------------ PADS
    P("submerged_choir", "Submerged Choir", "pads", ["underwater", "choir", "dark", "ambient"],
      "voice", dict(singers=5, vowels=["u"], vib_c=10, breath=0.03, attack=0.4, lp=1500, decim=10000),
      [1000, 0.35, 0.40, 0.80, 0.70, 0.10, 0.0, 0.0],
      V(atk=700, rel=2800, reso=0.9, vel=0.3, lfo=0.12, subsus=-6),
      (36, 84, 6), 4.0, True,
      "Ghost choir under water. Hold one chord and let it breathe."),
    P("midnight_wash", "Midnight Wash", "pads", ["underwater", "rnb", "wide", "dark", "late-night"],
      "supersaw", dict(voices=6, detune_c=14, lp=1100, keytrack=0.3, attack=0.3, noise=0.02, decim=10000),
      [1300, 0.40, 0.45, 0.85, 0.65, 0.12, 0.0, 0.0],
      V(atk=600, rel=2600, reso=1.2, vel=0.3, lfo=0.1, subsus=-6),
      (36, 84, 6), 4.0, True,
      "Wide detuned wash, low-passed until it is almost a memory."),
    P("supersaw_bloom", "Supersaw Bloom", "pads", ["future-bass", "supersaw", "euphoric", "bright", "wide"],
      "supersaw", dict(voices=9, detune_c=28, lp=9000, keytrack=0.2, attack=0.02),
      [12000, 0.25, 0.30, 0.90, 0.45, 0.15, 0.10, 0.65],
      V(atk=15, rel=900, reso=0.8, vel=0.35, lfo=0.25, dly="1/8D", subsus=-6),
      (36, 84, 6), 4.0, True,
      "Nine-voice supersaw chords that duck to the beat. Instant drop."),
    P("neon_haze", "Neon Haze", "pads", ["reggaeton", "atmospheric", "neon", "dark"],
      "supersaw", dict(voices=5, detune_c=18, pulse=1, lp=3200, attack=0.2),
      [3500, 0.30, 0.55, 0.75, 0.55, 0.20, 0.0, 0.20],
      V(atk=400, rel=2000, reso=1.0, vel=0.3, lfo=0.15, dly="1/4D", subsus=-8),
      (36, 84, 6), 4.0, True,
      "Moody saw-and-pulse atmosphere for perreo intros and bridges."),
    P("floating_dream_pad", "Floating Dream Pad", "pads", ["reggaeton", "dreamy", "lush", "airy"],
      "supersaw", dict(voices=4, detune_c=10, lp=1800, keytrack=0.4, attack=0.3, sub=0.15),
      [2000, 0.30, 0.45, 0.85, 0.75, 0.30, 0.0, 0.0],
      V(atk=300, rel=2600, reso=0.9, vel=0.3, lfo=0.15, dly="1/8D", subsus=-10),
      (36, 84, 6), 4.0, True,
      "Soft floaty pad with a slow filter drift and dotted echoes. Melodies float on it."),
    P("cold_glass", "Cold Glass", "pads", ["airy", "crystalline", "ambient", "bright"],
      "glass_pad", dict(attack=0.5, air=0.05),
      [14000, 0.05, 0.40, 0.85, 0.70, 0.25, 0.0, 0.0],
      V(atk=500, rel=3000, reso=0.7, vel=0.25, lfo=0.1, dly="1/4D", subsus=-20),
      (36, 84, 6), 4.0, True,
      "Glassy additive shimmer with slow beating partials."),
    P("analog_dusk", "Analog Dusk", "pads", ["warm", "analog", "vintage", "dark"],
      "supersaw", dict(voices=3, detune_c=9, pulse=1, lp=2400, reso=0.25, sub=0.25, attack=0.15),
      [2600, 0.45, 0.35, 0.60, 0.50, 0.10, 0.10, 0.0],
      V(atk=300, rel=1800, reso=1.4, vel=0.35, lfo=0.2, subsus=-6),
      (36, 84, 6), 4.0, True,
      "Two-oscillator analog pad, warm and slightly resonant."),
    P("velvet_strings", "Velvet Strings", "pads", ["cinematic", "lush", "strings", "emotional"],
      "supersaw", dict(voices=7, detune_c=16, lp=3800, attack=0.3, keytrack=0.6, hp=180),
      [4500, 0.30, 0.30, 0.80, 0.60, 0.05, 0.0, 0.0],
      V(atk=450, rel=2200, reso=0.8, vel=0.4, lfo=0.15, subsus=-12),
      (36, 84, 6), 4.0, True,
      "Ensemble strings from detuned saws. Slow swell, soft top end."),
    P("static_bloom", "Static Bloom", "pads", ["texture", "ambient", "lofi", "airy"],
      "breath", dict(pitch=0.8, vowels=["o"], attack=0.4),
      [5000, 0.20, 0.60, 0.90, 0.75, 0.30, 0.10, 0.0],
      V(atk=600, rel=3000, reso=0.8, vel=0.2, lfo=0.08, dly="1/4D", subsus=-20),
      (36, 84, 6), 4.0, True,
      "Pitched noise blooming into a tone. Texture under anything."),

    # ------------------------------------------------------------ PLUCKS
    P("future_pluck", "Future Pluck", "plucks", ["future-bass", "bright", "supersaw", "bouncy"],
      "supersaw", dict(voices=5, detune_c=20, lp=600, fenv=9000, fenv_t=0.12, t60=1.2, attack=0.001, keytrack=0.5),
      [14000, 0.20, 0.20, 0.80, 0.35, 0.30, 0.0, 0.55],
      V(atk=1, rel=350, reso=0.9, vel=0.55, lfo=0.3, dly="1/8D"),
      (48, 96, 6), 2.2, False,
      "Detuned saw pluck with a snappy filter, pumping on the quarter note."),
    P("dembow_nylon", "Dembow Nylon", "plucks", ["reggaeton", "guitar", "latin", "warm"],
      "karplus", dict(t60=2.6, bright=3200, body=0.6, pos=0.22, chorus=1),
      [9000, 0.20, 0.15, 0.55, 0.30, 0.20, 0.05, 0.0],
      V(atk=1, rel=500, reso=0.8, vel=0.65, lfo=0.2, dly="1/8"),
      (40, 88, 6), 2.6, False,
      "Nylon-string pluck with a woody body. Arpeggios and tresillo riffs."),
    P("night_marimba", "Night Marimba", "plucks", ["reggaeton", "marimba", "tropical", "warm"],
      "modal", dict(modes=[(1, 1, 1), (3.99, 0.35, 0.25), (9.9, 0.12, 0.08)], t60=1.4, strike=0.25),
      [8000, 0.25, 0.10, 0.50, 0.40, 0.25, 0.0, 0.0],
      V(atk=1, rel=400, reso=0.8, vel=0.7, lfo=0.2, dly="1/8D"),
      (48, 96, 6), 2.0, False,
      "Soft-mallet marimba with a night-time reverb. Tropical melodies."),
    P("dusty_kalimba", "Dusty Kalimba", "plucks", ["lofi", "kalimba", "intimate", "nostalgic"],
      "modal", dict(modes=[(1, 1, 1), (5.95, 0.18, 0.3), (13.1, 0.08, 0.1)], t60=2.2, strike=0.4, lp=3000, wow=5.0),
      [3500, 0.15, 0.25, 0.55, 0.50, 0.30, 0.0, 0.0],
      V(atk=1, rel=600, reso=0.9, vel=0.6, lfo=0.25, dly="1/4D"),
      (48, 96, 6), 2.6, False,
      "Thumb piano through a dusty tape deck."),
    P("vox_chop_pluck", "Vox Chop Pluck", "plucks", ["vocal-chop", "future-bass", "bouncy", "bright"],
      "voice", dict(singers=1, vowels=["a", "o"], t60=0.45, attack=0.003, vib_c=0, breath=0.03),
      [12000, 0.10, 0.20, 0.60, 0.35, 0.35, 0.0, 0.40],
      V(atk=1, rel=200, reso=0.8, vel=0.5, lfo=0.3, dly="1/8D"),
      (48, 84, 6), 1.5, False,
      "Short synthetic 'ah' chop. Play it like a lead for vocal-chop hooks."),
    P("waterlogged_keen", "Waterlogged Keen", "plucks", ["reggaeton", "dreamy", "underwater", "high"],
      "modal", dict(modes=[(1, 1, 1), (3, 0.12, 0.4), (5, 0.04, 0.3)], t60=1.6, strike=0.1, lp=2400),
      [2200, 0.10, 0.40, 0.60, 0.55, 0.35, 0.0, 0.0],
      V(atk=1, rel=500, reso=0.9, vel=0.55, lfo=0.2, dly="1/8D"),
      (60, 102, 6), 2.4, False,
      "High, soft sine-ish pluck through water. Dotted-eighth echoes for floating hooks."),
    P("glint_harp", "Glint Harp", "plucks", ["airy", "bright", "harp", "dreamy"],
      "karplus", dict(t60=3.5, bright=7000, damp=0.5, pos=0.12),
      [16000, 0.10, 0.20, 0.70, 0.55, 0.30, 0.0, 0.0],
      V(atk=1, rel=700, reso=0.7, vel=0.6, lfo=0.2, dly="1/4D"),
      (48, 96, 6), 3.0, False,
      "Bright plucked harp, wide reverb, sparkling echoes."),

    # ------------------------------------------------------------ LEADS
    P("hyper_saw_lead", "Hyper Saw Lead", "leads", ["future-bass", "supersaw", "bright", "anthem"],
      "supersaw", dict(voices=5, detune_c=16, lp=7000, attack=0.005),
      [9000, 0.20, 0.20, 0.70, 0.35, 0.30, 0.25, 0.30],
      V(atk=5, rel=250, reso=0.9, vel=0.4, lfo=0.3, dly="1/8D", subsus=-10),
      (48, 96, 6), 3.0, True,
      "Detuned saw lead for drop melodies. Grit and pump already dialled in."),
    P("velvet_square", "Velvet Square", "leads", ["reggaeton", "smooth", "retro", "lead"],
      "supersaw", dict(voices=2, detune_c=5, pulse=1, lp=2600, attack=0.01),
      [3000, 0.30, 0.35, 0.45, 0.35, 0.25, 0.05, 0.0],
      V(atk=8, rel=300, reso=1.0, vel=0.45, lfo=0.25, dly="1/8D", subsus=-10),
      (48, 96, 6), 3.0, True,
      "Rounded square lead, soft and vocal. Hooks over a dembow."),
    P("hollow_flute", "Hollow Flute", "leads", ["airy", "latin", "flute", "organic"],
      "flute", dict(vib_c=14, breath=0.25),
      [9000, 0.10, 0.20, 0.50, 0.45, 0.20, 0.0, 0.0],
      V(atk=40, rel=350, reso=0.7, vel=0.5, lfo=0.2, subsus=-20),
      (48, 96, 6), 3.0, True,
      "Breathy synthetic flute with delayed vibrato."),
    P("siren_vox_lead", "Siren Vox Lead", "leads", ["vocal", "lead", "emotional", "airy"],
      "voice", dict(singers=1, vowels=["a"], vib_c=22, breath=0.05, attack=0.05),
      [8000, 0.15, 0.25, 0.50, 0.45, 0.30, 0.0, 0.0],
      V(atk=30, rel=400, reso=0.8, vel=0.45, lfo=0.2, dly="1/4D", subsus=-20),
      (48, 84, 6), 3.0, True,
      "Wordless synthetic voice with a singer's vibrato."),
    P("dirty_brass_lead", "Dirty Brass Lead", "leads", ["reggaeton", "brass", "distorted", "dark"],
      "supersaw", dict(voices=3, detune_c=6, lp=900, fenv=2200, fenv_t=0.3, drive_pre=3.5, attack=0.03, keytrack=0.6),
      [3000, 0.30, 0.20, 0.50, 0.35, 0.15, 0.40, 0.0],
      V(atk=25, rel=250, reso=1.1, vel=0.5, lfo=0.2, dly="1/8", subsus=-8),
      (36, 84, 6), 3.0, True,
      "Low, fuzzy synth brass: dirty, nothing bright. Heavy reggaeton riffs."),
    P("grit_saw_lead", "Grit Saw Lead", "leads", ["gritty", "aggressive", "future-bass", "lead"],
      "supersaw", dict(voices=3, detune_c=10, lp=4000, drive=2.5, attack=0.003),
      [5000, 0.30, 0.30, 0.55, 0.30, 0.20, 0.50, 0.0],
      V(atk=3, rel=220, reso=1.2, vel=0.4, lfo=0.35, subsus=-10),
      (48, 96, 6), 3.0, True,
      "Driven saw lead with teeth. Cuts through a busy drop."),

    # ------------------------------------------------------------ BELLS
    P("crystal_fm_bell", "Crystal FM Bell", "bells", ["bright", "crystalline", "dreamy"],
      "fm_bell", dict(ratio=3.5, index=3.0, t60=4.0),
      [16000, 0.0, 0.20, 0.70, 0.55, 0.30, 0.0, 0.0],
      V(atk=1, rel=1200, reso=0.7, vel=0.6, lfo=0.2, dly="1/4D"),
      (60, 102, 6), 4.0, False,
      "Two-operator FM bell, glassy attack and a long shimmering tail."),
    P("music_box_memory", "Music Box Memory", "bells", ["lofi", "nostalgic", "music-box", "intimate"],
      "modal", dict(modes=[(1, 1, 1), (2.0, 0.3, 0.5), (5.4, 0.2, 0.2), (9.2, 0.1, 0.1)], t60=2.6, strike=0.2, wow=6.0, lp=5000),
      [6000, 0.05, 0.30, 0.60, 0.55, 0.25, 0.0, 0.0],
      V(atk=1, rel=800, reso=0.8, vel=0.6, lfo=0.2, dly="1/8D"),
      (60, 102, 6), 3.0, False,
      "Tiny music box with a warped tape memory."),
    P("celeste_mist", "Celeste Mist", "bells", ["underwater", "dreamy", "celeste", "soft"],
      "modal", dict(modes=[(1, 1, 1), (2, 0.25, 0.6), (3, 0.1, 0.4), (4.1, 0.08, 0.3)], t60=3.2, strike=0.15, lp=2400, decim=8000),
      [1600, 0.10, 0.30, 0.70, 0.70, 0.25, 0.0, 0.0],
      V(atk=2, rel=1500, reso=0.9, vel=0.55, lfo=0.15, dly="1/4D"),
      (60, 102, 6), 3.5, False,
      "Celeste under water. Pairs with low-passed keys."),
    P("gamelan_glass", "Gamelan Glass", "bells", ["metallic", "exotic", "bright", "shimmer"],
      "modal", dict(modes=[(1, 1, 1), (2.76, 0.5, 0.6), (5.4, 0.3, 0.35), (8.93, 0.15, 0.2)], t60=4.0, strike=0.3, beat_c=4.0),
      [12000, 0.0, 0.20, 0.75, 0.60, 0.20, 0.0, 0.0],
      V(atk=1, rel=1500, reso=0.7, vel=0.6, lfo=0.2),
      (60, 102, 6), 4.0, False,
      "Inharmonic metal bars that beat against each other."),

    # ------------------------------------------------------------ VOX
    P("ooh_ensemble", "Ooh Ensemble", "vox", ["choir", "lush", "vocal", "emotional"],
      "voice", dict(singers=6, vowels=["u"], vib_c=14, breath=0.05, attack=0.35),
      [7000, 0.25, 0.35, 0.85, 0.65, 0.10, 0.0, 0.0],
      V(atk=500, rel=2200, reso=0.8, vel=0.35, lfo=0.12, subsus=-12),
      (48, 84, 6), 4.0, True,
      "Six synthetic singers on an 'ooh'. Big, soft background vocals."),
    P("ah_chop_stack", "Ah Chop Stack", "vox", ["vocal-chop", "future-bass", "bright", "bouncy"],
      "voice", dict(singers=3, vowels=["a"], t60=0.7, attack=0.004, vib_c=0, spread_c=8),
      [11000, 0.10, 0.25, 0.80, 0.40, 0.40, 0.0, 0.50],
      V(atk=1, rel=250, reso=0.8, vel=0.5, lfo=0.3, dly="1/8D"),
      (48, 84, 6), 1.8, False,
      "Stacked 'ah' chops for call-and-response hooks."),
    P("breath_vox", "Breath Vox", "vox", ["breathy", "ambient", "intimate", "airy"],
      "breath", dict(pitch=0.5, vowels=["a"], attack=0.3),
      [6000, 0.10, 0.50, 0.85, 0.70, 0.25, 0.0, 0.0],
      V(atk=300, rel=2000, reso=0.8, vel=0.3, lfo=0.1, dly="1/4D", subsus=-20),
      (48, 84, 6), 4.0, True,
      "A pitched whisper. Doubles a topline without getting in the way."),
    P("formant_swirl", "Formant Swirl", "vox", ["vocal", "movement", "texture", "future-bass"],
      "voice", dict(singers=3, vowels=["a", "o", "e", "u"], vib_c=12, attack=0.2),
      [8000, 0.15, 0.50, 0.80, 0.60, 0.20, 0.0, 0.0],
      V(atk=250, rel=1500, reso=0.8, vel=0.35, lfo=0.15, subsus=-14),
      (48, 84, 6), 4.0, True,
      "Vowels morphing a-o-e-u while you hold the note."),

    # ------------------------------------------------------------ BASS
    P("long_808", "Long 808", "bass", ["808", "trap", "reggaeton", "deep"],
      "808", dict(drop_st=7, drop_t=0.05, t60=3.2, drive=1.4, click=0.15),
      [18000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.10, 0.0],
      V(atk=1, rel=250, reso=0.7, vel=0.35, lfo=0.1, subsus=-40, subdec=200),
      (24, 60, 6), 3.5, False,
      "Clean, long 808 with a short pitch drop. Glue for every low end."),
    P("grit_808", "Grit 808", "bass", ["808", "distorted", "aggressive", "trap"],
      "808", dict(drop_st=12, t60=2.5, drive=3.5, click=0.25),
      [9000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.45, 0.0],
      V(atk=1, rel=220, reso=0.7, vel=0.35, lfo=0.1, subsus=-40, subdec=200),
      (24, 60, 6), 3.0, False,
      "Saturated 808 that reads on phone speakers."),
    P("punch_808", "Punch 808", "bass", ["808", "punchy", "short", "dembow"],
      "808", dict(drop_st=14, drop_t=0.03, t60=1.0, drive=2.0, click=0.35),
      [14000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.0],
      V(atk=1, rel=150, reso=0.7, vel=0.45, lfo=0.1, subsus=-40, subdec=200),
      (24, 60, 6), 1.5, False,
      "Short, punchy 808 for bouncing dembow bass lines."),
    P("reese_shadow", "Reese Shadow", "bass", ["reese", "dark", "bass", "gritty"],
      "reese", dict(detune_c=14, lp=700, sub=0.6, sustain=0.9),
      [2500, 0.30, 0.30, 0.20, 0.10, 0.0, 0.25, 0.0],
      V(atk=3, rel=200, reso=1.2, vel=0.3, lfo=0.2, subsus=-6),
      (24, 60, 6), 3.0, True,
      "Detuned saw reese with a sine underneath. Dark and moving."),
    P("degraded_floor_bass", "Degraded Floor Bass", "bass", ["underwater", "lofi", "sub", "dark"],
      "reese", dict(detune_c=6, lp=400, sub=0.8, sustain=0.9, drive=1.2, decim=4400),
      [1500, 0.20, 0.10, 0.10, 0.05, 0.0, 0.15, 0.0],
      V(atk=3, rel=180, reso=0.9, vel=0.35, lfo=0.1, subsus=-8),
      (24, 60, 6), 3.0, True,
      "Saw plus sine bass crushed to a 4.4 kHz sample rate. Dark, grainy floor."),
    P("round_sub", "Round Sub", "bass", ["sub", "clean", "deep", "808"],
      "sub", dict(h2=0.05, sustain=0.95),
      [20000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0],
      V(atk=3, rel=150, reso=0.7, vel=0.3, lfo=0.1, subsus=-40, subdec=200),
      (24, 60, 6), 2.0, True,
      "Pure sustained sub. Sits under keys without clouding them."),
    P("dembow_bass", "Dembow Bass", "bass", ["reggaeton", "bass", "round", "dembow"],
      "sub", dict(h2=0.22, t60=0.9, drive=1.6),
      [12000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.20, 0.0],
      V(atk=1, rel=120, reso=0.7, vel=0.5, lfo=0.1, subsus=-40, subdec=200),
      (24, 60, 6), 1.5, False,
      "Round plucky bass for tight reggaeton lines."),
]


# ---------------------------------------------------------------------------
# Instrument packs: extra recipes as JSON in assets/packs/instruments/*.json.
# Each file is {"pack": "<pack name>", "presets": [<recipe>, ...]} where a
# recipe has the same fields as P(): id, name, cat, tags, gen, gp, m, v, z,
# dur, loop, desc and optional vl (1|2) and d (SHAPE values). v uses V() keys
# and missing ones take V() defaults. Files load in name order, and the
# recipes are appended to PRESETS, so build_loop_lines.py can use them too.
# ---------------------------------------------------------------------------
PACK_DIR = ROOT / "assets" / "packs"
RECIPE_KEYS = {"id", "name", "cat", "tags", "gen", "gp", "m", "v", "z", "dur", "loop", "desc", "vl", "d", "mod", "map", "rr"}


def pack_files(folder: Path) -> list[Path]:
    """Pack JSON files in a folder. With SM_TRACKED_PACKS=1 only files git tracks, so a
    local render matches CI exactly while new packs are still being written."""
    files = sorted(folder.glob("*.json"))
    if os.environ.get("SM_TRACKED_PACKS") == "1":
        import subprocess
        out = subprocess.run(["git", "ls-files", "--", str(folder)], capture_output=True, text=True,
                             cwd=str(folder)).stdout.split()
        tracked = {Path(folder, Path(x).name).resolve() for x in out}
        files = [f for f in files if f.resolve() in tracked]
    return files


def load_instrument_packs() -> list[dict]:
    out = []
    cats = {c for c, _ in CATEGORIES if c != "archive"}
    vkeys = set(V().keys())
    for f in pack_files(PACK_DIR / "instruments"):
        data = json.loads(f.read_text())
        pack = data.get("pack", f.stem)
        for r in data["presets"]:
            where = f"{f.name}:{r.get('id', '?')}"
            extra = set(r) - RECIPE_KEYS
            assert not extra, f"{where}: unknown fields {sorted(extra)}"
            for k in ("id", "name", "cat", "tags", "gen", "gp", "m", "v", "z", "dur", "loop", "desc"):
                assert k in r, f"{where}: missing {k}"
            assert r["gen"] in dsp.GENERATORS, f"{where}: gen must be one of {sorted(dsp.GENERATORS)}"
            assert r["cat"] in cats, f"{where}: cat must be one of {sorted(cats)}"
            assert len(r["m"]) == 8, f"{where}: m needs 8 macro values"
            assert 80 <= r["m"][0] <= 20000 and all(0.0 <= x <= 1.0 for x in r["m"][1:]), f"{where}: macro range"
            assert set(r["v"]) <= vkeys, f"{where}: v keys must be from {sorted(vkeys)}"
            assert len(r["z"]) == 3 and r["z"][0] <= r["z"][1] and r["z"][2] > 0, f"{where}: z = [lo, hi, step]"
            cap = 14.0 if "flagship" in r.get("tags", []) else 12.0     # flagship L-lock loops start after 3+ s
            assert 0.2 <= r["dur"] <= cap, f"{where}: dur seconds 0.2..{cap:g}"
            assert 1 <= r.get("vl", 1) <= 6, f"{where}: vl is 1..6"
            assert 1 <= r.get("rr", 1) <= 5, f"{where}: rr is 1..5"
            if r.get("vl", 1) >= 3:
                ax = r["gp"].get("vel_axis")
                assert ax and len(ax.get("values", [])) == r["vl"], f"{where}: vl >= 3 needs gp vel_axis with one value per layer"
            assert all(t == t.lower() for t in r["tags"]), f"{where}: tags lowercase"
            out.append(P(r["id"], r["name"], r["cat"], list(r["tags"]), r["gen"], dict(r["gp"]),
                         list(r["m"]), V(**r["v"]), tuple(r["z"]), float(r["dur"]), bool(r["loop"]),
                         r["desc"], vl=r.get("vl", 1), d=r.get("d"), mod=r.get("mod"), rr=r.get("rr", 1)))
            out[-1]["pack"] = pack
            if r.get("map"):
                out[-1]["map"] = r["map"]          # doc 25 B6: a snapshot of another preset's samples
    return out


PRESETS.extend(load_instrument_packs())

# Retired presets (doc 25 retirements): no longer rendered or listed. A saved Live set or
# user preset that names one loads its replacement (PRESET_ALIASES in FactoryBank.js,
# resolved by findPreset), so retiring never breaks a session.
RETIRED = {
    "night_drive_keys": "lullaby_underwater",
    "glass_room_ep": "fork_piano",
    "ensemble_poly_six": "ladder_poly",
    "floating_dream_pad": "singing_bowl_field",
    "analog_dusk": "ladder_drone_pad",
    "velvet_strings": "bowed_metal",
    "long_808": "sigh_circuit_808",
    "hazy_reed_keys": "dust_harmonium",
    "ooh_ensemble": "cave_chant",
    "tape_organ": "strip_choir",
    "grit_saw_lead": "undertone_lead",
}
PRESETS[:] = [p for p in PRESETS if p["id"] not in RETIRED]


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def seed_for(pid: str, note: int) -> int:
    h = hashlib.sha256(f"{pid}:{note}".encode()).hexdigest()
    return int(h[:8], 16)


def zone_roots(z):
    lo, hi, step = z
    return list(range(lo, hi + 1, step))


def write_wav24(path: Path, l: np.ndarray, r: np.ndarray, rng) -> None:
    """48 kHz / 24-bit stereo PCM with TPDF dither at the 24-bit LSB."""
    q = 8388607.0
    dither = (rng.random(len(l)) - rng.random(len(l))) / q
    li = np.clip(np.round((l + dither) * q), -8388608, 8388607).astype("<i4")
    ri = np.clip(np.round((r + dither) * q), -8388608, 8388607).astype("<i4")
    inter = np.empty(len(li) * 2, dtype="<i4")
    inter[0::2] = li
    inter[1::2] = ri
    raw = inter.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()   # little-endian low 3 bytes
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(raw)


def write_wav24_mono(path: Path, x: np.ndarray, rng) -> None:
    """48 kHz / 24-bit MONO PCM with TPDF dither (HISE plays a mono file on both channels)."""
    q = 8388607.0
    dither = (rng.random(len(x)) - rng.random(len(x))) / q
    xi = np.clip(np.round((x + dither) * q), -8388608, 8388607).astype("<i4")
    raw = xi.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(raw)


def write_wav16(path: Path, l: np.ndarray, r: np.ndarray, rng) -> None:
    """48 kHz / 16-bit stereo PCM with TPDF dither at the 16-bit LSB (loops: a third smaller
    than 24-bit; the loops sit near -13 dBFS RMS, so 16-bit leaves ~80 dB of clean range)."""
    q = 32767.0
    dither = (rng.random(len(l)) - rng.random(len(l))) / q
    inter = np.empty(len(l) * 2, dtype="<i2")
    inter[0::2] = np.clip(np.round((l + dither) * q), -32768, 32767).astype("<i2")
    inter[1::2] = np.clip(np.round((r + dither) * q), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(inter.tobytes())


SOFT_RULES = {
    # gen: {param: multiplier}  (missing params are left alone)
    "prepared":   {"hardness": 0.5, "lp": 0.75, "rattle": 0.5, "metal_mix": 0.7},
    "tine_ep":    {"bark": 0.55, "tine": 0.6, "pickup": 0.6, "lp": 0.7},
    "felt_piano": {"hardness": 0.5, "lp": 0.75},
    "reed_ep":    {"drive": 0.7, "lp": 0.75},
    "supersaw":   {"lp": 0.65, "fenv": 0.5, "drive": 0.7, "drive_pre": 0.7},
    "karplus":    {"bright": 0.55, "damp": 0.6},
    "modal":      {"strike": 0.4, "lp": 0.7},
    "fm_bell":    {"index": 0.55},
    "voice":      {"breath": 1.3, "lp": 0.75},
    "808":        {"drive": 0.75, "click": 0.5},
    "reese":      {"lp": 0.75, "drive": 0.8},
    "sub":        {"drive": 0.8, "h2": 0.6},
    "flute":      {"breath": 0.8},
}
SOFT_DEFAULT_LP = {"felt_piano": 3500, "prepared": 3500, "modal": 5000, "voice": 3200, "karplus": 3000}
SOFT_LEVEL = 0.71          # soft layer sits ~3 dB under the hard layer


def soften(gen, gp):
    """Soft velocity layer. doc 25 B4: a recipe can set its own rules with gp soft_mul
    {param: multiplier} (or soft {..} on generators where soft is not already a flag)."""
    out = dict(gp)
    rules = SOFT_RULES.get(gen, {})
    if isinstance(gp.get("soft_mul"), dict):
        rules = gp["soft_mul"]
    elif isinstance(gp.get("soft"), dict) and gen != "karplus":
        rules = gp["soft"]
    for k, mul in rules.items():
        if k in out and out[k]:
            out[k] = out[k] * mul
    if gen in SOFT_DEFAULT_LP and not out.get("lp"):
        out["lp"] = SOFT_DEFAULT_LP[gen]
    return out


def post_eq(x, gp):
    """Baked per-preset EQ (the plugin's Air EQ is fixed): post_hp = low cut Hz,
    post_shelf = (Hz, dB) high shelf built from a high-pass blend."""
    if gp.get("post_hp"):
        x = dsp.svf(x, gp["post_hp"], 0.707, 2)          # 12 dB/oct: keeps low-note bodies
    if gp.get("post_shelf"):
        f, db = gp["post_shelf"]
        x = x + (10 ** (db / 20.0) - 1.0) * dsp.svf(x, f, 0.707, 2)
    return x


def _st_decim(l, r, gp, rng):
    return (dsp.decimate(l, gp["decim"], gp.get("decim_drive", 0.0)),
            dsp.decimate(r, gp["decim"], gp.get("decim_drive", 0.0)))


def _st_reverse(l, r, gp, rng):                 # reversed swell: ends on the attack
    l = l[::-1].copy()
    r = r[::-1].copy()
    fade = int(0.02 * SR)
    l[:fade] *= np.linspace(0.0, 1.0, fade)
    r[:fade] *= np.linspace(0.0, 1.0, fade)
    return l, r


# doc 25 B12: texture stages by name; gp stage_order picks the order (a stage runs when its
# gp key is set). New stages (plate, spring, vnd, bbd, ensemble ...) register here.
STAGES = {"decim": _st_decim, "bbd": dsp.bbd_stage, "ensemble": dsp.ensemble_stage, "vnd": dsp.vnd_stage,
          "tape": lambda l, r, gp, rng: dsp.tape_age(l, r, gp, rng), "reverse": _st_reverse}
DEFAULT_STAGES = ["decim", "bbd", "ensemble", "tape", "vnd", "reverse"]   # chorus before tape; width last


def render_voice(p, gp, note, n, rng):
    """One zone/layer. gp['slow'] < 1 renders a slowed-tape take that stays in
    tune: render higher and shorter, then stretch back (pitch, envelopes and
    spectrum all drop together, like tape at that speed)."""
    gen = dsp.GENERATORS[p["gen"]]
    gp = dict(gp)
    gp["_wseed"] = seed_for(p["id"] + ":wow", 0)     # doc 25 B9: one wow phase per preset
    gp["_eseed"] = seed_for(p["id"] + ":excite", 0)  # doc 25 B11: one pluck noise per preset
    if p.get("loop"):                                # doc 25 B10: generators can fit cycles to the loop
        ls = gp.get("loop_start", max(gp.get("attack", 0.01) + 0.6, 1.0))
        if gp.get("llock"):
            gp["_loop"] = llock_region(p, gp, note)
        else:
            gp["_loop"] = (int(ls * SR), max(int(ls * SR) + 1, n - int(0.03 * SR)))
    slow = gp.get("slow", 1.0)
    speed = gp.get("speed", 1.0)
    if speed > 1.0:
        # varispeed up (voice_v2): render lower and longer, then play it faster, so the
        # formants rise with the pitch like tape (a chipmunk saint, not a pitch-shifted one)
        n_r = int(n * speed)
        l, r = gen(note - 12.0 * math.log2(speed), n_r, gp, rng)
        pos = np.linspace(0, n_r - 1, n)
        l = np.interp(pos, np.arange(n_r), l)
        r = np.interp(pos, np.arange(n_r), r)
    elif slow < 1.0:
        n_r = int(n * slow)
        l, r = gen(note - 12.0 * math.log2(slow), n_r, gp, rng)
        pos = np.linspace(0, n_r - 1, n)
        l = np.interp(pos, np.arange(n_r), l)
        r = np.interp(pos, np.arange(n_r), r)
    else:
        l, r = gen(note, n, gp, rng)
    for stage in gp.get("stage_order", DEFAULT_STAGES):
        if stage not in STAGES:
            raise SystemExit(f'{p["id"]}: unknown stage {stage!r} in stage_order (have {sorted(STAGES)})')
        if gp.get(stage):
            l, r = STAGES[stage](l, r, gp, rng)
    l = post_eq(np.nan_to_num(l), gp)
    r = post_eq(np.nan_to_num(r), gp)
    # doc 25 B7: subtracting the mean stepped sample 0 to -mean (5-24% of peak on 16 presets);
    # a 5 Hz DC blocker from zero state removes the offset with no onset step
    return dsp.dc_block(l), dsp.dc_block(r)


def write_wav16(path: Path, l: np.ndarray, r: np.ndarray, rng) -> None:
    dither = (rng.random(len(l)) - rng.random(len(l))) / 32768.0
    li = np.clip(np.round((l + dither) * 32767.0), -32768, 32767).astype("<i2")
    ri = np.clip(np.round((r + dither) * 32767.0), -32768, 32767).astype("<i2")
    inter = np.empty(len(li) * 2, dtype="<i2")
    inter[0::2] = li
    inter[1::2] = ri
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(inter.tobytes())


def loud400(l, r):
    """RMS of the loudest 400 ms (100 ms hop), after processing (doc 25 B2). The old
    first-second window under-read slow attacks and over-read plucks."""
    e = (l.astype(np.float64) ** 2 + r.astype(np.float64) ** 2) * 0.5
    w = int(0.4 * SR)
    if len(e) <= w:
        return math.sqrt(float(np.mean(e)) + 1e-12)
    c = np.concatenate([[0.0], np.cumsum(e)])
    st = np.arange(0, len(e) - w + 1, int(0.1 * SR))
    return math.sqrt(float(np.max((c[st + w] - c[st]) / w)) + 1e-12)


def tail_db(l, r, sec=0.3):
    """Level of the last `sec` seconds relative to the peak (dB)."""
    a = np.maximum(np.abs(l), np.abs(r))
    pk = float(a.max()) + 1e-12
    k = max(1, int(sec * SR))
    return 20.0 * math.log10(math.sqrt(float(np.mean(a[-k:] ** 2))) / pk + 1e-12)


def decay_end(l, r, floor_db=-60.0):
    """Sample where the sound has decayed `floor_db` below its peak, plus 50 ms."""
    a = np.maximum(np.abs(l), np.abs(r))
    blk = int(0.01 * SR)
    nb_ = len(a) // blk
    env = a[: nb_ * blk].reshape(nb_, blk).max(axis=1)
    thr = env.max() * 10 ** (floor_db / 20.0)
    above = np.nonzero(env > thr)[0]
    last = int(above[-1]) if len(above) else 0
    return min(len(a), (last + 1) * blk + int(0.05 * SR))


ONESHOT_CAP_S = 12.0


def zone_render(p, gp, note, n_base, rng_seed):
    """One-shot zones were cut at the preset's dur while still loud (doc 23: 26 of 61).
    If the tail is above -40 dB, render up to max(2 x dur, 1.3 x t60) (cap 12 s) and keep it
    only if the sound really decays there (a held tone stays at dur); end at -60 dB."""
    l, r = render_voice(p, gp, note, n_base, np.random.default_rng(rng_seed))
    # flagships render to the floor (docs/27 bar 7): extend while the tail is above -54 dB
    thr = -54.0 if "flagship" in p["tags"] else -40.0
    # generators that size their own takes (flagship_dsp.F_DUR) already end at the floor
    if p["loop"] or p["gen"] in fdsp.F_DUR or tail_db(l, r) < thr:
        return l, r
    t60 = p["gp"].get("t60", 0.0) or 0.0
    n_cap = int(min(ONESHOT_CAP_S, max(2.0 * p["dur"], 1.3 * t60)) * SR)
    if n_cap <= n_base:
        return l, r
    l2, r2 = render_voice(p, gp, note, n_cap, np.random.default_rng(rng_seed))
    if tail_db(l2, r2) > tail_db(l, r) - 12.0:        # not decaying: a held tone, keep the original
        return l, r
    end = max(n_base // 2, decay_end(l2, r2))
    return l2[:end], r2[:end]


def xfade_dip(l, r, ls, le, xf, gamma):
    """Dip (dB) at the middle of HISE's loop crossfade, against the power midpoint of the two
    blended sections: the same measure as scripts/ci/check_render_qa.py."""
    m = (l + r) * 0.5
    a = m[le - xf: le]
    b_ = m[ls - xf: ls]
    tt = np.linspace(0.0, 1.0, xf)
    blend = a * (1.0 - tt) ** gamma + b_ * tt ** gamma
    w = max(16, xf // 8)
    mid = slice(xf // 2 - w // 2, xf // 2 + w // 2)
    def rms(v):
        return math.sqrt(float(np.mean(v * v)) + 1e-12)
    ref = math.sqrt(0.5 * (rms(a[mid]) ** 2 + rms(b_[mid]) ** 2))
    return 20.0 * math.log10(rms(blend[mid]) / ref + 1e-12)


def llock_region(p, gp, note):
    """docs/27 L-lock: the loop holds a whole number of periods of the lowest oscillator
    (f0 x llock ratio); generators make every beat and drift periodic over it."""
    import flagship_dsp as fd
    lk = gp["llock"]
    ls = int(gp.get("loop_start", 1.0) * SR)
    f_key = fd.F_LOW[p["gen"]](note) if p["gen"] in fd.F_LOW else dsp.mtof(note)   # a divider's own tuning
    n_loop = fd.llock_n(f_key * lk.get("ratio", 1.0), lk.get("target_s", 5.0))
    return ls, ls + n_loop


def loop_points(p, l, r, note):
    """Sustain loop (doc 25 B3): the end is searched (within 0.5 s) for the spot whose last
    xf samples best match the xf samples before the loop start, which is what HISE's loop
    crossfade blends (StreamingSamplerSound 4.1.0). Returns ls, le, xf, correlation."""
    n = len(l)
    if p["gp"].get("llock"):                     # exact by construction: no search, no crossfade
        ls, le = llock_region(p, p["gp"], note)
        assert le <= n - int(0.02 * SR), f'{p["id"]} zone {note}: L-lock loop ends at {le}, past the render ({n}): raise dur'
        return ls, le, 0, 1.0
    atk = p["gp"].get("attack", 0.01)
    ls = int(p["gp"].get("loop_start", max(atk + 0.6, 1.0)) * SR)
    le0 = n - int(0.03 * SR)
    xf = int(min(0.35 * SR, (le0 - ls) * 0.45, ls * 0.8))
    m = (l + r) * 0.5
    ref = m[ls - xf: ls]
    srch = int(min(0.5 * SR, (le0 - ls) * 0.3))
    lo = le0 - srch
    seg = m[lo - xf: le0]
    if xf < 64 or srch < 16 or len(seg) < xf + srch:
        return ls, le0, xf, 1.0
    def best_end(lo_):
        seg_ = m[lo_ - xf: le0]
        num = np.correlate(seg_, ref, mode="valid")              # one value per candidate end
        c2 = np.concatenate([[0.0], np.cumsum(seg_.astype(np.float64) ** 2)])
        en = c2[xf:] - c2[:-xf]
        cr = num / (np.sqrt(en * float(np.dot(ref, ref))) + 1e-12)
        # near-ties (a steady tone matches at every period) are broken by position, not by
        # float noise: the candidate closest to the natural end within 0.005 of the best.
        # CI and a local render must pick the same end (the drift check compares maps).
        top = float(cr.max())
        kk_ = int(np.nonzero(cr >= top - 0.005)[0][-1])
        return lo_ + kk_, float(cr[kk_])

    le, cbest = best_end(lo)
    # chorus / detuned stacks: search the whole body, but never below a 2 s loop (a noise-like
    # zone otherwise landed on a random sub-second spot, review); still poor = natural end
    lo_full = ls + max(xf + int(0.3 * SR), int(2.0 * SR))
    if cbest < 0.3 and lo_full < lo:
        le2, c2best = best_end(lo_full)
        if c2best > cbest:
            le, cbest = le2, c2best
    if cbest < 0.3:
        le = le0
    if p["gen"] in ("sub", "reese"):             # periodic sources: also whole periods
        per = SR / dsp.mtof(note)
        kk = max(1, int(round((le - ls) / per)))
        le = min(le0, ls + int(round(kk * per)))
    return ls, le, xf, cbest


def render_preset(p) -> list[dict]:
    n = int(p["dur"] * SR)
    zones = []
    raw = []
    layers = p.get("vl", 1)
    if layers >= 3 or p.get("rr", 1) > 1:
        return render_preset_multi(p)
    for note in zone_roots(p["z"]):
        hard_l, hard_r = zone_render(p, p["gp"], note, n, seed_for(p["id"], note))
        nz = len(hard_l)
        # keyboard balance: one gain per zone from the HARD layer, shared by both layers
        rms = loud400(hard_l, hard_r)
        tilt_db = -max(0, note - 72) * 0.12                 # tame the very top
        g = (10 ** (tilt_db / 20.0)) * 0.18 / rms
        if layers == 2:
            sl, sr_ = render_voice(p, soften(p["gen"], p["gp"]), note, nz,
                                   np.random.default_rng(seed_for(p["id"], note) ^ 0x50F7))
            sv = p["gp"].get("soft_level", SOFT_LEVEL)
            # level-match the soft take to its own hard take before soft_level (docs/30 A):
            # a separately seeded soft render's loudness is random per zone, so the shared gain
            # left 3-13 dB jumps between neighbouring soft zones (paper_mute_upright 12.6 dB at
            # 68->72) and let a loud soft take set the whole preset's gain
            m = rms / max(loud400(sl, sr_), 1e-9)
            raw.append((note, 1, sl * g * m * sv, sr_ * g * m * sv))
            raw.append((note, 2, hard_l * g, hard_r * g))
        else:
            raw.append((note, 0, hard_l * g, hard_r * g))
    # one gain per instrument, set by LOUDNESS (loudest zone body RMS -> 0.12) so
    # presets are level-matched while browsing; a soft-knee peak limiter above
    # 0.6 catches attack spikes instead of letting them set the whole gain.
    rms_max = max(loud400(l, r) for _, _, l, r in raw)
    norm = 0.12 / max(rms_max, 1e-9)        # about -18 dBFS RMS per voice: headroom for chords + FX

    def limit(x):
        a = np.abs(x)
        over = a > 0.6
        y = x.copy()
        y[over] = np.sign(x[over]) * (0.6 + 0.35 * np.tanh((a[over] - 0.6) / 0.35))
        return y

    for note, layer, l, r in raw:
        l = limit(l * norm)
        r = limit(r * norm)
        if not p["loop"]:
            fade = int(0.04 * SR)
            ramp = np.linspace(1.0, 0.0, fade)
            l[-fade:] *= ramp
            r[-fade:] *= ramp
        zones.append(dict(note=note, layer=layer, l=l, r=r))
    return zones


def render_preset_multi(p) -> list[dict]:
    """docs/27 E0: velocity layers 1..6 rendered along a physical axis (gp vel_axis
    {param, values}: hammer speed, drive, pressure), never gain-only, and round robins 1..5
    with their own seeds (RR 1 keeps the preset's seed). One gain per zone, from its loudest
    layer and RR 1, shared by every take so the physics sets the level steps."""
    n = int(p["dur"] * SR)
    layers = p.get("vl", 1)
    rrs = p.get("rr", 1)
    ax = p["gp"].get("vel_axis") or {}
    raw = []
    for note in zone_roots(p["z"]):
        takes = []
        n_note = int(fdsp.F_DUR[p["gen"]](note, p["gp"]) * SR) if p["gen"] in fdsp.F_DUR else n
        for li in range(layers):
            gp = dict(p["gp"])
            if ax and len(ax.get("values", [])) == layers:     # an explicit physical axis always wins
                gp[ax["param"]] = ax["values"][li]
            elif layers == 2 and li == 0:
                gp = soften(p["gen"], p["gp"])
            for rk in range(rrs):
                seed = seed_for(p["id"], note) ^ (rk << 12) ^ (li << 20)
                gpr = dict(gp)
                gpr["_rr"] = rk if rrs > 1 else 1         # 0..rrs-1 (thermal state etc.)
                gpr["_nrr"] = rrs
                l, r = zone_render(p, gpr, note, n_note, seed)
                takes.append((li, rk, l, r))
        nz = min(len(t[2]) for t in takes)
        sc = p["gp"].get("layer_db_scale")
        if sc is not None and layers > 1:
            # keep each layer's timbre, shrink its level step to the top layer (dB x sc): a
            # struck instrument's full pp-ff range (25-30 dB) leaves the soft layers inaudible
            # next to the rest of the bank. RRs of a layer share the gain of its RR 1.
            lv_db = {li: 20.0 * math.log10(loud400(l, r) + 1e-12) for li, rk, l, r in takes if rk == 0}
            lg = {li: 10 ** ((1.0 - sc) * (lv_db[layers - 1] - lv_db[li]) / 20.0) for li in lv_db}
            takes = [(li, rk, l * lg[li], r * lg[li]) for li, rk, l, r in takes]
        top = [t for t in takes if t[0] == layers - 1 and t[1] == 0][0]
        tilt_db = -max(0, note - 72) * 0.12
        g = (10 ** (tilt_db / 20.0)) * 0.18 / loud400(top[2], top[3])
        for li, rk, l, r in takes:
            raw.append((note, li + 1 if layers > 1 else 0, rk, l[:nz] * g, r[:nz] * g))
    rms_max = max(loud400(l, r) for _, _, _, l, r in raw)
    norm = 0.12 / max(rms_max, 1e-9)
    ceil = p["gp"].get("peak_ceiling")
    if ceil:                                       # a strike's transient is physics: scale, never limit
        pk_max = max(max(float(np.abs(l).max()), float(np.abs(r).max())) for _, _, _, l, r in raw)
        norm = min(norm, ceil / max(pk_max, 1e-9))
    zones = []
    for note, layer, rk, l, r in raw:
        l = l * norm
        r = r * norm
        a = np.abs(np.concatenate([l, r]))
        if a.max() > 0.6 and not ceil:             # same soft limiter as render_preset
            def lim(x):
                ax_ = np.abs(x)
                y = x.copy()
                o = ax_ > 0.6
                y[o] = np.sign(x[o]) * (0.6 + 0.35 * np.tanh((ax_[o] - 0.6) / 0.35))
                return y
            l, r = lim(l), lim(r)
        if not p["loop"]:
            fade = int(0.04 * SR)
            ramp = np.linspace(1.0, 0.0, fade)
            l[-fade:] *= ramp
            r[-fade:] *= ramp
        zones.append(dict(note=note, layer=layer, rr=rk, l=l, r=r))
    return zones


def vel_ranges(p):
    """Velocity range per layer: vl 1/2 keep the bank's fixed split (85), vl 3..6 split evenly
    or at gp vel_splits (the boundaries, ascending)."""
    vl = p.get("vl", 1)
    if vl <= 2:
        return {0: (0, 127), 1: (0, 84), 2: (85, 127)}
    cuts = p["gp"].get("vel_splits") or [round(128 * k / vl) for k in range(1, vl)]
    edges = [0] + list(cuts) + [128]
    return {k + 1: (edges[k], edges[k + 1] - 1) for k in range(vl)}


def write_preset_audio(p, zones) -> None:
    roots = sorted(set(z["note"] for z in zones))
    step = p["z"][2]
    entries = []
    today = date.today().isoformat()
    VEL = vel_ranges(p)
    corrs = []
    loops = []
    for i, z in enumerate(zones):
        note = z["note"]
        layer = z["layer"]
        fname = f"SIG_{p['id']}_{note}.wav" if layer == 0 else f"SIG_{p['id']}_{note}_v{layer}.wav"
        rk = z.get("rr", 0)
        if rk:
            fname = fname[:-4] + f"_r{rk + 1}.wav"
        rng = np.random.default_rng(seed_for(p["id"], note) ^ 0x5EED ^ layer)
        if "flagship" in p["tags"] and np.array_equal(z["l"], z["r"]):
            write_wav24_mono(SAMPLES / fname, z["l"], rng)          # dry mono flagship: half the size
        else:
            write_wav24(SAMPLES / fname, z["l"], z["r"], rng)
        meta = {
            "filename": fname,
            "source": {
                "license": "research-facility-original",
                "uploader": "Research Facility procedural synthesis",
                "url": "",
                "downloaded": today,
                "generator": "scripts/build_signature_bank.py",
            },
            "musical": {"category": p["cat"], "tags": p["tags"], "root_midi": note,
                        "preset": p["name"]},
        }
        if p["gp"].get("tune_check"):               # docs/27 bar 9: the flagship QA tunes these
            f_key = fdsp.F_LOW[p["gen"]](note) if p["gen"] in fdsp.F_LOW else dsp.mtof(note)
            meta["musical"]["f0_hz"] = round(f_key * p["gp"].get("tune_ratio", 1.0)
                                             + p["gp"].get("tune_offset_hz", 0.0), 4)
            meta["musical"]["tune_c"] = p["gp"].get("tune_c", 1.0)
            if p["gp"].get("tune_win"):              # percussive: tune the strike, not the decay
                meta["musical"]["tune_win"] = p["gp"]["tune_win"]
        if p["gp"].get("llock"):
            meta["musical"]["llock"] = True
        (SAMPLES / (fname + ".meta.json")).write_text(json.dumps(meta, indent=2))
        ri = roots.index(note)
        lo = 0 if ri == 0 else note - step // 2
        hi = 127 if ri == len(roots) - 1 else note + (step - step // 2) - 1
        lov, hiv = VEL[layer]
        n = len(z["l"])
        if p["loop"]:
            ls, le, xf, cc = loop_points(p, z["l"], z["r"], note)
            corrs.append(cc)
            if xf >= 64 and ls >= xf:
                loops.append((z["l"], z["r"], ls, le, xf))
            loop_attr = f'LoopStart="{ls}" LoopEnd="{le}" LoopXFade="{xf}" LoopEnabled="1"'
        else:
            loop_attr = 'LoopStart="0" LoopEnd="0" LoopXFade="0" LoopEnabled="0"'
        entries.append(
            f'  <sample ID="{i}" FileName="{{PROJECT_FOLDER}}{fname}" Root="{note}" HiKey="{hi}"\n'
            f'          LoKey="{lo}" LoVel="{lov}" HiVel="{hiv}" RRGroup="{z.get("rr", 0) + 1}" Volume="0" Pan="0"\n'
            f'          Normalized="0" Pitch="0" SampleStart="0" SampleEnd="{n}"\n'
            f'          SampleStartMod="0" {loop_attr}\n'
            f'          LowerVelocityXFade="0" UpperVelocityXFade="0" SampleState="0"\n'
            f'          NormalizedPeak="-1" Duplicate="0"/>')
    # doc 25 B3: when even the best loop end barely correlates with the loop start (noise,
    # chorus, beating partials) a linear crossfade dips; gamma 0.5 is equal power
    # the most linear gamma whose simulated crossfade dips stay above -5 dB on every zone
    # (correlation alone missed a zone that matched overall but cancelled mid-fade)
    gamma = "0.5"
    for g in ("1.0", "0.85", "0.7", "0.5"):
        if all(xfade_dip(l_, r_, ls_, le_, xf_, float(g)) >= -5.0 for l_, r_, ls_, le_, xf_ in loops):
            gamma = g
            break
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n\n'
           f'<samplemap ID="SIG_{p["id"]}" SaveMode="1" RRGroupAmount="{float(p.get("rr", 1))}" MicPositions=";"\n'
           f'           CrossfadeGamma="{gamma}">\n' + "\n".join(entries) + "\n</samplemap>\n")
    (MAPS / f"SIG_{p['id']}.xml").write_text(xml)


# ---------------------------------------------------------------------------
# browser data (embedded into the plugin as a script include)
# ---------------------------------------------------------------------------

LEGACY_DIR = PROJ / "UserPresets" / "Factory"
LEGACY_CAT = {"Pads": "pads", "Plucks": "plucks", "Basses": "bass", "Leads": "leads", "Textures": "pads"}
LEGACY_ENV = {"pads": (600, 2400), "plucks": (2, 600), "bass": (2, 300), "leads": (10, 400)}


def _read_wav(path: Path):
    """PCM 16 / 24-bit (or 32-bit int) WAV -> float32 stereo array [n, 2]."""
    with wave.open(str(path)) as w:
        ch, sw, n = w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        x = (np.where(v >= 1 << 23, v - (1 << 24), v)).astype(np.float32) / 8388608.0
    else:
        x = np.frombuffer(raw, "<i4").astype(np.float32) / 2147483648.0
    x = x.reshape(-1, ch)
    return np.repeat(x, 2, axis=1) if ch == 1 else x[:, :2]


def archive_trim(smap: str, group: str) -> float:
    """Level-match an archive map to the Signature Bank: loudest zone's loudest 400 ms RMS -> 0.12
    (the render_preset target). Basses are measured above 80 Hz so a sub is not read as loud
    as its energy and turned down too far. Capped so peak + the +2.5 dB air shelf <= -3 dBFS."""
    from scipy.signal import butter, sosfilt
    xml = (MAPS / f"{smap}.xml").read_text()
    files = sorted(set(re.findall(r'FileName="\{PROJECT_FOLDER\}([^"]+)"', xml)))
    sos = butter(2, 80.0, "highpass", fs=SR, output="sos")
    rms_max, peak = 1e-9, 1e-9
    for fn in files:
        f = SAMPLES / fn
        if not f.exists():
            continue
        x = _read_wav(f)
        peak = max(peak, float(np.abs(x).max()))
        body = x
        if group == "bass":
            body = sosfilt(sos, body, axis=0)
        rms_max = max(rms_max, loud400(body[:, 0], body[:, 1]))      # doc 25 B2: loudest 400 ms
    trim = 20.0 * math.log10(0.12 / rms_max)
    cap = -3.0 - 2.5 - 20.0 * math.log10(peak)
    return round(min(trim, cap), 1)


def legacy_presets() -> list[dict]:
    """The original 53-specimen Lab library, kept as the ARCHIVE category."""
    out = []
    catalog_tags = {}
    cat_file = SAMPLES / "_catalog.json"
    if cat_file.exists():
        for e in json.loads(cat_file.read_text()):
            catalog_tags[e.get("samplemap")] = e.get("tags", [])[:3] + e.get("mood", [])[:2]
    for f in sorted(LEGACY_DIR.glob("*/*.preset")):
        txt = f.read_text()
        vals = dict(re.findall(r'id="(\w+)" value="([^"]*)"', txt))
        smap = vals.get("SpecimenId")
        if not smap or not (MAPS / f"{smap}.xml").exists():
            continue
        group = LEGACY_CAT.get(f.parent.name, "pads")
        atk, rel = LEGACY_ENV[group]
        tone = float(vals.get("BrightnessKnob", 8000))
        mot_hz = float(vals.get("MovementKnob", 0.25))
        q = float(vals.get("WarmthKnob", 1.5))
        pid = "lab_" + re.sub(r"[^a-z0-9]+", "_", f.stem.lower()).strip("_")
        tags = ["lab-archive", f.parent.name.lower()] + [t for t in catalog_tags.get(smap, []) if t]
        out.append(dict(
            id=pid, name=f.stem, cat="archive", tags=tags[:5], map=smap,
            m=[tone, 0.25, max(0.0, min(1.0, (mot_hz - 0.1) / 2.5)), float(vals.get("WidthKnob", 0.5)),
               float(vals.get("LengthKnob", 0.25)), 0.12, float(vals.get("DriveKnob", 0.1)), 0.0],
            v=V(atk=atk, rel=rel, reso=max(0.5, min(4.5, q)), vel=0.4, lfo=max(0.05, min(4.0, mot_hz)),
                subsus=-6 if group in ("pads", "leads") else -30, trim=archive_trim(smap, group)),
            desc=f"Original Research Facility lab specimen ({f.parent.name.lower()[:-1]}).",
        ))
    return out


DEEP_REGISTRY = Path(__file__).resolve().parent / "deep_params.json"


def load_deep_registry() -> dict:
    return json.loads(DEEP_REGISTRY.read_text())


RENDER_KEYS = {"slow", "speed", "decim", "bbd", "ensemble", "vnd", "decim_drive", "tape", "reverse", "post_hp", "post_shelf",
               "attack", "loop_start", "t60", "soft_mul", "soft_level", "stage_order", "soft",
               "vel_axis", "vel_splits", "llock", "tune_check", "tune_c", "tune_ratio", "tune_offset_hz", "centroid_gate",
               "peak_ceiling", "layer_db_scale", "tune_win", "lowend_gate"}


def gen_keys() -> dict:
    """gp keys each generator can read (doc 25 B5), from its source and the generators and
    helpers it calls, so a typo or a key for a not-yet-built feature fails the build instead
    of rendering silently without it."""
    import inspect
    src = {name: inspect.getsource(fn) for name, fn in dsp.GENERATORS.items()}
    funcs = {nm: inspect.getsource(getattr(dsp, nm)) for nm in dir(dsp)
             if nm.startswith(("gen_", "_formant", "tape_age")) and callable(getattr(dsp, nm))}
    # flagship helpers that read gp (fork_strike, fork_t60, tine_dur, _tine_ref ...)
    funcs.update({nm: inspect.getsource(getattr(fdsp, nm)) for nm in dir(fdsp)
                  if nm.startswith(("fork_", "tine_", "_tine_")) and callable(getattr(fdsp, nm))})
    def keys_of(code, seen):
        ks = set(re.findall(r'p(?:\.get\(|\[)"([A-Za-z_0-9]+)"', code))
        for callee in set(re.findall(r"\b(gen_[a-z_0-9]+|_formant_filter|tape_age|fork_[a-z_0-9]+|_?tine_[a-z_0-9]+)\(", code)):
            if callee in funcs and callee not in seen:
                seen.add(callee)
                ks |= keys_of(funcs[callee], seen)
        return ks
    return {name: keys_of(code, set()) | RENDER_KEYS for name, code in src.items()}


def check_gp_keys(presets) -> None:
    known = gen_keys()
    bad = []
    for p in presets:
        extra = set(p["gp"]) - known.get(p["gen"], set())
        if extra:
            bad.append(f'{p["id"]} ({p["gen"]}): {sorted(extra)}')
    if bad:
        raise SystemExit("gp keys no generator reads (doc 25 B5):\n  " + "\n  ".join(bad))


def check_deep(pid: str, d: dict, reg: dict) -> None:
    """Build gate: every SHAPE value a preset sets must name a real control and sit in its range."""
    by_id = {e["id"]: e for e in reg["params"]}
    for k, v in d.items():
        assert k in by_id, f"{pid}: unknown SHAPE control {k}"
        e = by_id[k]
        assert e["kind"] != "proxy", f"{pid}: {k} is a proxy; set atk/rel in V() instead"
        assert e["min"] <= v <= e["max"], f"{pid}: {k}={v} outside {e['min']}..{e['max']}"


# Mod matrix (docs/16 Stage 2): source kinds decide which targets accept them.
# Slots per target are [voice-start, time-variant, envelope] (Interface.js addModulatorTarget).
MOD_SOURCE_KIND = {"LFO 1": "tv", "LFO 2": "tv", "LFO 3": "tv", "LFO 4": "tv", "Env 2": "env", "Env 3": "env",
                   "Velocity": "vs", "Key": "vs", "Random": "vs", "Mod Wheel": "tv", "Aftertouch": "tv"}
MOD_TARGET_SLOTS = {"A Pitch": (2, 2, 2), "A Level": (2, 2, 0), "Sub Level": (1, 2, 0),   # no env slot on gain targets
                    "Cutoff": (2, 2, 2), "Resonance": (1, 1, 1), "Grit": (0, 2, 0)}


def check_mod(pid: str, rows: list) -> None:
    """Build gate: every factory routing must name a real source/target pair the matrix can make."""
    used = {}
    for r in rows:
        assert set(r) <= {"Source", "Target", "Intensity", "Mode", "Inverted"}, f"{pid}: mod row fields {sorted(r)}"
        src, tgt = r["Source"], r["Target"]
        assert src in MOD_SOURCE_KIND, f"{pid}: unknown mod source {src}"
        assert tgt in MOD_TARGET_SLOTS, f"{pid}: unknown mod target {tgt}"
        slot = {"vs": 0, "tv": 1, "env": 2}[MOD_SOURCE_KIND[src]]
        used[(tgt, slot)] = used.get((tgt, slot), 0) + 1
        assert used[(tgt, slot)] <= MOD_TARGET_SLOTS[tgt][slot], f"{pid}: no free {MOD_SOURCE_KIND[src]} slot on {tgt}"
        lo, hi = (-12.0, 12.0) if tgt == "A Pitch" else (0.0, 1.0)
        assert lo <= r.get("Intensity", 0.25) <= hi, f"{pid}: {src}>{tgt} intensity outside {lo}..{hi}"
        assert r.get("Mode", "Scale") in ("Scale", "Unipolar", "Bipolar"), f"{pid}: mode {r.get('Mode')}"


def check_sample_maps() -> None:
    """Uniform voice handler gate (docs/16): one sample per key x velocity x round-robin in every map."""
    import xml.etree.ElementTree as ET
    for f in sorted(MAPS.glob("*.xml")):
        seen = {}
        for smp in ET.parse(f).getroot().iter("sample"):
            a = smp.attrib
            for k in range(int(a["LoKey"]), int(a["HiKey"]) + 1):
                for v in range(int(a["LoVel"]), int(a["HiVel"]) + 1):
                    key = (k, v, a.get("RRGroup", "1"))
                    assert key not in seen, f"{f.name}: key {k} vel {v} starts two samples ({seen[key]}, {a['FileName']})"
                    seen[key] = a["FileName"]


def write_deep_params(reg: dict) -> None:
    js = ["// AUTO-GENERATED by scripts/build_signature_bank.py from scripts/deep_params.json - do not edit by hand.",
          "// SHAPE page controls (docs/16 Stage 1): geometry, ranges and defaults in one place.",
          "const var DEEP_FILTER_TYPES = " + json.dumps(reg["filter_types"]) + ";",
          "const var DEEP_SUB_OCTAVES = " + json.dumps(reg["sub_octaves"]) + ";",
          "const var DEEP_PARAMS = ["]
    for i, e in enumerate(reg["params"]):
        js.append("    " + json.dumps(e, separators=(", ", ": ")) + ("," if i < len(reg["params"]) - 1 else ""))
    js.append("];")
    (SCRIPTS / "DeepParams.js").write_text("\n".join(js) + "\n")


def bank_records() -> list[dict]:
    recs = []
    reg = load_deep_registry()
    for p in PRESETS:
        check_deep(p["id"], p.get("d", {}), reg)
        check_mod(p["id"], p.get("mod", []))
        recs.append(dict(id=p["id"], name=p["name"], cat=p["cat"], tags=p["tags"],
                         map=f"SIG_{p.get('map') or p['id']}", m=[round(x, 4) for x in p["m"]], v=p["v"],
                         desc=p["desc"], d=p.get("d", {}), mod=p.get("mod", [])))
    recs.extend(legacy_presets())
    return recs


def write_bank_data(recs) -> None:
    js_recs = []
    for r in recs:
        js_recs.append({
            "id": r["id"], "name": r["name"], "cat": r["cat"], "tags": r["tags"], "map": r["map"],
            "m": r["m"], "atk": r["v"]["atk"], "rel": r["v"]["rel"], "reso": r["v"]["reso"],
            "vel": r["v"]["vel"], "lfo": r["v"]["lfo"], "dly": r["v"]["dly"],
            "subdec": r["v"]["subdec"], "subsus": r["v"]["subsus"], "trim": r["v"]["trim"],
            "desc": r["desc"],
        })
        if r.get("d"):
            js_recs[-1]["d"] = r["d"]
        if r.get("mod"):
            js_recs[-1]["mod"] = r["mod"]
    lines = [
        "// AUTO-GENERATED by scripts/build_signature_bank.py - do not edit by hand.",
        "// Research Facility factory bank: every sound the browser can load.",
        "// m = macros [TONE Hz, BODY, MOTION, WIDTH, SPACE, ECHO, GRIT, PUMP].",
        "",
        "const var FACTORY_DEFAULT = " + json.dumps(DEFAULT_PRESET) + ";",
        "const var PRESET_ALIASES = " + json.dumps(RETIRED) + ";       // retired id -> replacement",
        "const var FACTORY_CATS = " + json.dumps([c for c, _ in CATEGORIES]) + ";",
        "const var FACTORY_CAT_LABELS = " + json.dumps([lbl for _, lbl in CATEGORIES]) + ";",
        "const var FACTORY_VIBES = " + json.dumps(VIBES) + ";",
        "const var FACTORY_BANK = [",
    ]
    for i, r in enumerate(js_recs):
        lines.append("    " + json.dumps(r, separators=(", ", ": ")) + ("," if i < len(js_recs) - 1 else ""))
    lines.append("];")
    (SCRIPTS / "FactoryBank.js").write_text("\n".join(lines) + "\n")
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "signature_bank.json").write_text(json.dumps(
        {"default": DEFAULT_PRESET, "categories": CATEGORIES, "vibes": VIBES, "presets": js_recs}, indent=1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-only", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    # sanity: no producer / artist names in preset names
    banned = ["tainy", "drake", "40", "shebib", "flume", "bad bunny", "balvin", "ovo"]
    for p in PRESETS:
        low = p["name"].lower()
        assert not any(b in low.split() or b in low for b in banned if b != "40") and "40" not in low.split(), p["name"]
        for v in p["tags"]:
            assert v == v.lower()
    ids = [p["id"] for p in PRESETS]
    assert len(ids) == len(set(ids)), "duplicate preset id"
    assert DEFAULT_PRESET in ids
    for old, new in RETIRED.items():
        assert new in ids, f"retired {old}: replacement {new} is not in the bank"
        assert old not in ids, f"retired {old} is still in the bank"
    for p in PRESETS:
        if p.get("map"):
            assert p["map"] in ids and not next(q for q in PRESETS if q["id"] == p["map"]).get("map"), \
                f'{p["id"]}: map alias must name a preset that renders its own samples'
    check_gp_keys(PRESETS)

    SAMPLES.mkdir(parents=True, exist_ok=True)
    MAPS.mkdir(parents=True, exist_ok=True)
    if not args.data_only:
        todo = [p for p in PRESETS if (not args.only or p["id"] == args.only) and not p.get("map")]
        total_bytes = 0
        for k, p in enumerate(todo, 1):
            zones = render_preset(p)
            write_preset_audio(p, zones)
            sz = sum(len(z["l"]) * 4 for z in zones)
            total_bytes += sz
            print(f"[{k:2d}/{len(todo)}] {p['name']:<20s} {len(zones):2d} zones  {sz / 1e6:6.1f} MB", flush=True)
        print(f"audio total {total_bytes / 1e6:.1f} MB")
    write_deep_params(load_deep_registry())
    recs = bank_records()
    write_bank_data(recs)
    check_sample_maps()
    print(f"FactoryBank.js: {len(recs)} presets ({len(PRESETS)} signature + {len(recs) - len(PRESETS)} archive)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
