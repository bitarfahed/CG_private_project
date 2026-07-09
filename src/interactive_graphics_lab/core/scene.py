"""Minimal scene data for the current rendering pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from math import radians

from interactive_graphics_lab.geometry import Mesh, MeshGenerator, PrimitiveType
from interactive_graphics_lab.lighting import LightingSettings
from interactive_graphics_lab.materials import MaterialLibrary, MaterialType, ProceduralMaterial


@dataclass(frozen=True)
class Transform:
    """Object transform values used by the renderer."""

    rotation_y_degrees: float = -24.0


@dataclass(frozen=True)
class Camera:
    """Fixed camera values for the default scene."""

    position: tuple[float, float, float] = (0.0, 0.0, 2.5)
    vertical_size: float = 2.4
    near: float = 0.1
    far: float = 10.0


@dataclass(frozen=True)
class Scene:
    """Single-object scene used by the current application."""

    mesh: Mesh
    material: ProceduralMaterial
    lighting: LightingSettings
    transform: Transform
    camera: Camera

    @property
    def rotation_y_radians(self) -> float:
        """Return the object Y rotation in radians."""
        return radians(self.transform.rotation_y_degrees)


def create_default_scene() -> Scene:
    """Create the polished default procedural scene."""
    return Scene(
        mesh=MeshGenerator.create(PrimitiveType.SPHERE),
        material=MaterialLibrary().get(MaterialType.MARBLE),
        lighting=LightingSettings(),
        transform=Transform(),
        camera=Camera(),
    )
