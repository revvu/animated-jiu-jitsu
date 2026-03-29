"""
Rig utilities for manipulating armature bones.

This module provides helper functions for working with Blender armatures
and pose bones in the Animal Jiu Jitsu project.
"""

import bpy
from mathutils import Euler, Vector
import math


def get_pose_bone(rig_name: str, bone_name: str):
    """
    Get a pose bone from a rig by name.

    Args:
        rig_name: Name of the armature object
        bone_name: Name of the bone to retrieve

    Returns:
        PoseBone or None if not found
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None or rig.type != 'ARMATURE':
        print(f"Warning: Rig '{rig_name}' not found or not an armature")
        return None

    if bone_name not in rig.pose.bones:
        print(f"Warning: Bone '{bone_name}' not found in rig '{rig_name}'")
        return None

    return rig.pose.bones[bone_name]


def set_bone_rotation(
    rig_name: str,
    bone_name: str,
    rotation: tuple,
    mode: str = 'XYZ'
) -> bool:
    """
    Set the rotation of a pose bone using Euler angles.

    Args:
        rig_name: Name of the armature object
        bone_name: Name of the bone to rotate
        rotation: Tuple of (x, y, z) rotation in radians
        mode: Euler rotation order (default 'XYZ')

    Returns:
        True if successful, False otherwise
    """
    bone = get_pose_bone(rig_name, bone_name)
    if bone is None:
        return False

    bone.rotation_mode = mode
    bone.rotation_euler = Euler(rotation, mode)
    return True


def set_bone_location(
    rig_name: str,
    bone_name: str,
    location: tuple
) -> bool:
    """
    Set the location offset of a pose bone.

    Args:
        rig_name: Name of the armature object
        bone_name: Name of the bone to move
        location: Tuple of (x, y, z) location offset

    Returns:
        True if successful, False otherwise
    """
    bone = get_pose_bone(rig_name, bone_name)
    if bone is None:
        return False

    bone.location = Vector(location)
    return True


def reset_pose(rig_name: str) -> bool:
    """
    Reset all pose bones to their rest position.

    Args:
        rig_name: Name of the armature object

    Returns:
        True if successful, False otherwise
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None or rig.type != 'ARMATURE':
        print(f"Warning: Rig '{rig_name}' not found or not an armature")
        return False

    for bone in rig.pose.bones:
        bone.location = Vector((0, 0, 0))
        bone.rotation_euler = Euler((0, 0, 0))
        bone.rotation_quaternion = (1, 0, 0, 0)
        bone.scale = Vector((1, 1, 1))

    return True


def get_bone_names(rig_name: str) -> list:
    """
    Get all bone names from a rig.

    Args:
        rig_name: Name of the armature object

    Returns:
        List of bone names, or empty list if rig not found
    """
    rig = bpy.data.objects.get(rig_name)
    if rig is None or rig.type != 'ARMATURE':
        return []

    return [bone.name for bone in rig.pose.bones]


def rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.radians(degrees)
