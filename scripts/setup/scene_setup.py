"""
Scene setup for Animal Jiu Jitsu project.

This module creates the basic scene elements: ground plane, lighting,
camera, and render settings for Eevee.
"""

import bpy
import math


def setup_scene():
    """
    Full scene setup - creates ground, lighting, camera, and configures render.
    Call this once to initialize the scene.
    """
    # Clear default objects
    clear_default_scene()

    # Create scene elements
    create_ground_plane()
    setup_lighting()
    setup_camera()
    configure_eevee_render()

    print("Scene setup complete!")


def clear_default_scene():
    """Remove default cube, light, and camera if they exist."""
    default_objects = ['Cube', 'Light', 'Camera']
    for name in default_objects:
        if name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)


def create_ground_plane(
    size: float = 10.0,
    name: str = "Mat"
) -> bpy.types.Object:
    """
    Create a ground plane (jiu jitsu mat).

    Args:
        size: Size of the plane
        name: Name for the object

    Returns:
        The created plane object
    """
    bpy.ops.mesh.primitive_plane_add(
        size=size,
        location=(0, 0, 0)
    )
    plane = bpy.context.active_object
    plane.name = name

    # Import material function
    from .materials import create_mat_material
    mat = create_mat_material()
    plane.data.materials.append(mat)

    return plane


def setup_lighting():
    """
    Create 3-point lighting setup for the scene.
    - Key light: Main light from upper front-right
    - Fill light: Softer light from front-left
    - Rim light: Back light for edge definition
    """
    # Key light (main)
    bpy.ops.object.light_add(
        type='AREA',
        location=(4, -3, 5)
    )
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 500
    key_light.data.size = 3
    key_light.data.color = (1.0, 0.95, 0.9)  # Warm white

    # Point at origin
    direction = key_light.location.normalized()
    key_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Fill light (softer)
    bpy.ops.object.light_add(
        type='AREA',
        location=(-3, -2, 3)
    )
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 200
    fill_light.data.size = 4
    fill_light.data.color = (0.9, 0.95, 1.0)  # Cool white

    direction = fill_light.location.normalized()
    fill_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Rim light (back)
    bpy.ops.object.light_add(
        type='AREA',
        location=(0, 4, 3)
    )
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 300
    rim_light.data.size = 2

    direction = rim_light.location.normalized()
    rim_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def setup_camera(
    location: tuple = (5, -5, 3),
    target: tuple = (0, 0, 0.5)
) -> bpy.types.Object:
    """
    Create and position the camera for a good view of the action.

    Args:
        location: Camera position (x, y, z)
        target: Point the camera looks at

    Returns:
        The created camera object
    """
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


def configure_eevee_render(
    resolution_x: int = 1280,
    resolution_y: int = 720,
    fps: int = 24,
    samples: int = 64
):
    """
    Configure Eevee render settings optimized for CPU preview.

    Args:
        resolution_x: Horizontal resolution
        resolution_y: Vertical resolution
        fps: Frames per second
        samples: Render samples (lower = faster)
    """
    scene = bpy.context.scene

    # Set render engine
    scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Blender 4+ uses EEVEE_NEXT

    # Resolution
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = 100

    # Frame rate
    scene.render.fps = fps

    # Eevee settings
    eevee = scene.eevee
    eevee.taa_render_samples = samples
    eevee.taa_samples = 16  # Viewport samples

    # Output settings
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

    # Animation range (default 10 seconds)
    scene.frame_start = 1
    scene.frame_end = fps * 10  # 10 seconds

    # Background color
    scene.world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
    scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.15, 0.18, 0.22, 1.0)  # Dark blue-gray

    print(f"Render configured: {resolution_x}x{resolution_y} @ {fps}fps, {samples} samples")
