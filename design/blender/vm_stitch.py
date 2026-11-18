"""Stitch vm_ui_assets.py frames into vertical strips for HISE (docs/28 Phase 4).

    python3 design/blender/vm_stitch.py <frames_dir> [asset ...]

Checks per strip: frame 16 against frame 0 (periodic seam, mean absolute difference under
1/255), the alpha bounding box inside the frame (2 px margin), strip height at most 16384.
Writes hise_project/ResearchFacility/Images/vm_<asset>_2x.png (and the Hook Lab copy) plus a
manifest line per asset (px, frames, RAM, sha256) in design/blender/vm_manifest.txt.
"""
import hashlib
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DSTS = [ROOT / "hise_project" / "ResearchFacility" / "Images", ROOT / "hise_project" / "HookLab" / "Images"]
MANIFEST = ROOT / "design" / "blender" / "vm_manifest.txt"


def edge_fade(im, r_in=0.84, r_out=0.93):
    """Soft radial alpha fade so the cast shadow never meets the frame edge."""
    a = np.asarray(im).astype(np.float64)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - (w - 1) / 2.0, yy - (h - 1) / 2.0) / (min(w, h) / 2.0)
    m = np.clip((r_out - r) / (r_out - r_in), 0.0, 1.0)
    a[:, :, 3] *= m
    return Image.fromarray(a.round().astype(np.uint8), "RGBA")


def rect_fade(im, px=3):
    """Linear alpha fade over the last `px` pixels of a rectangular sprite."""
    a = np.asarray(im).astype(np.float64)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    a[:, :, 3] *= np.clip((d - 1.0) / px, 0.0, 1.0)
    return Image.fromarray(a.round().astype(np.uint8), "RGBA")


SPRITES = {"rocker": 8, "push_red": 2}        # non-periodic sprite sheets: frame count


def stitch(frames_dir, asset, n=16):
    src = Path(frames_dir) / asset
    if asset in SPRITES:
        n = SPRITES[asset]
        fr = [rect_fade(Image.open(src / f"{k:04d}.png").convert("RGBA")) for k in range(n)]
        fr.append(fr[0])                        # no seam to check
    else:
        fr = [edge_fade(Image.open(src / f"{k:04d}.png").convert("RGBA")) for k in range(n + 1)]
    w, h = fr[0].size
    a0 = np.asarray(fr[0], dtype=np.float64) / 255.0
    a16 = np.asarray(fr[n], dtype=np.float64) / 255.0
    mad = float(np.abs(a0 - a16).mean())
    alpha = np.asarray(fr[0])[:, :, 3]
    ys, xs = np.nonzero(alpha > 2)
    margin_ok = xs.min() >= 1 and ys.min() >= 1 and xs.max() <= w - 2 and ys.max() <= h - 2
    sheet = Image.new("RGBA", (w, h * n), (0, 0, 0, 0))
    for k in range(n):
        sheet.paste(fr[k], (0, k * h))
    assert sheet.size[1] <= 16384
    name = f"vm_{asset}_2x.png"
    for d in DSTS:
        d.mkdir(parents=True, exist_ok=True)
        sheet.save(d / name, optimize=True)
    data = (DSTS[0] / name).read_bytes()
    line = f"{name} {w}x{h * n} frames={n} ram={w * h * n * 4 / 1048576:.2f}MiB sha256={hashlib.sha256(data).hexdigest()[:16]} seam_mad={mad * 255:.3f}/255 margin={'ok' if margin_ok else 'CLIPPED'}"
    print(line)
    return line, mad < 1.0 / 255.0 and margin_ok


if __name__ == "__main__":
    frames_dir = sys.argv[1]
    assets = sys.argv[2:] or ["knob_l", "knob_s", "collet_l", "collet_s"]
    lines, ok = [], True
    for a in assets:
        ln, good = stitch(frames_dir, a)
        lines.append(ln)
        ok = ok and good
    old = MANIFEST.read_text().splitlines() if MANIFEST.exists() else []
    keep = [l for l in old if l.split(" ")[0] not in {x.split(" ")[0] for x in lines}]
    MANIFEST.write_text("\n".join(keep + lines) + "\n")
    print("stitch", "OK" if ok else "FAILED (seam or margin)")
    sys.exit(0 if ok else 1)
