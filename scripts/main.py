"""
Animal Jiu Jitsu - Main Script (Single File Version)

This script creates a cartoon fox performing a shrimping/hip escape animation.
All code is contained in this single file to avoid Blender import issues.

Usage:
1. Open Blender 5.1
2. Go to Scripting workspace
3. Open this file in the Text Editor (Text > Open)
4. Press Alt+P or click "Run Script"
"""

import bpy
from mathutils import Euler, Vector
import math


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def rad(degrees):
    """Convert degrees to radians."""
    return math.radians(degrees)


# ============================================================
# MATERIALS
# ============================================================

def create_fox_material(name="Fox_Body", color=(0.9, 0.4, 0.1, 1.0), roughness=0.8):
    """Create a cartoon fox material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    nodes.clear()

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Specular IOR Level'].default_value = 0.3

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)

    # Link
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def create_mat_material(name="BJJ_Mat", color=(0.1, 0.3, 0.6, 1.0)):
    """Create a jiu jitsu mat material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    nodes.clear()

    # Principled BSDF (simplified - no checker pattern to avoid complexity)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.9  # Matte rubber look

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)

    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def get_all_fox_materials():
    """Create and return all fox materials."""
    return {
        'body': create_fox_material("Fox_Body", (0.9, 0.4, 0.1, 1.0)),
        'white': create_fox_material("Fox_White", (0.95, 0.92, 0.85, 1.0)),
        'dark': create_fox_material("Fox_Dark", (0.15, 0.08, 0.02, 1.0)),
        'nose': create_fox_material("Fox_Nose", (0.02, 0.02, 0.02, 1.0), 0.3),
    }


# ============================================================
# SCENE SETUP
# ============================================================

def clear_default_scene():
    """Remove default cube, light, and camera if they exist."""
    default_objects = ['Cube', 'Light', 'Camera']
    for name in default_objects:
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)


