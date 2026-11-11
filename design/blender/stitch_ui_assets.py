"""Stitch Blender frame renders into the filmstrips Sweet Melody loads.

    python3 design/blender/stitch_ui_assets.py <frames_dir>

Writes hise_project/ResearchFacility/Images/sm_*.png (embedded at export).
"""
import sys
from pathlib import Path
from PIL import Image

src = Path(sys.argv[1])
dst = Path(__file__).resolve().parents[2] / "hise_project" / "ResearchFacility" / "Images"
dst.mkdir(parents=True, exist_ok=True)


def strip(name, out):
    frames = sorted((src / name).glob("*.png"))
    first = Image.open(frames[0])
    w, h = first.size
    sheet = Image.new("RGBA", (w, h * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(Image.open(f).convert("RGBA"), (0, i * h))
    sheet.save(dst / out, optimize=True)
    print(out, sheet.size, len(frames), "frames")


strip("knob", "sm_knob_strip.png")
strip("orb", "sm_orb_strip.png")
Image.open(src / "backdrop" / "0001.png").convert("RGB").save(dst / "sm_backdrop.png", optimize=True)
Image.open(src / "logo" / "0001.png").convert("RGBA").save(dst / "sm_logo.png", optimize=True)
print("backdrop + logo written")
