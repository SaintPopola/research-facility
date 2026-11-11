"""
Sweet Melody - 3D UI assets rendered headless in Blender 5.1 (Cycles, Metal).

  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
      --python design/blender/sm_ui_assets.py -- <asset> <out_dir>

asset = knob | orb | backdrop | logo | all
Each asset is built in a fresh empty scene (no user .blend is opened or saved).
Frames are written to <out_dir>/<asset>/####.png; stitch_ui_assets.py turns
them into the filmstrips the plugin loads from hise_project/.../Images.
"""

import math
import os
import sys

import bpy

TEAL = (0.0, 0.85, 0.63, 1.0)


# ---------------------------------------------------------------- helpers
def fresh_scene(res_x, res_y, samples=64, transparent=True):
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
    sc.render.resolution_x = res_x
    sc.render.resolution_y = res_y
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.004, 0.005, 0.007, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    sc.world = world
    return sc


def principled(name, base=(0.05, 0.05, 0.05, 1), metallic=0.0, rough=0.4, emit=None, emit_strength=0.0,
               transmission=0.0, ior=1.45, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = transmission
    b.inputs["IOR"].default_value = ior
    b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


def add_bump(mat, height_socket_builder):
    """Plug a procedural height into a Bump node on the material's normal."""
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    nt.links.new(height_socket_builder(nt), bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])


def knurl_height(nt, teeth=96):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    ang = nt.nodes.new("ShaderNodeMath"); ang.operation = "ARCTAN2"
    nt.links.new(sep.outputs["Y"], ang.inputs[0]); nt.links.new(sep.outputs["X"], ang.inputs[1])
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = float(teeth)
    nt.links.new(ang.outputs[0], mul.inputs[0])
    sin = nt.nodes.new("ShaderNodeMath"); sin.operation = "SINE"
    nt.links.new(mul.outputs[0], sin.inputs[0])
    return sin.outputs[0]


def rings_height(nt):
    w = nt.nodes.new("ShaderNodeTexWave")
    w.wave_type = "RINGS"
    w.inputs["Scale"].default_value = 60.0
    w.inputs["Distortion"].default_value = 0.0
    return w.outputs["Fac"]


def area_light(name, loc, rot, size, power, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, type="AREA")
    d.size = size
    d.energy = power
    d.color = color
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = rot
    bpy.context.scene.collection.objects.link(o)
    return o


def camera(loc, target=(0, 0, 0), lens=50.0, ortho=None):
    d = bpy.data.cameras.new("Cam")
    d.lens = lens
    if ortho:
        d.type = "ORTHO"
        d.ortho_scale = ortho
    o = bpy.data.objects.new("Cam", d)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    tgt = bpy.data.objects.new("CamTarget", None)
    tgt.location = target
    bpy.context.scene.collection.objects.link(tgt)
    c = o.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    bpy.context.scene.camera = o
    return o


def cylinder(name, r, depth, z, verts=96, bevel=0.0, mat=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=(0, 0, z))
    o = bpy.context.active_object
    o.name = name
    bpy.ops.object.shade_smooth()
    if bevel > 0:
        m = o.modifiers.new("Bevel", "BEVEL")
        m.width = bevel
        m.segments = 4
        m.harden_normals = True
    if mat:
        o.data.materials.append(mat)
    return o


def render_frames(out_dir, frames):
    os.makedirs(out_dir, exist_ok=True)
    sc = bpy.context.scene
    for f in range(1, frames + 1):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out_dir, f"{f:04d}.png")
        bpy.ops.render.render(write_still=True)