def create_ground_plane(size=10.0, name="Mat"):
    """Create a ground plane (jiu jitsu mat)."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = name

    mat = create_mat_material()
    plane.data.materials.append(mat)

    return plane


def setup_lighting():
    """Create 3-point lighting setup for the scene."""
    # Key light (main)
    bpy.ops.object.light_add(type='AREA', location=(4, -3, 5))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 500
    key_light.data.size = 3
    key_light.data.color = (1.0, 0.95, 0.9)

    direction = key_light.location.normalized()
    key_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Fill light (softer)
    bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 200
    fill_light.data.size = 4
    fill_light.data.color = (0.9, 0.95, 1.0)

    direction = fill_light.location.normalized()
    fill_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Rim light (back)
    bpy.ops.object.light_add(type='AREA', location=(0, 4, 3))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 300
    rim_light.data.size = 2

    direction = rim_light.location.normalized()
    rim_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def setup_camera(location=(5, -5, 3), target=(0, 0, 0.5)):
    """Create and position the camera."""
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.name = "Main_Camera"

    # Create empty target for camera to track
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=target)
    target_empty = bpy.context.active_object
    target_empty.name = "Camera_Target"

    # Add track-to constraint
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = target_empty
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Set as active camera
    bpy.context.scene.camera = camera

    return camera


def configure_eevee_render(resolution_x=1280, resolution_y=720, fps=24, samples=64):
    """Configure Eevee render settings."""
    scene = bpy.context.scene

    # Set render engine (try EEVEE_NEXT for Blender 4+, fallback to EEVEE)
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except:
        scene.render.engine = 'BLENDER_EEVEE'

    # Resolution
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = 100

    # Frame rate
    scene.render.fps = fps

    # Eevee settings
    eevee = scene.eevee
    eevee.taa_render_samples = samples
    eevee.taa_samples = 16

    # Output settings
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

    # Animation range
    scene.frame_start = 1
    scene.frame_end = fps * 10

    # Background color
    scene.world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
    scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.15, 0.18, 0.22, 1.0)

    print(f"Render configured: {resolution_x}x{resolution_y} @ {fps}fps")


def setup_scene():
    """Full scene setup."""
    clear_default_scene()
    create_ground_plane()
    setup_lighting()
    setup_camera()
    configure_eevee_render()
    print("Scene setup complete!")


# ============================================================
# FOX CREATION
# ============================================================

def create_fox_primitive(name="FoxRig"):
    """Create a simple fox from primitives with a basic armature."""
    print("Creating fox from primitives...")

    # Create armature
    bpy.ops.object.armature_add(location=(0, 0, 0.5))
    armature = bpy.context.active_object
    armature.name = name

    # Enter edit mode to add bones
    bpy.ops.object.mode_set(mode='EDIT')
    arm = armature.data

    # Get the default bone and make it the root
    root = arm.edit_bones[0]
    root.name = 'root'
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.2)

    # Spine chain
    spine = arm.edit_bones.new('spine_fk')
    spine.head = (0, 0, 0.2)
    spine.tail = (0, 0.3, 0.25)
    spine.parent = root

    spine_001 = arm.edit_bones.new('spine_fk.001')
    spine_001.head = spine.tail
    spine_001.tail = (0, 0.6, 0.3)
    spine_001.parent = spine

    spine_002 = arm.edit_bones.new('spine_fk.002')
    spine_002.head = spine_001.tail
    spine_002.tail = (0, 0.8, 0.35)
    spine_002.parent = spine_001

    # Head
    head = arm.edit_bones.new('head')
    head.head = spine_002.tail
    head.tail = (0, 1.1, 0.4)
    head.parent = spine_002

    # Left leg
    thigh_L = arm.edit_bones.new('thigh_fk.L')
    thigh_L.head = (0.15, 0.1, 0.2)
    thigh_L.tail = (0.15, 0.1, -0.1)
    thigh_L.parent = root

    shin_L = arm.edit_bones.new('shin_fk.L')
    shin_L.head = thigh_L.tail
    shin_L.tail = (0.15, 0.15, -0.35)
    shin_L.parent = thigh_L

    foot_L = arm.edit_bones.new('foot_fk.L')
    foot_L.head = shin_L.tail
    foot_L.tail = (0.15, 0.25, -0.35)
    foot_L.parent = shin_L

    # Right leg
    thigh_R = arm.edit_bones.new('thigh_fk.R')
    thigh_R.head = (-0.15, 0.1, 0.2)
    thigh_R.tail = (-0.15, 0.1, -0.1)
    thigh_R.parent = root

    shin_R = arm.edit_bones.new('shin_fk.R')
    shin_R.head = thigh_R.tail
    shin_R.tail = (-0.15, 0.15, -0.35)
    shin_R.parent = thigh_R

    foot_R = arm.edit_bones.new('foot_fk.R')
    foot_R.head = shin_R.tail
    foot_R.tail = (-0.15, 0.25, -0.35)
    foot_R.parent = shin_R

    # Front legs
    front_thigh_L = arm.edit_bones.new('front_thigh_fk.L')
    front_thigh_L.head = (0.12, 0.7, 0.3)
    front_thigh_L.tail = (0.12, 0.7, 0.05)
    front_thigh_L.parent = spine_002

    front_shin_L = arm.edit_bones.new('front_shin_fk.L')
    front_shin_L.head = front_thigh_L.tail
    front_shin_L.tail = (0.12, 0.75, -0.15)
    front_shin_L.parent = front_thigh_L

    front_thigh_R = arm.edit_bones.new('front_thigh_fk.R')
    front_thigh_R.head = (-0.12, 0.7, 0.3)
    front_thigh_R.tail = (-0.12, 0.7, 0.05)
    front_thigh_R.parent = spine_002

    front_shin_R = arm.edit_bones.new('front_shin_fk.R')
    front_shin_R.head = front_thigh_R.tail
    front_shin_R.tail = (-0.12, 0.75, -0.15)
    front_shin_R.parent = front_thigh_R

    # Tail
    tail = arm.edit_bones.new('tail_fk')
    tail.head = (0, -0.05, 0.2)
    tail.tail = (0, -0.4, 0.4)
    tail.parent = root

    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create mesh body from primitives
    _create_fox_body(armature)

    print(f"Fox rig '{name}' created with {len(arm.bones)} bones")
    return armature


def _create_fox_body(armature):
    """Create simple mesh body and parent to armature."""
    materials = get_all_fox_materials()

    # Body (elongated sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.25,
        location=(0, 0.4, 0.28),
        scale=(0.8, 1.5, 0.7)
    )
    body = bpy.context.active_object
    body.name = "Fox_Body"
    body.data.materials.append(materials['body'])

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.15,
        location=(0, 0.95, 0.38)
    )
    head = bpy.context.active_object
    head.name = "Fox_Head"
    head.data.materials.append(materials['body'])

    # Snout (cone)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.08,
        radius2=0.02,
        depth=0.2,
        location=(0, 1.15, 0.35),
        rotation=(1.57, 0, 0)
    )
    snout = bpy.context.active_object
    snout.name = "Fox_Snout"
    snout.data.materials.append(materials['body'])

    # Ears (cones)
    for side, x in [('L', 0.08), ('R', -0.08)]:
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.05,
            radius2=0.01,
            depth=0.15,
            location=(x, 0.9, 0.55),
            rotation=(0, 0, 0)
        )
        ear = bpy.context.active_object
        ear.name = f"Fox_Ear_{side}"
        ear.data.materials.append(materials['body'])

    # Tail (tapered sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.08,
        location=(0, -0.2, 0.35),
        scale=(0.8, 2, 0.8)
    )
    tail = bpy.context.active_object
    tail.name = "Fox_Tail"
    tail.data.materials.append(materials['body'])

    # Simple legs (cylinders)
    leg_positions = [
        (0.15, 0.1, 0.05, 'Back_L'),
        (-0.15, 0.1, 0.05, 'Back_R'),
        (0.12, 0.7, 0.1, 'Front_L'),
        (-0.12, 0.7, 0.1, 'Front_R'),
    ]

    for x, y, z, leg_name in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.04,
            depth=0.4,
            location=(x, y, z)
        )
        leg = bpy.context.active_object
        leg.name = f"Fox_Leg_{leg_name}"
        leg.data.materials.append(materials['dark'])

    # Parent all mesh objects to armature
    mesh_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Fox_') and obj.type == 'MESH']
    for obj in mesh_objects:
        obj.select_set(True)

    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')


# ============================================================
# SHRIMPING ANIMATION
# ============================================================

def shrimp_escape(rig_name, start_frame=1, fps=24, direction='RIGHT'):
    """Create a shrimping/hip escape animation on a quadruped rig."""
    rig = bpy.data.objects.get(rig_name)
    if rig is None:
        print(f"Error: Rig '{rig_name}' not found")
        return start_frame

    # Ensure rig is selected and active
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)

    # Animation timing
    phase_duration = int(fps * 0.8)

    frame = start_frame
    dir_mult = 1 if direction == 'RIGHT' else -1

    # Phase 1: Guard position
    frame = _pose_guard(rig, frame, phase_duration)

    # Phase 2: Bridge
    frame = _pose_bridge(rig, frame, phase_duration, dir_mult)

    # Phase 3: Hip escape
    frame = _pose_escape(rig, frame, phase_duration, dir_mult)

    # Phase 4: Reset to guard
    frame = _pose_guard(rig, frame, phase_duration)

    print(f"Shrimp animation created: frames {start_frame} to {frame}")
    return frame


def _pose_guard(rig, start_frame, duration):
    """Set guard position pose - on back with legs bent."""
    scene = bpy.context.scene
    scene.frame_set(start_frame)

    bones = rig.pose.bones

    # Root on back
    if 'root' in bones:
        bones['root'].rotation_mode = 'XYZ'
        bones['root'].rotation_euler = Euler((rad(180), 0, 0))
        bones['root'].location = Vector((0, 0, 0.3))
        bones['root'].keyframe_insert('rotation_euler', frame=start_frame)
        bones['root'].keyframe_insert('location', frame=start_frame)

    # Spine slightly curved
    for spine_name in ['spine_fk', 'spine_fk.001', 'spine_fk.002']:
        if spine_name in bones:
            bones[spine_name].rotation_mode = 'XYZ'
            bones[spine_name].rotation_euler = Euler((rad(-10), 0, 0))
            bones[spine_name].keyframe_insert('rotation_euler', frame=start_frame)

    # Legs bent up
    for side in ['.L', '.R']:
        thigh = f'thigh_fk{side}'
        shin = f'shin_fk{side}'

        if thigh in bones:
            bones[thigh].rotation_mode = 'XYZ'
            bones[thigh].rotation_euler = Euler((rad(-60), 0, 0))
            bones[thigh].keyframe_insert('rotation_euler', frame=start_frame)

        if shin in bones:
            bones[shin].rotation_mode = 'XYZ'
            bones[shin].rotation_euler = Euler((rad(90), 0, 0))
            bones[shin].keyframe_insert('rotation_euler', frame=start_frame)

    # Head stays oriented
    if 'head' in bones:
        bones['head'].rotation_mode = 'XYZ'
        bones['head'].rotation_euler = Euler((rad(-180), 0, 0))
        bones['head'].keyframe_insert('rotation_euler', frame=start_frame)

    return start_frame + duration


def _pose_bridge(rig, start_frame, duration, direction):
    """Bridge position - hips raised, foot planted."""
    scene = bpy.context.scene
    scene.frame_set(start_frame)

    bones = rig.pose.bones

    # Root bridges up
    if 'root' in bones:
        bones['root'].rotation_mode = 'XYZ'
        bones['root'].rotation_euler = Euler((rad(160), 0, rad(15 * direction)))
        bones['root'].location = Vector((0, 0, 0.6))
        bones['root'].keyframe_insert('rotation_euler', frame=start_frame)
        bones['root'].keyframe_insert('location', frame=start_frame)

    plant_side = '.R' if direction > 0 else '.L'
    extend_side = '.L' if direction > 0 else '.R'

    # Planted leg
    if f'thigh_fk{plant_side}' in bones:
        bones[f'thigh_fk{plant_side}'].rotation_euler = Euler((rad(-80), 0, 0))
        bones[f'thigh_fk{plant_side}'].keyframe_insert('rotation_euler', frame=start_frame)

    if f'shin_fk{plant_side}' in bones:
        bones[f'shin_fk{plant_side}'].rotation_euler = Euler((rad(80), 0, 0))
        bones[f'shin_fk{plant_side}'].keyframe_insert('rotation_euler', frame=start_frame)

    # Extended leg
    if f'thigh_fk{extend_side}' in bones:
        bones[f'thigh_fk{extend_side}'].rotation_euler = Euler((rad(-30), 0, rad(-20 * direction)))
        bones[f'thigh_fk{extend_side}'].keyframe_insert('rotation_euler', frame=start_frame)

    if f'shin_fk{extend_side}' in bones:
        bones[f'shin_fk{extend_side}'].rotation_euler = Euler((rad(20), 0, 0))
        bones[f'shin_fk{extend_side}'].keyframe_insert('rotation_euler', frame=start_frame)

    # Head maintains orientation
    if 'head' in bones:
        bones['head'].rotation_euler = Euler((rad(-160), 0, rad(-15 * direction)))
        bones['head'].keyframe_insert('rotation_euler', frame=start_frame)

    return start_frame + duration


def _pose_escape(rig, start_frame, duration, direction):
    """Escape position - hips shot back, on side."""
    scene = bpy.context.scene
    scene.frame_set(start_frame)

    bones = rig.pose.bones

    # Root rotated to side, hips back
    if 'root' in bones:
        bones['root'].rotation_mode = 'XYZ'
        bones['root'].rotation_euler = Euler((rad(120), 0, rad(45 * direction)))
        bones['root'].location = Vector((-0.3 * direction, -0.5, 0.4))
        bones['root'].keyframe_insert('rotation_euler', frame=start_frame)
        bones['root'].keyframe_insert('location', frame=start_frame)

    # Spine twists
    for i, spine_name in enumerate(['spine_fk', 'spine_fk.001', 'spine_fk.002']):
        if spine_name in bones:
            twist = rad(-20 * direction) * (i + 1) / 3
            bones[spine_name].rotation_euler = Euler((rad(-15), twist, 0))
            bones[spine_name].keyframe_insert('rotation_euler', frame=start_frame)

    # Both legs extend
    for side in ['.L', '.R']:
        if f'thigh_fk{side}' in bones:
            bones[f'thigh_fk{side}'].rotation_euler = Euler((rad(-20), 0, rad(-15 * direction)))
            bones[f'thigh_fk{side}'].keyframe_insert('rotation_euler', frame=start_frame)

        if f'shin_fk{side}' in bones:
            bones[f'shin_fk{side}'].rotation_euler = Euler((rad(30), 0, 0))
            bones[f'shin_fk{side}'].keyframe_insert('rotation_euler', frame=start_frame)

    # Head looks toward escape direction
    if 'head' in bones:
        bones['head'].rotation_euler = Euler((rad(-120), rad(20 * direction), rad(-45 * direction)))
        bones['head'].keyframe_insert('rotation_euler', frame=start_frame)

    return start_frame + duration


def create_shrimp_animation(rig_name, repetitions=2, fps=24):
    """Create a full shrimping drill with multiple reps."""
    frame = 1

    for i in range(repetitions):
        direction = 'RIGHT' if i % 2 == 0 else 'LEFT'
        frame = shrimp_escape(rig_name, frame, fps, direction)

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frame

    print(f"Created shrimping drill: {repetitions} reps, {frame} total frames")
    return frame


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def run_mvp():
    """Main function to run the MVP demo."""
    print("\n" + "="*50)
    print("ANIMAL JIU JITSU - MVP")
    print("="*50 + "\n")

    # Step 1: Setup scene
    print("[1/3] Setting up scene...")
    setup_scene()

    # Step 2: Create fox
    print("[2/3] Creating fox character...")
    fox_rig = create_fox_primitive("FoxRig")

    # Step 3: Create animation
    print("[3/3] Creating shrimping animation...")
    end_frame = create_shrimp_animation("FoxRig", repetitions=2, fps=24)

    # Configure render output
    configure_eevee_render(
        resolution_x=1280,
        resolution_y=720,
        fps=24,
        samples=32
    )

    # Set output path
    bpy.context.scene.render.filepath = "//renders/test/shrimp_"

    print("\n" + "="*50)
    print("MVP SETUP COMPLETE!")
    print("="*50)
    print(f"\nAnimation: {end_frame} frames ({end_frame/24:.1f} seconds)")
    print("\nNext steps:")
    print("1. Press SPACE to play animation in viewport")
    print("2. Adjust poses in Pose Mode as needed")
    print("3. Render > Render Animation (Ctrl+F12) for output")
    print("="*50 + "\n")


# Run when executed
run_mvp()
