#!/usr/bin/env python3
"""
Sweet Melody - STAGE visual assets (docs/18b Stage 1, Pillow only, no Blender).

Writes, at 2x for the 720x292 Visualiser:
  hise_project/ResearchFacility/Images/sm_stage_plate.png  1440x584 RGB, opaque
      stage black, gothic lancet ribs converging on the wall, unlit pixel towers
      and hanging strands, the LED wall bezel with a matte-black face, a haze glow
      behind the truss, floor spill, vignette, sheen, grain and 1-LSB dither, and
      the page background in the rounded corners (the panel is drawn opaque).
  hise_project/ResearchFacility/Images/sm_led_mesh.png     1024x312 RGBA
      2 px seams per 16x13 cell (32 x 12 cells) plus 1 px pixel-pitch lines at 35%.
  hise_project/ResearchFacility/Scripts/StageData.js
      CROWD_PTS, HAND_PTS, DOT_PTS, TRUSS_SEG, BOOTH_PTS, FASCIA_PTS, LAMP_X in
      1x panel pixels at the rest camera (vanishing point 360,120).
Stage 3 of docs/18b swaps in Blender plates under the same file names.
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "hise_project" / "ResearchFacility" / "Images"
SCR = ROOT / "hise_project" / "ResearchFacility" / "Scripts"
W, H = 720, 292                 # panel (1x)
S = 2                           # plate scale
VP = (360.0, 120.0)
BG = (0xD3, 0xD9, 0xDF)         # T.bg: the porcelain page behind the panel corners
WALL = (104, 42, 512, 156)


def rng(seed):
    return np.random.default_rng(seed)


def plate() -> None:
    w, h = W * S, H * S
    y = np.linspace(0.0, 1.0, h)[:, None]
    top, bot = np.array([0x07, 0x09, 0x0C], float), np.array([0x0A, 0x0D, 0x11], float)
    base = np.repeat((top * (1 - y) + bot * y)[:, None, :], w, axis=1).reshape(h, w, 3)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(img, "RGBA")
    vx, vy = VP[0] * S, VP[1] * S
    # gothic lancet ribs: 6 per side, from the outer frame toward the vanishing point
    for side in (-1, 1):
        for i in range(6):
            x0 = vx + side * (vx + 40 * S) * (0.35 + 0.13 * i)
            y0 = h * (1.05 - 0.17 * i)
            pts = []
            for t in np.linspace(0.0, 0.82, 24):
                px = x0 + (vx - x0) * t
                py = y0 + (vy - y0) * t - math.sin(t * math.pi) * 40 * S * (0.3 + 0.1 * i)
                pts.append((px, py))
            d.line(pts, fill=(0x16, 0x1B, 0x22, 150), width=2 * S)
    # unlit pixel towers with 12 off cells each
    for tx in (84, 624):
        d.rectangle([tx * S, 40 * S, (tx + 12) * S, 214 * S], fill=(0x0E, 0x11, 0x15, 255))
        for c in range(12):
            cy = 44 + c * 14
            d.rectangle([(tx + 2) * S, cy * S, (tx + 10) * S, (cy + 10) * S], fill=(0x15, 0x19, 0x1F, 255))
    # unlit hanging strands (bulbs every 9 px)
    r = rng(23)
    for lo, hi in ((20, 74), (644, 698)):
        for x in range(lo, hi + 1, 9):
            length = 60 + int(r.integers(0, 70))
            d.line([(x * S, 0), (x * S, length * S)], fill=(0x14, 0x18, 0x1D, 255), width=1 * S)
            for b in range(8, length, 9):
                d.ellipse([(x - 1.4) * S, (b - 1.4) * S, (x + 1.4) * S, (b + 1.4) * S], fill=(0x1A, 0x1F, 0x26, 255))
    # LED wall bezel + matte-black face (the LED_Screen Brightness 0 look)
    d.rectangle([102 * S, 40 * S, 618 * S, 200 * S], fill=(0x15, 0x19, 0x1E, 255))
    d.line([(102 * S, 40 * S), (618 * S, 40 * S)], fill=(0x2C, 0x33, 0x3C, 255), width=1 * S)
    d.rectangle([WALL[0] * S, WALL[1] * S, (WALL[0] + WALL[2]) * S - 1, (WALL[1] + WALL[3]) * S - 1], fill=(0x03, 0x04, 0x05, 255))
    arr = np.asarray(img, float)
    yy, xx = np.mgrid[0:h, 0:w] / S
    # neutral haze glow behind the truss (7%) and a floor spill (3.5%)
    glow = np.exp(-(((xx - 360) / 300) ** 2 + ((yy - 34) / 40) ** 2))
    spill = np.exp(-(((xx - 360) / 340) ** 2 + ((yy - 214) / 30) ** 2))
    outside_face = ~((xx >= WALL[0]) & (xx < WALL[0] + WALL[2]) & (yy >= WALL[1]) & (yy < WALL[1] + WALL[3]))
    arr += (255 * 0.07 * glow * outside_face)[..., None] * np.array([0.85, 0.92, 1.0])
    arr += (255 * 0.035 * spill)[..., None] * np.array([0.85, 0.92, 1.0])
    # vignette, then a 3% sheen over the top 18%
    vig = 1.0 - 0.35 * np.clip(((xx - 360) / 360) ** 2 + ((yy - 140) / 170) ** 2 - 0.25, 0, 1)
    arr *= vig[..., None]
    sheen = (yy < 0.18 * H) * 0.03
    arr = arr * (1 - sheen[..., None]) + 255 * sheen[..., None]
    # grain + 1-LSB TPDF dither
    g = rng(18)
    arr += g.normal(0.0, 1.1, arr.shape) + (g.random(arr.shape) - g.random(arr.shape))
    rgb = Image.fromarray(np.clip(np.round(arr), 0, 255).astype(np.uint8), "RGB")
    # page colour in the 6 px rounded corners (panel drawn opaque)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=6 * S, fill=255)
    out = Image.new("RGB", (w, h), BG)
    out.paste(rgb, (0, 0), mask)
    out.save(IMG / "sm_stage_plate.png", optimize=True)


def mesh() -> None:
    w, h = WALL[2] * S, WALL[3] * S                      # 1024 x 312: 1:1 over the wall at 2x
    a = np.zeros((h, w), float)
    yy, xx = np.mgrid[0:h, 0:w]
    a = np.maximum(a, ((xx % 8) == 0) * 0.35)            # 1 px lines at a 4 px LED pitch (1x)
    a = np.maximum(a, ((yy % 8) == 0) * 0.35)
    cw, ch = 16 * S, 13 * S
    a = np.maximum(a, (((xx % cw) < 2) | ((yy % ch) < 2)) * 0.9)   # 2 px seams per 16x13 cell
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 3] = np.round(a * 255).astype(np.uint8)    # black seams over the lit cells
    Image.fromarray(rgba, "RGBA").save(IMG / "sm_led_mesh.png", optimize=True)


def crowd_rows():
    """3 skyline polygons (back, mid, front) plus raised-arm and phone subsets."""
    rows, hands, dots = [], [], []
    spec = [(222.0, 13.0, 3.0, 0.8), (238.0, 17.0, 4.2, 0.9), (258.0, 24.0, 6.0, 1.0)]   # base y, spacing, head r
    for ri, (by, sp, hr, _k) in enumerate(spec):
        r = rng(100 + ri)
        pts = [-40.0, 340.0, -40.0, by + 6]
        figs = []
        x = -40.0 + sp * 0.5
        while x < 760.0:
            jx = x + float(r.uniform(-0.25, 0.25)) * sp
            hy = by - hr * 2.2 - float(r.uniform(0, 1.6 * hr))       # head height jitter
            sh = hr * 1.7                                            # half shoulder width
            sy = hy + hr * 2.4
            pts += [jx - sh, sy + 2, jx - sh * 0.8, sy, jx - hr * 0.55, sy - 0.4]
            for t in np.linspace(math.pi, 2 * math.pi, 7):           # head arc, left to right over the top
                pts += [jx + hr * math.cos(t), hy + hr * math.sin(t)]
            pts += [jx + hr * 0.55, sy - 0.4, jx + sh * 0.8, sy, jx + sh, sy + 2]
            figs.append((jx, hy, sy, sh, hr))
            x += sp
        pts += [760.0, by + 6, 760.0, 340.0]
        rows.append([round(v, 1) for v in pts])
        # hand subsets: 25%, +25%, +50% of the figures, one raised arm each (5-point polygon)
        order = list(range(len(figs)))
        r.shuffle(order)
        n = len(order)
        cuts = [order[: n // 4], order[n // 4: n // 2], order[n // 2:]]
        hs = []
        for sub in cuts:
            al = []
            for fi in sub:
                jx, hy, sy, sh, hrr = figs[fi]
                side = 1 if fi % 2 else -1
                ax = jx + side * sh * 0.75
                top = hy - hrr * (2.6 + float(r.uniform(0, 1.2)))
                lean = side * hrr * float(r.uniform(0.2, 0.9))
                wdt = max(1.0, hrr * 0.42)
                al += [ax - wdt, sy, ax + lean - wdt * 0.6, top + hrr, ax + lean, top,
                       ax + lean + wdt * 0.6, top + hrr, ax + wdt, sy]
            hs.append([round(v, 1) for v in al])
        hands.append(hs)
        if ri == 0:                                                   # phones in the back row, 3 twinkle subsets
            for sub in range(3):
                dl = []
                for fi in range(sub, len(figs), 5):
                    jx, hy, sy, sh, hrr = figs[fi]
                    dl += [round(jx + float(r.uniform(-2, 2)), 1), round(hy - 6 - float(r.uniform(0, 4)), 1), 1.1]
                dots.append(dl)
    return rows, hands, dots


def truss():
    seg = []
    for yc in (30.0, 37.0):
        seg += [-40.0, yc, 760.0, yc]
    x, up = -40.0, True
    while x < 760.0:
        seg += [x, 30.0 if up else 37.0, x + 12.0, 37.0 if up else 30.0]
        x += 12.0
        up = not up
    for mx in (180.0, 540.0):                                         # motor drops
        seg += [mx, 0.0, mx, 30.0]
    return seg


def booth():
    pts = [318.0, 216.0, 318.0, 202.0, 340.0, 202.0, 344.0, 197.0, 350.0, 194.0]
    for t in np.linspace(math.pi * 1.15, math.pi * 1.85, 7):         # DJ head
        pts += [round(360.0 + 6.0 * math.cos(t), 1), round(188.0 + 6.0 * math.sin(t), 1)]
    pts += [370.0, 194.0, 376.0, 197.0, 380.0, 202.0, 402.0, 202.0, 402.0, 216.0]
    return pts


def main() -> int:
    plate()
    mesh()
    rows, hands, dots = crowd_rows()
    js = ["// AUTO-GENERATED by scripts/build_stage_assets.py - do not edit by hand.",
          "// STAGE geometry (docs/18b) in 1x panel pixels at the rest camera (vanishing point 360,120).",
          "const var CROWD_PTS = " + json.dumps(rows) + ";",
          "const var HAND_PTS = " + json.dumps(hands) + ";",
          "const var DOT_PTS = " + json.dumps(dots) + ";",
          "const var TRUSS_SEG = " + json.dumps(truss()) + ";",
          "const var BOOTH_PTS = " + json.dumps(booth()) + ";",
          "const var FASCIA_PTS = " + json.dumps([300.0, 214.0, 420.0, 214.0, 420.0, 216.0, 300.0, 216.0]) + ";",
          "const var LAMP_X = " + json.dumps([200.0, 290.0, 430.0, 520.0]) + ";"]
    (SCR / "StageData.js").write_text("\n".join(js) + "\n")
    print("stage assets written:", [len(r) // 2 for r in rows], "crowd points;", sum(len(x) for h in hands for x in h) // 10, "arms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
