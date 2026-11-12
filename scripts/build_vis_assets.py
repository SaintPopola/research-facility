#!/usr/bin/env python3
"""
Sweet Melody - visualiser plates (docs/18 Stage 1, static-stack fix).

Bakes everything the Visualiser used to composite on every frame into one
2x plate: glass gradient, the Blender chamber backdrop at 50%, the bottom fade
into glass, a soft vignette, the top sheen and a 1-LSB dither, with rounded
corners. The paint routine then draws this single image at full opacity.

  in : hise_project/ResearchFacility/Images/sm_backdrop.png   (1440x584 RGB)
  out: hise_project/ResearchFacility/Images/sm_backdrop_dim.png (1440x584 RGBA)
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "hise_project" / "ResearchFacility" / "Images"
GLASS_HI = np.array([0x1C, 0x22, 0x28], float)     # T.glassHi
GLASS = np.array([0x13, 0x17, 0x1C], float)        # T.glass


def main() -> int:
    src = np.asarray(Image.open(IMG / "sm_backdrop.png").convert("RGB"), float)
    h, w, _ = src.shape
    y = np.linspace(0.0, 1.0, h)[:, None, None]
    x = np.linspace(-1.0, 1.0, w)[None, :, None]
    base = GLASS_HI * (1.0 - y) + GLASS * y                       # glassHi -> glass, top to bottom
    out = base * 0.5 + src * 0.5                                   # backdrop at 50% (was setOpacity(0.5))
    fade = np.clip((y - 110.0 / 292.0) / (1.0 - 110.0 / 292.0), 0.0, 1.0) * (0xF2 / 255.0)
    out = out * (1.0 - fade) + GLASS * fade                        # bottom fade into glass (traces stay readable)
    r2 = x ** 2 + ((y - 0.45) * 1.6) ** 2
    out = out * (1.0 - 0.18 * np.clip(r2 - 0.35, 0.0, 1.0))        # soft vignette
    sheen = (y < 0.3).astype(float) * (0x0F / 255.0)
    out = out * (1.0 - sheen) + 255.0 * sheen                      # top sheen (was a translucent white fill)
    rng = np.random.default_rng(18)
    out = out + (rng.random(out.shape) - rng.random(out.shape))    # TPDF dither, 1 LSB: no gradient banding
    rgb = np.clip(np.round(out), 0, 255).astype(np.uint8)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=12, fill=255)   # 6 px corners at 1x
    plate = Image.fromarray(rgb, "RGB").convert("RGBA")
    plate.putalpha(mask)
    plate.save(IMG / "sm_backdrop_dim.png", optimize=True)
    print("wrote", IMG / "sm_backdrop_dim.png", plate.size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