# ---------------------------------------------------------------- assets
def build_knob(out):
    """64-frame machined knob cap: knurled anodized skirt, brushed top,
    glowing teal indicator. Frame 1 = minimum (-135 deg), 64 = maximum."""
    fresh_scene(128, 128, samples=48, transparent=True)
    rot = bpy.data.objects.new("KnobRot", None)
    bpy.context.scene.collection.objects.link(rot)

    skirt_m = principled("Skirt", base=(0.035, 0.038, 0.045, 1), metallic=1.0, rough=0.34)
    add_bump(skirt_m, knurl_height)
    top_m = principled("Top", base=(0.055, 0.06, 0.07, 1), metallic=1.0, rough=0.26)
    add_bump(top_m, rings_height)
    ind_m = principled("Indicator", base=(0, 0, 0, 1), emit=TEAL, emit_strength=1.1)   # >1 clips to cyan under Standard

    skirt = cylinder("Skirt", 1.0, 0.34, 0.17, bevel=0.04, mat=skirt_m)
    top = cylinder("Top", 0.80, 0.12, 0.40, bevel=0.03, mat=top_m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.40, 0.465))
    ind = bpy.context.active_object
    ind.name = "Indicator"
    ind.scale = (0.055, 0.42, 0.012)
    ind.data.materials.append(ind_m)
    for o in (skirt, top, ind):
        o.parent = rot

    rot.rotation_euler = (0, 0, math.radians(135))
    rot.keyframe_insert("rotation_euler", frame=1)
    rot.rotation_euler = (0, 0, math.radians(-135))
    rot.keyframe_insert("rotation_euler", frame=64)
    for fc in rot.animation_data.action.fcurves if hasattr(rot.animation_data.action, "fcurves") else []:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

    camera((0, -1.0, 4.6), target=(0, 0, 0.2), lens=50)
    area_light("Key", (-2.2, -2.0, 4.0), (math.radians(40), 0, math.radians(-45)), 2.5, 420)
    area_light("Soft", (0.0, 0.0, 5.0), (0, 0, 0), 4.0, 45)
    area_light("Rim", (2.4, 2.6, 1.2), (math.radians(-70), 0, math.radians(135)), 2.0, 260, color=(0.2, 1.0, 0.8))
    area_light("Fill", (2.5, -2.5, 3.0), (math.radians(45), 0, math.radians(45)), 3.0, 120, color=(0.7, 0.8, 1.0))
    render_frames(out, 64)


def build_orb(out):
    """32-frame rotating holographic sphere (two wire shells + core)."""
    fresh_scene(256, 256, samples=32, transparent=True)
    rot = bpy.data.objects.new("OrbRot", None)
    bpy.context.scene.collection.objects.link(rot)
    wire_m = principled("Wire", base=(0, 0, 0, 1), emit=TEAL, emit_strength=1.15)
    wire2_m = principled("Wire2", base=(0, 0, 0, 1), emit=(0.25, 0.55, 1.0, 1), emit_strength=0.95)
    core_m = principled("Core", base=(0, 0, 0, 1), emit=(0.6, 1.0, 0.9, 1), emit_strength=0.95)
    for name, sub, r, mat, thick in (("ShellA", 2, 1.0, wire_m, 0.012), ("ShellB", 1, 0.72, wire2_m, 0.016)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r)
        o = bpy.context.active_object
        o.name = name
        w = o.modifiers.new("Wire", "WIREFRAME")
        w.thickness = thick
        o.data.materials.append(mat)
        o.parent = rot
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, segments=32, ring_count=16)
    core = bpy.context.active_object
    core.data.materials.append(core_m)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.25, minor_radius=0.008)
    ring = bpy.context.active_object
    ring.rotation_euler = (math.radians(72), 0, 0)
    ring.data.materials.append(wire_m)
    rot.rotation_euler = (math.radians(18), 0, 0)
    rot.keyframe_insert("rotation_euler", frame=1)
    rot.rotation_euler = (math.radians(18), 0, math.radians(360 * 31 / 32))
    rot.keyframe_insert("rotation_euler", frame=32)
    camera((0, -4.2, 0.0), target=(0, 0, 0), lens=50)
    render_frames(out, 32)


