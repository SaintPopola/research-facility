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
  python3 scripts/build_signature_bank.py --only night_drive_keys
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import wave
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sigbank_dsp as dsp  # noqa: E402

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

def P(id, name, cat, tags, gen, gp, m, v, z, dur, loop, desc, vl=1):
    """vl = velocity layers (1 or 2). Layer 1 (soft) is rendered with a gentler
    excitation from soften(); layer 2 is the recipe as written."""
    return dict(id=id, name=name, cat=cat, tags=tags, gen=gen, gp=gp, m=m, v=v,
                z=z, dur=dur, loop=loop, desc=desc, vl=vl)


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


SOFT_RULES = {
    # gen: {param: multiplier}  (missing params are left alone)
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
SOFT_DEFAULT_LP = {"felt_piano": 3500, "modal": 5000, "voice": 3200, "karplus": 3000}
SOFT_LEVEL = 0.71          # soft layer sits ~3 dB under the hard layer


def soften(gen, gp):
    out = dict(gp)
    for k, mul in SOFT_RULES.get(gen, {}).items():
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


def render_voice(p, gp, note, n, rng):
    """One zone/layer. gp['slow'] < 1 renders a slowed-tape take that stays in
    tune: render higher and shorter, then stretch back (pitch, envelopes and
    spectrum all drop together, like tape at that speed)."""
    gen = dsp.GENERATORS[p["gen"]]
    slow = gp.get("slow", 1.0)
    if slow < 1.0:
        n_r = int(n * slow)
        l, r = gen(note - 12.0 * math.log2(slow), n_r, gp, rng)
        pos = np.linspace(0, n_r - 1, n)
        l = np.interp(pos, np.arange(n_r), l)
        r = np.interp(pos, np.arange(n_r), r)
    else:
        l, r = gen(note, n, gp, rng)
    if gp.get("decim"):
        l = dsp.decimate(l, gp["decim"], gp.get("decim_drive", 0.0))
        r = dsp.decimate(r, gp["decim"], gp.get("decim_drive", 0.0))
    if gp.get("reverse"):                      # reversed swell: ends on the attack
        l = l[::-1].copy()
        r = r[::-1].copy()
        fade = int(0.02 * SR)
        l[:fade] *= np.linspace(0.0, 1.0, fade)
        r[:fade] *= np.linspace(0.0, 1.0, fade)
    l = post_eq(np.nan_to_num(l), gp)
    r = post_eq(np.nan_to_num(r), gp)
    return l - np.mean(l), r - np.mean(r)


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


def loop_points(p, n, note):
    atk = p["gp"].get("attack", 0.01)
    ls = int(max(atk + 0.6, 1.0) * SR)
    le = n - int(0.03 * SR)
    if p["gen"] in ("sub", "reese"):             # periodic sources: snap to whole periods
        per = SR / dsp.mtof(note)
        k = max(1, int((le - ls) / per))
        le = ls + int(round(k * per))
    xf = int(min(0.35 * SR, (le - ls) * 0.45, ls * 0.8))
    return ls, le, xf


def render_preset(p) -> list[dict]:
    n = int(p["dur"] * SR)
    zones = []
    raw = []
    layers = p.get("vl", 1)
    for note in zone_roots(p["z"]):
        hard_l, hard_r = render_voice(p, p["gp"], note, n, np.random.default_rng(seed_for(p["id"], note)))
        # keyboard balance: one gain per zone from the HARD layer, shared by both layers
        win = slice(0, min(n, int(1.0 * SR)))
        rms = math.sqrt(float(np.mean((hard_l[win] ** 2 + hard_r[win] ** 2) * 0.5)) + 1e-12)
        tilt_db = -max(0, note - 72) * 0.12                 # tame the very top
        g = (10 ** (tilt_db / 20.0)) * 0.18 / rms
        if layers == 2:
            sl, sr_ = render_voice(p, soften(p["gen"], p["gp"]), note, n,
                                   np.random.default_rng(seed_for(p["id"], note) ^ 0x50F7))
            raw.append((note, 1, sl * g * SOFT_LEVEL, sr_ * g * SOFT_LEVEL))
            raw.append((note, 2, hard_l * g, hard_r * g))
        else:
            raw.append((note, 0, hard_l * g, hard_r * g))
    # one gain per instrument, set by LOUDNESS (loudest zone body RMS -> 0.12) so
    # presets are level-matched while browsing; a soft-knee peak limiter above
    # 0.6 catches attack spikes instead of letting them set the whole gain.
    win = slice(0, min(n, int(1.0 * SR)))
    rms_max = max(math.sqrt(float(np.mean((l[win] ** 2 + r[win] ** 2) * 0.5))) for _, _, l, r in raw)
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


def write_preset_audio(p, zones) -> None:
    roots = sorted(set(z["note"] for z in zones))
    step = p["z"][2]
    entries = []
    today = date.today().isoformat()
    VEL = {0: (0, 127), 1: (0, 84), 2: (85, 127)}
    for i, z in enumerate(zones):
        note = z["note"]
        layer = z["layer"]
        fname = f"SIG_{p['id']}_{note}.wav" if layer == 0 else f"SIG_{p['id']}_{note}_v{layer}.wav"
        rng = np.random.default_rng(seed_for(p["id"], note) ^ 0x5EED ^ layer)
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
        (SAMPLES / (fname + ".meta.json")).write_text(json.dumps(meta, indent=2))
        ri = roots.index(note)
        lo = 0 if ri == 0 else note - step // 2
        hi = 127 if ri == len(roots) - 1 else note + (step - step // 2) - 1
        lov, hiv = VEL[layer]
        n = len(z["l"])
        if p["loop"]:
            ls, le, xf = loop_points(p, n, note)
            loop_attr = f'LoopStart="{ls}" LoopEnd="{le}" LoopXFade="{xf}" LoopEnabled="1"'
        else:
            loop_attr = 'LoopStart="0" LoopEnd="0" LoopXFade="0" LoopEnabled="0"'
        entries.append(
            f'  <sample ID="{i}" FileName="{{PROJECT_FOLDER}}{fname}" Root="{note}" HiKey="{hi}"\n'
            f'          LoKey="{lo}" LoVel="{lov}" HiVel="{hiv}" RRGroup="1" Volume="0" Pan="0"\n'
            f'          Normalized="0" Pitch="0" SampleStart="0" SampleEnd="{n}"\n'
            f'          SampleStartMod="0" {loop_attr}\n'
            f'          LowerVelocityXFade="0" UpperVelocityXFade="0" SampleState="0"\n'
            f'          NormalizedPeak="-1" Duplicate="0"/>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n\n'
           f'<samplemap ID="SIG_{p["id"]}" SaveMode="1" RRGroupAmount="1.0" MicPositions=";"\n'
           '           CrossfadeGamma="1.0">\n' + "\n".join(entries) + "\n</samplemap>\n")
    (MAPS / f"SIG_{p['id']}.xml").write_text(xml)


# ---------------------------------------------------------------------------
# browser data (embedded into the plugin as a script include)
# ---------------------------------------------------------------------------

LEGACY_DIR = PROJ / "UserPresets" / "Factory"
LEGACY_CAT = {"Pads": "pads", "Plucks": "plucks", "Basses": "bass", "Leads": "leads", "Textures": "pads"}
LEGACY_ENV = {"pads": (600, 2400), "plucks": (2, 600), "bass": (2, 300), "leads": (10, 400)}


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
                subsus=-6 if group in ("pads", "leads") else -30),
            desc=f"Original Research Facility lab specimen ({f.parent.name.lower()[:-1]}).",
        ))
    return out


