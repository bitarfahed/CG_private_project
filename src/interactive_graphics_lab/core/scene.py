"""Minimal scene data for the current rendering pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin

from interactive_graphics_lab.geometry import Mesh, MeshGenerator, PrimitiveType
from interactive_graphics_lab.lighting import LightingSettings
from interactive_graphics_lab.materials import MaterialLibrary, MaterialType, ProceduralMaterial


@dataclass
class Transform:
    """Object transform values used by the renderer."""

    rotation_y_degrees: float = -24.0


@dataclass
class Camera:
    """Simple orbit camera centered on the scene origin."""

    target: tuple[float, float, float] = (0.0, 0.0, 0.0)
    yaw_degrees: float = 0.0
    pitch_degrees: float = 0.0
    distance: float = 2.5
    vertical_size: float = 2.4
    min_distance: float = 1.25
    max_distance: float = 6.0
    min_vertical_size: float = 1.2
    max_vertical_size: float = 4.8
    near: float = 0.1
    far: float = 10.0

    @property
    def position(self) -> tuple[float, float, float]:
        """Return the camera eye position derived from orbit angles."""
        yaw = radians(self.yaw_degrees)
        pitch = radians(self.pitch_degrees)
        cos_pitch = cos(pitch)
        return (
            self.target[0] + self.distance * sin(yaw) * cos_pitch,
            self.target[1] + self.distance * sin(pitch),
            self.target[2] + self.distance * cos(yaw) * cos_pitch,
        )

    def orbit(self, yaw_delta_degrees: float, pitch_delta_degrees: float) -> None:
        """Orbit around the fixed target."""
        self.yaw_degrees = (self.yaw_degrees + yaw_delta_degrees) % 360.0
        self.pitch_degrees = _clamp(self.pitch_degrees + pitch_delta_degrees, -75.0, 75.0)

    def zoom(self, steps: float) -> None:
        """Zoom toward or away from the target while keeping safe bounds."""
        distance_factor = 1.0 - steps * 0.08
        size_factor = 1.0 - steps * 0.08
        self.distance = _clamp(self.distance * distance_factor, self.min_distance, self.max_distance)
        self.vertical_size = _clamp(self.vertical_size * size_factor, self.min_vertical_size, self.max_vertical_size)

    def reset(self) -> None:
        """Restore the default camera view."""
        self.yaw_degrees = 0.0
        self.pitch_degrees = 0.0
        self.distance = 2.5
        self.vertical_size = 2.4


@dataclass
class Scene:
    """Single-object scene used by the current application."""

    mesh: Mesh
    material: ProceduralMaterial
    lighting: LightingSettings
    transform: Transform
    camera: Camera
    active_primitive: PrimitiveType
    active_material: MaterialType

    @property
    def rotation_y_radians(self) -> float:
        """Return the object Y rotation in radians."""
        return radians(self.transform.rotation_y_degrees)


def create_default_scene() -> Scene:
    """Create the polished default procedural scene."""
    active_primitive = PrimitiveType.SPHERE
    active_material = MaterialType.MARBLE
    return Scene(
        mesh=MeshGenerator.create(active_primitive),
        material=MaterialLibrary().get(active_material),
        lighting=LightingSettings(),
        transform=Transform(),
        camera=Camera(),
        active_primitive=active_primitive,
        active_material=active_material,
    )


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return min(max(value, minimum), maximum)