def build_backdrop(out):
    """Dark specimen chamber behind the spectrum (1440 x 584, opaque)."""
    sc = fresh_scene(1440, 584, samples=96, transparent=False)
    floor_m = principled("Floor", base=(0.01, 0.011, 0.013, 1), metallic=0.0, rough=0.18)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(floor_m)
    wall_m = principled("Wall", base=(0.006, 0.007, 0.009, 1), rough=0.8)
    nt = wall_m.node_tree
    b = nt.nodes["Principled BSDF"]
    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.wave_type = "BANDS"; wave.bands_direction = "X"; wave.inputs["Scale"].default_value = 18.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.985
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].color = (0.0, 0.5, 0.38, 1)
    nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 0.10
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 6, 0), rotation=(math.radians(90), 0, 0))
    bpy.context.active_object.data.materials.append(wall_m)
    glass_m = principled("Glass", base=(0.9, 1, 1, 1), rough=0.04, transmission=1.0, ior=1.5)
    liquid_m = principled("Liquid", base=(0, 0.02, 0.016, 1), emit=TEAL, emit_strength=0.55)
    cap_m = principled("Cap", base=(0.03, 0.03, 0.035, 1), metallic=1.0, rough=0.3)
    for x, h, lv in ((-3.4, 1.6, 0.55), (0.0, 2.2, 0.7), (3.4, 1.3, 0.4)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.42, depth=h, location=(x, 0.6, h / 2))
        g = bpy.context.active_object; bpy.ops.object.shade_smooth(); g.data.materials.append(glass_m)
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.36, depth=h * lv, location=(x, 0.6, h * lv / 2 + 0.02))
        l = bpy.context.active_object; bpy.ops.object.shade_smooth(); l.data.materials.append(liquid_m)
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.46, depth=0.12, location=(x, 0.6, h + 0.06))
        c = bpy.context.active_object; bpy.ops.object.shade_smooth(); c.data.materials.append(cap_m)
    haze = bpy.data.materials.new("Haze")
    haze.use_nodes = True
    hn = haze.node_tree
    hn.nodes.remove(hn.nodes["Principled BSDF"])
    vol = hn.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = 0.008
    vol.inputs["Color"].default_value = (0.6, 0.9, 1.0, 1)
    hn.links.new(vol.outputs["Volume"], hn.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1.5, 2.5))
    hz = bpy.context.active_object
    hz.scale = (14, 8, 5)
    hz.data.materials.append(haze)
    area_light("Top", (0, 0.6, 5.5), (0, 0, 0), 4.0, 150, color=(0.6, 1.0, 0.9))
    for lt in (area_light("RimL", (-6, 2, 2), (0, math.radians(-80), 0), 3.0, 90, color=(0.2, 0.9, 0.75)),
               area_light("RimR", (6, 2, 2), (0, math.radians(80), 0), 3.0, 70, color=(0.35, 0.5, 1.0))):
        lt.visible_glossy = False        # no bright light-card reflections on the floor
    camera((0, -9.8, 1.9), target=(0, 1.0, 1.0), lens=28)
    sc.frame_set(1)
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "0001.png")
    bpy.ops.render.render(write_still=True)


def build_logo(out):
    """Small 3D glass vial mark (128 x 128, transparent)."""
    sc = fresh_scene(128, 128, samples=64, transparent=True)
    glass_m = principled("Glass", base=(0.9, 1, 1, 1), rough=0.04, transmission=1.0, ior=1.5)
    liquid_m = principled("Liquid", base=(0, 0.05, 0.04, 1), emit=TEAL, emit_strength=1.1)
    cap_m = principled("Cap", base=(0.04, 0.04, 0.045, 1), metallic=1.0, rough=0.3)
    cylinder("Vial", 0.5, 2.0, 1.0, verts=64, mat=glass_m)
    cylinder("Liquid", 0.42, 1.1, 0.58, verts=64, mat=liquid_m)
    cylinder("Cap", 0.55, 0.18, 2.09, verts=64, bevel=0.03, mat=cap_m)
    area_light("Key", (-2, -3, 3), (math.radians(55), 0, math.radians(-35)), 2.0, 260)
    area_light("Rim", (2, 2, 2), (math.radians(-60), 0, math.radians(135)), 2.0, 200, color=(0.2, 1.0, 0.8))
    camera((0, -5.4, 2.2), target=(0, 0, 1.05), lens=50)
    sc.frame_set(1)
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, "0001.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["all", "/tmp/sm_ui"]
    which, out_dir = argv[0], argv[1]
    builders = {"knob": build_knob, "orb": build_orb, "backdrop": build_backdrop, "logo": build_logo}
    for name in (builders if which == "all" else [which]):
        builders[name](os.path.join(out_dir, name))
        print(f"SM_UI_ASSET_DONE {name}", flush=True)
