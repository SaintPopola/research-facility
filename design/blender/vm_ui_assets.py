"""Sweet Melody / Hook Lab vintage panel assets (docs/28 asset plan, docs/28b).

Headless only, factory-empty scenes (no user .blend or camera is touched):
    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
        --python design/blender/vm_ui_assets.py -- swatch <out_dir>

Step 0 is the TEST FRAME (vm_swatch, 2048x700 = 1024x350 logical at 2x): three wood
candidates, a panel patch with silkscreen, an XL and an L fluted knob, the four rocker
colours on and off, a red push up and down, one lit wheel in its slot, two white keys and
a black key, and a nameplate draft. The user picks the wood before any other asset.

Texture sources (CC0, approved per file, kept outside the repo; see docs/28 download log):
Poly Haven walnut_veneer / black_walnut_veneer_02 / sapele_veneer (2K), ambientCG
Metal028 / Metal051A / Plastic006 / Plastic010 (2K JPG maps only; the zips' .blend files
are never opened). No HDR was approved, so the world is a flat studio grey.
"""
import math
import os
import sys

import bpy

DL = os.path.expanduser("~/Desktop/Sweet Melody UI assets/downloads")
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hise_project", "ResearchFacility", "Images", "fonts")
PX = 0.000691                    # 1 logical px in metres (KeyWidth 34 = 23.5 mm white key)


def srgb(hexstr, a=1.0):
    h = hexstr.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (out[0], out[1], out[2], a)


def fresh_scene(res_x, res_y, samples=256):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    sc.cycles.device = "GPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.seed = 7
    sc.render.resolution_x = res_x
    sc.render.resolution_y = res_y
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    w = bpy.data.worlds.new("World")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.25, 0.25, 0.25, 1.0)
    bg.inputs["Strength"].default_value = 0.06
    sc.world = w
    return sc


def to_m(px, py, fw, fh):
    """Logical frame px (origin top-left) -> scene metres (origin centre, +Y up)."""
    return ((px - fw / 2.0) * PX, (fh / 2.0 - py) * PX)


def ortho_camera(fw):
    d = bpy.data.cameras.new("VM_Cam")
    d.type = "ORTHO"
    d.ortho_scale = fw * PX
    o = bpy.data.objects.new("VM_Cam", d)
    o.location = (0, 0, 1.0)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.scene.camera = o


def vm_rig():
    """Key softbox upper left (elevation ~55 deg, azimuth ~-30 deg), fill at 10%."""
    def area(name, loc, size, power, col):
        ld = bpy.data.lights.new(name, "AREA")
        ld.size = size
        ld.energy = power
        ld.color = col
        o = bpy.data.objects.new(name, ld)
        o.location = loc
        bpy.context.scene.collection.objects.link(o)
        tgt = bpy.data.objects.new(name + "_t", None)
        bpy.context.scene.collection.objects.link(tgt)
        c = o.constraints.new("TRACK_TO")
        c.target = tgt
        c.track_axis = "TRACK_NEGATIVE_Z"
        c.up_axis = "UP_Y"
        return o
    el, az, dist = math.radians(55), math.radians(-30), 7.0
    kx = -dist * math.cos(el) * math.sin(-az + math.pi / 2) * 0.6
    ky = dist * math.cos(el) * 0.8
    area("VM_Key", (kx, ky, dist * math.sin(el)), 3.0, 420.0, (1.0, 0.89, 0.80))      # ~4800 K
    area("VM_Fill", (2.0, -2.0, 5.0), 3.0, 42.0, (0.95, 0.97, 1.0))                     # 10% of the key
    area("VM_Rim", (0.0, 4.0, 2.0), 0.6, 25.0, (1.0, 1.0, 1.0))


