"""Small lighting data model for Phong shading."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


MAX_POINT_LIGHTS = 4


def _validate_vec3(name: str, value: tuple[float, float, float]) -> None:
    if len(value) != 3:
        raise ValueError(f"{name} must contain exactly three components")


def _validate_color(name: str, color: tuple[float, float, float]) -> None:
    _validate_vec3(name, color)
    if any(component < 0 or component > 1 for component in color):
        raise ValueError(f"{name} components must be between 0 and 1")


@dataclass(frozen=True)
class PointLight:
    """Configurable point light for the shader pipeline."""

    position: tuple[float, float, float]
    color: tuple[float, float, float]
    intensity: float = 1.0

    def __post_init__(self) -> None:
        _validate_vec3("position", self.position)
        _validate_color("color", self.color)
        if self.intensity < 0:
            raise ValueError("intensity must be non-negative")


@dataclass(frozen=True)
class LightingSettings:
    """Ambient and Phong material response settings."""

    ambient_color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    ambient_intensity: float = 0.22
    specular_strength: float = 0.55
    shininess: float = 48.0
    point_lights: tuple[PointLight, ...] = (
        PointLight(position=(-2.2, 2.2, 2.2), color=(1.0, 0.92, 0.78), intensity=1.15),
        PointLight(position=(2.4, 1.2, 1.2), color=(0.35, 0.58, 1.0), intensity=0.45),
    )

    def __post_init__(self) -> None:
        _validate_color("ambient_color", self.ambient_color)
        if self.ambient_intensity < 0:
            raise ValueError("ambient_intensity must be non-negative")
        if self.specular_strength < 0:
            raise ValueError("specular_strength must be non-negative")
        if self.shininess <= 0:
            raise ValueError("shininess must be positive")
        if len(self.point_lights) > MAX_POINT_LIGHTS:
            raise ValueError(f"at most {MAX_POINT_LIGHTS} point lights are supported")

    def apply(self, program: Any) -> None:
        """Upload lighting uniforms to a ModernGL program."""
        program["u_ambient_color"].value = self.ambient_color
        program["u_ambient_intensity"].value = self.ambient_intensity
        program["u_specular_strength"].value = self.specular_strength
        program["u_shininess"].value = self.shininess
        program["u_point_light_count"].value = len(self.point_lights)

        for index in range(MAX_POINT_LIGHTS):
            light = self.point_lights[index] if index < len(self.point_lights) else _disabled_light()
            prefix = f"u_point_lights[{index}]"
            program[f"{prefix}.position"].value = light.position
            program[f"{prefix}.color"].value = light.color
            program[f"{prefix}.intensity"].value = light.intensity


def _disabled_light() -> PointLight:
    return PointLight(position=(0.0, 0.0, 0.0), color=(0.0, 0.0, 0.0), intensity=0.0)
