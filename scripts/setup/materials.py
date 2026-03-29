"""
Materials for Animal Jiu Jitsu project.

Simple cartoon-style materials using Principled BSDF.
"""

import bpy


def create_fox_material(
    name: str = "Fox_Body",
    color: tuple = (0.9, 0.4, 0.1, 1.0),  # Orange
    roughness: float = 0.8
) -> bpy.types.Material:
    """
    Create a cartoon fox material.

    Args:
        name: Material name
        color: RGBA color tuple
        roughness: Surface roughness (higher = more matte)

    Returns:
        The created material
    """
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


def create_fox_white_material(
    name: str = "Fox_White",
    color: tuple = (0.95, 0.92, 0.85, 1.0)  # Cream white
) -> bpy.types.Material:
    """Create material for fox belly/chest (cream white)."""
    return create_fox_material(name=name, color=color)


def create_fox_dark_material(
    name: str = "Fox_Dark",
    color: tuple = (0.15, 0.08, 0.02, 1.0)  # Dark brown
) -> bpy.types.Material:
    """Create material for fox paws/ear tips (dark brown)."""
    return create_fox_material(name=name, color=color)


def create_fox_nose_material(
    name: str = "Fox_Nose",
    color: tuple = (0.02, 0.02, 0.02, 1.0)  # Near black
) -> bpy.types.Material:
    """Create material for fox nose (black, slightly shiny)."""
    return create_fox_material(name=name, color=color, roughness=0.3)


def create_mat_material(
    name: str = "BJJ_Mat",
    color: tuple = (0.1, 0.3, 0.6, 1.0)  # Blue mat
) -> bpy.types.Material:
    """
    Create a jiu jitsu mat material.

    Args:
        name: Material name
        color: RGBA color tuple (blue by default)

    Returns:
        The created material
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    nodes.clear()

    # Texture coordinate
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    # Mapping for scaling
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (4, 4, 1)

    # Checker texture for subtle mat pattern
    checker = nodes.new('ShaderNodeTexChecker')
    checker.location = (-200, 100)
    checker.inputs['Scale'].default_value = 20

    # Mix the pattern subtly with base color
    mix = nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.location = (0, 100)
    mix.inputs['Factor'].default_value = 0.05  # Very subtle pattern

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.9  # Matte rubber look

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)

    # Links
    links = mat.node_tree.links
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], mix.inputs['A'])
    links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat


def get_all_fox_materials() -> dict:
    """
    Create and return all fox materials.

    Returns:
        Dict with material names as keys
    """
    return {
        'body': create_fox_material(),
        'white': create_fox_white_material(),
        'dark': create_fox_dark_material(),
        'nose': create_fox_nose_material(),
    }
