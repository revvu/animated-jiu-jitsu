"""
Shrimping / Hip Escape animation for Animal Jiu Jitsu.

The shrimp (hip escape) is a fundamental BJJ movement used to create
space and escape from bottom positions. This script creates the
keyframe animation for a quadruped rig performing this drill.

Movement phases:
1. Start on back (guard position)
2. Plant foot, bridge hips up
3. Turn to side, shoot hips back
4. Return to guard position
5. Repeat on other side (optional)
"""

import bpy
from mathutils import Euler, Vector
import math

# Import core utilities - these work when run inside Blender
try:
    import sys
    import os
    # Add scripts folder to path if needed
    scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if scripts_dir not in sys.path:
        sys.path.append(scripts_dir)
    from core.rig_utils import rad, set_bone_rotation, set_bone_location
    from core.keyframe_utils import insert_keyframe, set_frame_range
except ImportError:
    # Fallback for standalone testing
    def rad(degrees): return math.radians(degrees)


# Default bone names for Rigify quadruped rig
# These may need adjustment based on actual rig configuration
RIGIFY_BONES = {
    'root': 'root',
    'spine': 'spine_fk',
    'spine_001': 'spine_fk.001',
    'spine_002': 'spine_fk.002',
    'spine_003': 'spine_fk.003',  # Upper back
    'hips': 'torso',
    'thigh_L': 'thigh_fk.L',
    'thigh_R': 'thigh_fk.R',
    'shin_L': 'shin_fk.L',
    'shin_R': 'shin_fk.R',
    'foot_L': 'foot_fk.L',
    'foot_R': 'foot_fk.R',
    'head': 'head',
    'tail': 'tail_fk',
}


def shrimp_escape(
    rig_name: str,
    start_frame: int = 1,
    fps: int = 24,
    direction: str = 'RIGHT'
) -> int:
    """
    Create a shrimping/hip escape animation on a quadruped rig.

    Args:
        rig_name: Name of the armature object
        start_frame: Starting frame for animation
        fps: Frames per second
        direction: 'RIGHT' or 'LEFT' - which direction to escape

    Returns:
        End frame of the animation
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None:
        print(f"Error: Rig '{rig_name}' not found")
        return start_frame

    # Ensure rig is selected and active
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)

    # Animation timing (in frames at 24fps)
    # Total duration: ~4 seconds for one shrimp
    phase_duration = int(fps * 0.8)  # ~0.8 seconds per phase

    frame = start_frame

    # Direction multiplier
    dir_mult = 1 if direction == 'RIGHT' else -1

    # Phase 1: Guard position (on back, legs bent)
    frame = _pose_guard(rig, frame, phase_duration)

    # Phase 2: Bridge (hips up, preparing to escape)
    frame = _pose_bridge(rig, frame, phase_duration, dir_mult)

    # Phase 3: Hip escape (rotate and shoot hips back)
    frame = _pose_escape(rig, frame, phase_duration, dir_mult)

    # Phase 4: Reset to guard
    frame = _pose_guard(rig, frame, phase_duration)

    print(f"Shrimp animation created: frames {start_frame} to {frame}")
    return frame


def _pose_guard(rig, start_frame: int, duration: int) -> int:
    """
    Set guard position pose - on back with legs bent.

    Returns the next frame after this phase.
    """
    scene = bpy.context.scene

    # Keyframe at start
    scene.frame_set(start_frame)

    bones = rig.pose.bones

    # Root on back (rotated 180 around X to be belly-up)
    if 'root' in bones:
        bones['root'].rotation_mode = 'XYZ'
        bones['root'].rotation_euler = Euler((rad(180), 0, 0))
        bones['root'].location = Vector((0, 0, 0.3))  # Slightly off ground
        bones['root'].keyframe_insert('rotation_euler', frame=start_frame)
        bones['root'].keyframe_insert('location', frame=start_frame)

    # Spine slightly curved
    for i, spine_name in enumerate(['spine_fk', 'spine_fk.001', 'spine_fk.002']):
        if spine_name in bones:
            bones[spine_name].rotation_mode = 'XYZ'
            bones[spine_name].rotation_euler = Euler((rad(-10), 0, 0))
            bones[spine_name].keyframe_insert('rotation_euler', frame=start_frame)

    # Legs bent up (guard position)
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

    # Head stays oriented forward
    if 'head' in bones:
        bones['head'].rotation_mode = 'XYZ'
        bones['head'].rotation_euler = Euler((rad(-180), 0, 0))  # Counter rotation
        bones['head'].keyframe_insert('rotation_euler', frame=start_frame)

    return start_frame + duration


def _pose_bridge(rig, start_frame: int, duration: int, direction: int) -> int:
    """
    Bridge position - hips raised, foot planted.

    Returns the next frame after this phase.
    """
    scene = bpy.context.scene
    scene.frame_set(start_frame)

    bones = rig.pose.bones

    # Root bridges up
    if 'root' in bones:
        bones['root'].rotation_mode = 'XYZ'
        bones['root'].rotation_euler = Euler((rad(160), 0, rad(15 * direction)))
        bones['root'].location = Vector((0, 0, 0.6))  # Higher off ground
        bones['root'].keyframe_insert('rotation_euler', frame=start_frame)
        bones['root'].keyframe_insert('location', frame=start_frame)

    # Plant foot on escape side, other leg extends slightly
    plant_side = '.R' if direction > 0 else '.L'
    extend_side = '.L' if direction > 0 else '.R'

    # Planted leg - foot flat, driving the bridge
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


def _pose_escape(rig, start_frame: int, duration: int, direction: int) -> int:
    """
    Escape position - hips shot back, on side.

    Returns the next frame after this phase.
    """
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

    # Both legs extend in escape
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


def create_shrimp_animation(
    rig_name: str,
    repetitions: int = 2,
    fps: int = 24
) -> int:
    """
    Create a full shrimping drill with multiple reps.

    Args:
        rig_name: Name of the armature
        repetitions: Number of shrimps to perform
        fps: Frames per second

    Returns:
        Total end frame
    """
    frame = 1

    for i in range(repetitions):
        # Alternate directions
        direction = 'RIGHT' if i % 2 == 0 else 'LEFT'
        frame = shrimp_escape(rig_name, frame, fps, direction)

    # Set frame range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frame

    print(f"Created shrimping drill: {repetitions} reps, {frame} total frames")
    return frame


# For testing in Blender
if __name__ == "__main__":
    # Assumes a rig named "FoxRig" exists in the scene
    create_shrimp_animation("FoxRig", repetitions=2)