def bsdf(name, base, rough=0.4, metallic=0.0, coat=0.0, coat_rough=0.1, aniso=0.0, transmission=0.0,
         emit=None, emit_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    b.inputs["Anisotropic"].default_value = aniso
    b.inputs["Transmission Weight"].default_value = transmission
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


def wood_mat(name, asset, tile_m, tint, coat, coat_rough, rough_mul=1.0, curl=False, edge=None, hsv=None):
    """Poly Haven veneer: diffuse x tint, roughness map, GL normal; object-space metres
    mapped so one image covers its physical tile. curl adds a figured-wood band pattern."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0 / tile_m, 1.0 / tile_m, 1.0 / tile_m)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    folder = os.path.join(DL, "polyhaven_" + asset)

    def img(kind, non_color):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(folder, f"{asset}_{kind}_2k.jpg"))
        if non_color:
            t.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        return t
    diff = img("diff", False)
    rough = img("rough", True)
    nor = img("nor_gl", True)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    src = diff.outputs["Color"]
    if hsv:                                                        # hue / saturation / value shift of the veneer
        hs = nt.nodes.new("ShaderNodeHueSaturation")
        hs.inputs["Hue"].default_value = hsv[0]
        hs.inputs["Saturation"].default_value = hsv[1]
        hs.inputs["Value"].default_value = hsv[2]
        nt.links.new(src, hs.inputs["Color"])
        src = hs.outputs["Color"]
    nt.links.new(src, mul.inputs[6])
    mul.inputs[7].default_value = tint
    col_out = mul.outputs[2]
    if curl:
        wave = nt.nodes.new("ShaderNodeTexWave")
        wave.bands_direction = "Y"                                   # flame bands run across the grain
        wave.inputs["Scale"].default_value = 120.0 * tile_m          # flame bands every ~8 mm
        wave.inputs["Distortion"].default_value = 1.6
        wave.inputs["Detail"].default_value = 2.0
        wave.inputs["Detail Scale"].default_value = 1.5
        nt.links.new(mp.outputs["Vector"], wave.inputs["Vector"])
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["To Min"].default_value = 0.60                     # bold cross-grain figure
        mr.inputs["To Max"].default_value = 1.40
        nt.links.new(wave.outputs["Fac"], mr.inputs["Value"])
        mul2 = nt.nodes.new("ShaderNodeMix")
        mul2.data_type = "RGBA"
        mul2.blend_type = "MULTIPLY"
        mul2.inputs["Factor"].default_value = 1.0
        nt.links.new(col_out, mul2.inputs[6])
        nt.links.new(mr.outputs["Result"], mul2.inputs[7])
        col_out = mul2.outputs[2]
    if edge:
        # darker panel-side edge (25%) for depth: object-space Y ramp over the last 20%
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
        er = nt.nodes.new("ShaderNodeMapRange")
        er.inputs["From Min"].default_value = edge[0]
        er.inputs["From Max"].default_value = edge[1]
        er.inputs["To Min"].default_value = 0.70
        er.inputs["To Max"].default_value = 1.0
        nt.links.new(sep.outputs["Y"], er.inputs["Value"])
        mul3 = nt.nodes.new("ShaderNodeMix")
        mul3.data_type = "RGBA"
        mul3.blend_type = "MULTIPLY"
        mul3.inputs["Factor"].default_value = 1.0
        nt.links.new(col_out, mul3.inputs[6])
        nt.links.new(er.outputs["Result"], mul3.inputs[7])
        col_out = mul3.outputs[2]
    nt.links.new(col_out, b.inputs["Base Color"])
    rm = nt.nodes.new("ShaderNodeMath")
    rm.operation = "MULTIPLY"
    rm.inputs[1].default_value = rough_mul
    nt.links.new(rough.outputs["Color"], rm.inputs[0])
    nt.links.new(rm.outputs["Value"], b.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.6
    nt.links.new(nor.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    if coat > 0:
        b.inputs["Coat Tint"].default_value = srgb("#F0B070")
    return m


def wood_figured(name, edge, block_h):
    """Figured amber cheek (docs/28 A, revised): long grain from black_walnut_veneer_02 along
    the board, toned through an amber ramp (darks #6E3418, mid #B8622E), crossed by curl
    bands with noise-warped, irregular 5-20 mm spacing, strength fading in and out, and the
    band phase flipped across 2.5 zones (chatoyance in a still frame). Darker panel-side
    edge, lacquer coat."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, 1.0, 1.0)              # black_walnut_veneer_02 is a 1 m tile
    L(tc.outputs["Object"], mp.inputs["Vector"])
    folder = os.path.join(DL, "polyhaven_black_walnut_veneer_02")

    def img(kind, non_color):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(folder, f"black_walnut_veneer_02_{kind}_2k.jpg"))
        if non_color:
            t.image.colorspace_settings.name = "Non-Color"
        L(mp.outputs["Vector"], t.inputs["Vector"])
        return t
    diff, rough, nor = img("diff", False), img("rough", True), img("nor_gl", True)
    # grain luminance -> amber ramp
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    L(diff.outputs["Color"], bw.inputs["Color"])
    lum = nt.nodes.new("ShaderNodeMapRange")
    lum.inputs["From Min"].default_value = 0.04
    lum.inputs["From Max"].default_value = 0.30
    L(bw.outputs["Val"], lum.inputs["Value"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    el = ramp.color_ramp.elements
    el[0].position = 0.0
    el[0].color = srgb("#5E2A12")
    el[1].position = 1.0
    el[1].color = srgb("#D08442")
    mid = el.new(0.5)
    mid.color = srgb("#B8622E")
    dk = el.new(0.2)
    dk.color = srgb("#6E3418")
    L(lum.outputs["Result"], ramp.inputs["Fac"])
    # curl bands across the grain (the grain runs along X)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    L(tc.outputs["Object"], sep.inputs["Vector"])
    warp = nt.nodes.new("ShaderNodeTexNoise")
    warp.inputs["Scale"].default_value = 14.0
    warp.inputs["Detail"].default_value = 1.0
    L(tc.outputs["Object"], warp.inputs["Vector"])

    def math(op, a, bb=None, v=None):
        n = nt.nodes.new("ShaderNodeMath")
        n.operation = op
        if hasattr(a, "bl_idname") or not isinstance(a, (int, float)):
            L(a, n.inputs[0])
        else:
            n.inputs[0].default_value = a
        if bb is not None:
            if isinstance(bb, (int, float)):
                n.inputs[1].default_value = bb
            else:
                L(bb, n.inputs[1])
        return n.outputs[0]
    # phase in cycles: ~85 per metre (12 mm) plus a strong noise warp -> 5-20 mm, bending bands
    ph = math("ADD", math("MULTIPLY", sep.outputs["X"], 85.0), math("MULTIPLY", math("SUBTRACT", warp.outputs["Fac"], 0.5), 9.0))
    # chatoyance: flip the band phase by half a cycle across 2.5 zones along the board's width
    zone = math("GREATER_THAN", math("SINE", math("MULTIPLY", sep.outputs["Y"], 2.0 * 3.14159 * 2.5 / block_h)), 0.0)
    ph = math("ADD", ph, math("MULTIPLY", zone, 0.5))
    band = math("SINE", math("MULTIPLY", ph, 2.0 * 3.14159))
    sharp = nt.nodes.new("ShaderNodeMapRange")                    # narrower bright bands
    sharp.inputs["From Min"].default_value = -0.2
    sharp.inputs["From Max"].default_value = 1.0
    sharp.clamp = True
    L(band, sharp.inputs["Value"])
    fade = nt.nodes.new("ShaderNodeTexNoise")                     # strength fades in and out
    fade.inputs["Scale"].default_value = 22.0
    L(tc.outputs["Object"], fade.inputs["Vector"])
    amp = nt.nodes.new("ShaderNodeMapRange")
    amp.inputs["From Min"].default_value = 0.38
    amp.inputs["From Max"].default_value = 0.66
    amp.clamp = True
    L(fade.outputs["Fac"], amp.inputs["Value"])
    fig = math("ADD", 0.82, math("MULTIPLY", math("MULTIPLY", sharp.outputs["Result"], amp.outputs["Result"]), 0.42))
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    L(ramp.outputs["Color"], mul.inputs[6])
    L(fig, mul.inputs[7])
    col = mul.outputs[2]
    # darker panel-side edge
    er = nt.nodes.new("ShaderNodeMapRange")
    er.inputs["From Min"].default_value = edge[0]
    er.inputs["From Max"].default_value = edge[1]
    er.inputs["To Min"].default_value = 0.70
    er.clamp = True
    L(sep.outputs["Y"], er.inputs["Value"])
    mul2 = nt.nodes.new("ShaderNodeMix")
    mul2.data_type = "RGBA"
    mul2.blend_type = "MULTIPLY"
    mul2.inputs["Factor"].default_value = 1.0
    L(col, mul2.inputs[6])
    L(er.outputs["Result"], mul2.inputs[7])
    L(mul2.outputs[2], b.inputs["Base Color"])
    L(rough.outputs["Color"], b.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.5
    L(nor.outputs["Color"], nm.inputs["Color"])
    L(nm.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Coat Weight"].default_value = 0.85
    b.inputs["Coat Roughness"].default_value = 0.14
    b.inputs["Coat Tint"].default_value = srgb("#F3D2A8")
    return m


def panel_mat():
    """Black paint on smooth aluminium: Metal028 roughness remapped to 0.38-0.5."""
    m = bsdf("VM_Panel", srgb("#1E1D1B"), rough=0.44, metallic=0.0)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    folder = os.path.join(DL, "ambientcg_Metal028", "x")
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(folder, "Metal028_2K-JPG_Roughness.jpg"))
    t.image.colorspace_settings.name = "Non-Color"
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (5.6, 5.6, 5.6)               # one 2K map per 177 mm tile
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = 0.38
    mr.inputs["To Max"].default_value = 0.50
    nt.links.new(t.outputs["Color"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    return m


def box(name, cx, cy, w, h, d, z0, mat, bevel=0.0006):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, z0 + d / 2.0))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, d)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        bv = o.modifiers.new("Chamfer", "BEVEL")
        bv.width = bevel
        bv.segments = 3
    o.data.materials.append(mat)
    return o


def cyl(name, cx, cy, r, d, z0, mat, verts=96, flutes=0, dome=0.0, bevel=0.0004):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=(cx, cy, z0 + d / 2.0))
    o = bpy.context.active_object
    o.name = name
    if flutes:                                       # one pass: shallow flutes on the skirt wall
        for v in o.data.vertices:
            ang = math.atan2(v.co.y, v.co.x)
            s = 1.0 - 0.045 * (0.5 + 0.5 * math.cos(ang * flutes))
            v.co.x *= s
            v.co.y *= s
    if dome > 0:
        for v in o.data.vertices:
            if v.co.z > 0:
                rr = math.hypot(v.co.x, v.co.y) / r
                v.co.z += dome * (1.0 - rr * rr)
    bpy.ops.object.shade_smooth()
    if bevel > 0:
        bv = o.modifiers.new("Chamfer", "BEVEL")
        bv.width = bevel
        bv.segments = 3
        bv.harden_normals = True
    o.data.materials.append(mat)
    return o


def text(name, body, cx, cy, size_px, mat, font_file, z0=0.0002, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.font = bpy.data.fonts.load(os.path.join(FONTS, font_file))
    cu.size = size_px * PX
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.extrude = 0.00005
    o = bpy.data.objects.new(name, cu)
    o.location = (cx, cy, z0)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    return o


def build_swatch(out):
    FW, FH = 1024, 350
    sc = fresh_scene(FW * 2, FH * 2, samples=256)
    ortho_camera(FW)
    vm_rig()
    P = lambda x, y: to_m(x, y, FW, FH)

    floor = bsdf("VM_Felt", srgb("#101112"), rough=0.9)
    box("Floor", 0, 0, FW * PX * 1.2, FH * PX * 1.2, 0.002, -0.004, floor, bevel=0)

    # three wood candidates, each 300 x 110 logical with a chamfer
    blk_h = 110 * PX
    woods = [("A FIGURED AMBER", wood_figured("VM_WoodA", (-blk_h / 2.0, -blk_h * 0.15), blk_h)),
             ("B UNSTAINED WALNUT", wood_mat("VM_WoodB", "black_walnut_veneer_02", 1.0, (1, 1, 1, 1), 0.0, 0.3, rough_mul=1.0)),
             ("C BUTTERSCOTCH", wood_mat("VM_WoodC", "walnut_veneer", 1.8, srgb("#F2C27A"), 0.2, 0.3))]
    ink = bsdf("VM_Silk", srgb("#E8E4D8"), rough=0.5)
    for i, (lab, mat) in enumerate(woods):
        x0 = 20 + i * 342
        cx, cy = P(x0 + 150, 75)
        box("Wood" + "ABC"[i], cx, cy, 300 * PX, 110 * PX, 0.012, 0.0, mat, bevel=0.0012)
        tx, ty = P(x0 + 150, 142)
        text("WoodLabel" + "ABC"[i], lab, tx, ty, 11, ink, "Jost-600-Semi.ttf", z0=0.0005)
    recv = bpy.data.collections.new("WoodRecv")
    recv.objects.link(bpy.data.objects["WoodA"])               # the lacquered candidate only
    sx, sy = P(170, 60)
    sld = bpy.data.lights.new("VM_Streak", "AREA")
    sld.shape = "RECTANGLE"
    sld.size = 0.5
    sld.size_y = 0.12
    sld.energy = 0.35
    so = bpy.data.objects.new("VM_Streak", sld)
    so.location = (sx, sy, 1.2)
    so.rotation_euler = (math.radians(-4), 0.0, math.radians(-8))
    bpy.context.scene.collection.objects.link(so)
    so.light_linking.receiver_collection = recv

    # panel patch: black paint, silk title, 0-10 scale around an XL knob
    px_, py_ = P(270, 262)
    box("Panel", px_, py_, 500 * PX, 156 * PX, 0.002, 0.0, panel_mat(), bevel=0.0003)
    tx, ty = P(150, 322)
    text("SilkTitle", "PERFORMANCE", tx, ty, 14, ink, "Jost-500-Medium.ttf", z0=0.0021)
    kx, ky = P(150, 250)
    skirt = bsdf("VM_Skirt", srgb("#0C0D0D"), rough=0.32, coat=0.4, coat_rough=0.15)
    alu = bsdf("VM_CapAlu", srgb("#C9CCCF"), rough=0.22, metallic=1.0, aniso=0.7)
    cyl("KnobXL_skirt", kx, ky, 28 * PX, 0.014, 0.002, skirt, verts=192, flutes=24)
    cyl("KnobXL_cap", kx, ky, 28 * 0.56 * PX, 0.0016, 0.016, alu, verts=128, dome=0.0008)
    for k in range(11):                               # 300 deg scale, numerals 0..10
        a = math.radians(-150 + 30 * k)
        r0, r1 = 31 * PX, 35 * PX
        ox, oy = math.sin(a), math.cos(a)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(kx + ox * (r0 + r1) / 2, ky + oy * (r0 + r1) / 2, 0.0021))
        d = bpy.context.active_object
        d.scale = (1.2 * PX, (r1 - r0), 0.00005)
        d.rotation_euler.z = -a
        d.data.materials.append(ink)
        if k % 2 == 0:
            text(f"Num{k}", str(k), kx + ox * 43 * PX, ky + oy * 43 * PX, 9, ink, "Jost-500-Medium.ttf", z0=0.0021)
    lx, ly = P(400, 230)                              # L knob near the corner
    cyl("KnobL_skirt", lx, ly, 22 * PX, 0.012, 0.002, skirt, verts=192, flutes=24)
    cyl("KnobL_cap", lx, ly, 22 * 0.56 * PX, 0.0014, 0.014, alu, verts=128, dome=0.0006)

    # rockers: orange, blue, cream, faded orange; off then on (tilted +/- 8 deg)
    cols = ["#E06A26", "#3F7BAA", "#E2DCCB", "#F09048"]
    bezel = bsdf("VM_Bezel", srgb("#0B0B0C"), rough=0.5)
    for i, c in enumerate(cols):
        base = srgb(c)
        m_on = bsdf("VM_RockerOn" + str(i), base, rough=0.22, coat=0.4, coat_rough=0.08, emit=base, emit_strength=0.08)
        m_off = bsdf("VM_RockerOff" + str(i), (base[0] * 0.8, base[1] * 0.8, base[2] * 0.8, 1.0), rough=0.6)
        for on in (0, 1):
            x = 560 + (i * 2 + on) * 46
            cx, cy = P(x, 200)
            box(f"RockBezel{i}{on}", cx, cy, 42 * PX, 26 * PX, 0.003, 0.0, bezel, bevel=0.0004)
            o = box(f"Rocker{i}{on}", cx, cy, 36 * PX, 20 * PX, 0.004, 0.003, m_on if on else m_off, bevel=0.0010)
            o.rotation_euler.x = math.radians(14 if on else -6)     # ON: top edge up into the light

    # red push: up and down (1 mm lower), in an aluminium ring
    red = bsdf("VM_PushRed", srgb("#C8321C"), rough=0.2, coat=0.6, coat_rough=0.05)
    red_dn = bsdf("VM_PushRedDown", srgb("#A42816"), rough=0.26, coat=0.5, coat_rough=0.08)
    ring = bsdf("VM_Ring", srgb("#C9CCCF"), rough=0.3, metallic=1.0)
    for j, down in enumerate((0, 1)):
        cx, cy = P(580 + j * 48, 280)
        cyl(f"PushRing{j}", cx, cy, 14 * PX, 0.003, 0.0, ring, verts=96)
        cyl(f"Push{j}", cx, cy, 11 * PX, 0.008 - 0.0035 * down, 0.002, red_dn if down else red, verts=96, dome=0.0008)

    # one lit clear wheel in its slot
    wx, wy = P(720, 270)
    box("WheelSlot", wx, wy, 40 * PX, 108 * PX, 0.004, -0.002, bezel, bevel=0.0004)
    acr = bsdf("VM_Acrylic", srgb("#F4EEE4"), rough=0.15, transmission=1.0)
    core = bsdf("VM_WheelCore", (0, 0, 0, 1), emit=srgb("#FFC27A"), emit_strength=1.0)
    w = cyl("Wheel", wx, wy, 52 * PX, 30 * PX, -0.012, acr, verts=180, flutes=60, bevel=0.0003)
    w.rotation_euler.y = math.radians(90)
    w.location.z = 0.0
    c = cyl("WheelCore", wx, wy, 30 * PX, 18 * PX, -0.008, core, verts=64, bevel=0)
    c.rotation_euler.y = math.radians(90)
    c.location.z = -0.004

    # keys: two white and one black
    ivory = bsdf("VM_Ivory", srgb("#E4E1D6"), rough=0.2)
    ebony = bsdf("VM_Ebony", srgb("#121010"), rough=0.25, coat=0.6, coat_rough=0.06)
    for k in range(2):
        cx, cy = P(770 + k * 34 + 17, 276)
        box(f"KeyW{k}", cx, cy, 33 * PX, 124 * PX, 0.012, 0.0, ivory, bevel=0.0006)
    cx, cy = P(804, 252)
    box("KeyB", cx, cy, 24 * PX, 77 * PX, 0.010, 0.012, ebony, bevel=0.0016)

    # nameplate draft: brushed aluminium with black engraved caps
    nx, ny = P(930, 300)
    plate = bsdf("VM_Plate", srgb("#141414"), rough=0.35, metallic=0.6, aniso=0.5)
    box("Nameplate", nx, ny, 170 * PX, 36 * PX, 0.0015, 0.0, plate, bevel=0.0005)
    cream = bsdf("VM_Engrave", srgb("#E8E4D8"), rough=0.45)
    text("PlateText", "SWEET MELODY", nx, ny + 4 * PX, 15, cream, "Jost-600-Semi.ttf", z0=0.0016)
    text("PlateSub", "RESEARCH FACILITY", nx, ny - 10 * PX, 7, cream, "Jost-500-Medium.ttf", z0=0.0016)

    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "vm_swatch.png")
    bpy.ops.render.render(write_still=True)
    print("VM swatch written", sc.render.filepath)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    what = argv[0] if argv else "swatch"
    out_dir = argv[1] if len(argv) > 1 else os.path.expanduser("~/CBR_previews")
    if what == "swatch":
        build_swatch(out_dir)
    else:
        raise SystemExit(f"unknown asset {what!r} (have: swatch)")
