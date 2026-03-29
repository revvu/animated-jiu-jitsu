"""
Animal Jiu Jitsu - Main Entry Point

This script is the main entry point for the Animal Jiu Jitsu project.
Run this in Blender's Text Editor (Alt+P) to set up the scene and
create the fox shrimping animation.

Usage:
1. Open Blender
2. Go to Scripting workspace
3. Open this file in the Text Editor
4. Press Alt+P or click "Run Script"
"""

import bpy
import sys
import os

# ============================================================
# PATH SETUP - Required for Blender's Text Editor
# ============================================================
# When running from Blender's Text Editor, we need to manually
# add the scripts directory to Python's path.

def get_script_directory():
    """Get the directory containing this script."""
    # Method 1: Try __file__ (works when run as external script)
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        pass

    # Method 2: Get from Blender's text block filepath
    for text in bpy.data.texts:
        if text.filepath and 'main.py' in text.filepath:
            return os.path.dirname(os.path.abspath(text.filepath))

    # Method 3: Fallback - assume standard project structure
    # Look for common locations
    possible_paths = [
        r"C:\Users\Owner\Desktop\animated-jiu-jitsu\scripts",
        os.path.expanduser("~/Desktop/animated-jiu-jitsu/scripts"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise RuntimeError(
        "Could not find scripts directory. "
        "Please open main.py from File > Open in Blender's Text Editor "
        "(not copy-pasted) so the filepath is preserved."
    )

# Add scripts directory to Python path
SCRIPT_DIR = get_script_directory()
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

print(f"Scripts directory: {SCRIPT_DIR}")

# Import project modules
from setup.scene_setup import setup_scene, configure_eevee_render
from setup.materials import get_all_fox_materials
from moves.shrimp import create_shrimp_animation


def create_fox_primitive(name: str = "FoxRig") -> bpy.types.Object:
    """
    Create a simple fox from primitives with a basic armature.

    This creates a placeholder fox using basic shapes that can be
    animated immediately. For the MVP, this demonstrates the concept
    before creating more detailed geometry.

    Returns:
        The armature object
    """
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

    # Tail (tapered cylinder-ish)
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

    for x, y, z, name in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.04,
            depth=0.4,
            location=(x, y, z)
        )
        leg = bpy.context.active_object
        leg.name = f"Fox_Leg_{name}"
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


def run_mvp():
    """
    Main function to run the MVP demo.

    Creates:
    - Scene setup (lighting, camera, ground)
    - Fox character with simple rig
    - Shrimping animation (2 reps)
    """
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
        samples=32  # Lower samples for faster preview
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
if __name__ == "__main__":
    run_mvp()
