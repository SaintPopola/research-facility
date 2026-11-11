"""Probe: load a plug-in headless with pedalboard, render one note, report level."""
import sys
import numpy as np
from pedalboard import load_plugin

path = sys.argv[1]
sr = 48000
plugin = load_plugin(path)
print("loaded:", plugin.name, "| params:", len(plugin.parameters))
plugin([], duration=1.0, sample_rate=sr, num_channels=2, reset=False)   # warm-up (instruments take MIDI only)
midi = [(bytes([0x90, 60, 100]), 0.05), (bytes([0x80, 60, 0]), 1.5)]
audio = plugin(midi, duration=3.0, sample_rate=sr, num_channels=2)
rms = float(np.sqrt(np.mean(audio ** 2)))
print(f"rendered {audio.shape}, peak {float(np.abs(audio).max()):.4f}, rms {rms:.5f}", "SOUND" if rms > 1e-4 else "SILENT")
