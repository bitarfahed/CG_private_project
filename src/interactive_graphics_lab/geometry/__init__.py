"""Procedural geometry package."""

from interactive_graphics_lab.geometry.generators import (
    MeshGenerator,
    PrimitiveType,
    generate_cone,
    generate_cube,
    generate_cylinder,
    generate_plane,
    generate_sphere,
    generate_torus,
)
from interactive_graphics_lab.geometry.mesh import Mesh

__all__ = [
    "Mesh",
    "MeshGenerator",
    "PrimitiveType",
    "generate_cone",
    "generate_cube",
    "generate_cylinder",
    "generate_plane",
    "generate_sphere",
    "generate_torus",
]
