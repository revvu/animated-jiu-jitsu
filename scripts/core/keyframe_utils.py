"""
Keyframe utilities for animation.

This module provides helper functions for inserting and managing
keyframes in Blender animations.
"""

import bpy


def insert_keyframe(
    rig_name: str,
    bone_name: str,
    frame: int,
    data_path: str = "rotation_euler"
) -> bool:
    """
    Insert a keyframe for a specific bone property.

    Args:
        rig_name: Name of the armature object
        bone_name: Name of the bone
        frame: Frame number to insert keyframe
        data_path: Property to keyframe (rotation_euler, location, scale)

    Returns:
        True if successful, False otherwise
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None or rig.type != 'ARMATURE':
        return False

    if bone_name not in rig.pose.bones:
        return False

    bone = rig.pose.bones[bone_name]

    # Set the current frame
    bpy.context.scene.frame_set(frame)

    # Insert the keyframe
    bone.keyframe_insert(data_path=data_path, frame=frame)
    return True


def insert_keyframes_for_bones(
    rig_name: str,
    bone_data: dict,
    frame: int,
    data_paths: list = None
) -> int:
    """
    Insert keyframes for multiple bones at once.

    Args:
        rig_name: Name of the armature object
        bone_data: Dict of {bone_name: {rotation, location, scale}}
        frame: Frame number to insert keyframes
        data_paths: List of data paths to keyframe (default: rotation_euler only)

    Returns:
        Number of successful keyframe insertions
    """
    if data_paths is None:
        data_paths = ["rotation_euler"]

    rig = bpy.data.objects.get(rig_name)
    if rig is None or rig.type != 'ARMATURE':
        return 0

    bpy.context.scene.frame_set(frame)
    count = 0

    for bone_name in bone_data:
        if bone_name not in rig.pose.bones:
            continue

        bone = rig.pose.bones[bone_name]

        for data_path in data_paths:
            try:
                bone.keyframe_insert(data_path=data_path, frame=frame)
                count += 1
            except Exception as e:
                print(f"Warning: Could not keyframe {bone_name}.{data_path}: {e}")

    return count


def set_interpolation(
    rig_name: str,
    interpolation: str = 'BEZIER'
) -> bool:
    """
    Set interpolation mode for all keyframes on a rig.

    Args:
        rig_name: Name of the armature object
        interpolation: Interpolation type (BEZIER, LINEAR, CONSTANT)

    Returns:
        True if successful, False otherwise
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None:
        return False

    if rig.animation_data is None or rig.animation_data.action is None:
        return False

    for fcurve in rig.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = interpolation

    return True


def clear_all_keyframes(rig_name: str) -> bool:
    """
    Remove all keyframes from a rig.

    Args:
        rig_name: Name of the armature object

    Returns:
        True if successful, False otherwise
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None:
        return False

    if rig.animation_data is not None:
        rig.animation_data_clear()

    return True


def set_frame_range(start: int, end: int, fps: int = 24):
    """
    Set the scene frame range and FPS.

    Args:
        start: Start frame
        end: End frame
        fps: Frames per second
    """
    scene = bpy.context.scene
    scene.frame_start = start
    scene.frame_end = end
    scene.render.fps = fps
    scene.frame_set(start)