def bank_records() -> list[dict]:
    recs = []
    for p in PRESETS:
        recs.append(dict(id=p["id"], name=p["name"], cat=p["cat"], tags=p["tags"],
                         map=f"SIG_{p['id']}", m=[round(x, 4) for x in p["m"]], v=p["v"],
                         desc=p["desc"]))
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
    lines = [
        "// AUTO-GENERATED by scripts/build_signature_bank.py - do not edit by hand.",
        "// Research Facility factory bank: every sound the browser can load.",
        "// m = macros [TONE Hz, BODY, MOTION, WIDTH, SPACE, ECHO, GRIT, PUMP].",
        "",
        "const var FACTORY_DEFAULT = " + json.dumps(DEFAULT_PRESET) + ";",
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

    SAMPLES.mkdir(parents=True, exist_ok=True)
    MAPS.mkdir(parents=True, exist_ok=True)
    if not args.data_only:
        todo = [p for p in PRESETS if not args.only or p["id"] == args.only]
        total_bytes = 0
        for k, p in enumerate(todo, 1):
            zones = render_preset(p)
            write_preset_audio(p, zones)
            sz = sum(len(z["l"]) * 4 for z in zones)
            total_bytes += sz
            print(f"[{k:2d}/{len(todo)}] {p['name']:<20s} {len(zones):2d} zones  {sz / 1e6:6.1f} MB", flush=True)
        print(f"audio total {total_bytes / 1e6:.1f} MB")
    recs = bank_records()
    write_bank_data(recs)
    print(f"FactoryBank.js: {len(recs)} presets ({len(PRESETS)} signature + {len(recs) - len(PRESETS)} archive)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
