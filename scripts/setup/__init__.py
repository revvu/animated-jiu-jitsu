"""Scene setup utilities for Animal Jiu Jitsu project."""

from .scene_setup import (
    setup_scene,
    create_ground_plane,
    setup_lighting,
    setup_camera,
    configure_eevee_render,
)
from .materials import (
    create_fox_material,
    create_mat_material,
)

__all__ = [
    "setup_scene",
    "create_ground_plane",
    "setup_lighting",
    "setup_camera",
    "configure_eevee_render",
    "create_fox_material",
    "create_mat_material",
]
