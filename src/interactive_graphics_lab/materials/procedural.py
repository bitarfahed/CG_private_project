"""Procedural material definitions and shader support."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Any


class MaterialType(StrEnum):
    """Supported shader-generated material types."""

    SOLID = "solid"
    CHECKER = "checker"
    STRIPES = "stripes"
    GRADIENT = "gradient"
    MARBLE = "marble"
    WOOD = "wood"
    CLOUDS = "clouds"
    LAVA = "lava"


class MaterialShaderId(IntEnum):
    """Integer IDs mirrored in the procedural fragment shader."""

    SOLID = 0
    CHECKER = 1
    STRIPES = 2
    GRADIENT = 3
    MARBLE = 4
    WOOD = 5
    CLOUDS = 6
    LAVA = 7


@dataclass(frozen=True)
class ProceduralMaterial:
    """Configurable procedural material parameters."""

    material_type: MaterialType
    name: str
    base_color: tuple[float, float, float] = (0.9, 0.9, 0.9)
    secondary_color: tuple[float, float, float] = (0.1, 0.1, 0.1)
    scale: float = 8.0
    frequency: float = 4.0
    contrast: float = 1.0
    noise_strength: float = 0.5
    time: float = 0.0

    def __post_init__(self) -> None:
        _validate_color("base_color", self.base_color)
        _validate_color("secondary_color", self.secondary_color)
        _require_positive("scale", self.scale)
        _require_positive("frequency", self.frequency)
        if self.contrast < 0:
            raise ValueError("contrast must be non-negative")
        if self.noise_strength < 0:
            raise ValueError("noise_strength must be non-negative")

    @property
    def shader_id(self) -> MaterialShaderId:
        """Material ID used by the fragment shader."""
        return MaterialShaderId[self.material_type.name]

    def apply(self, program: Any) -> None:
        """Upload material parameters to a ModernGL program."""
        program["u_material_type"].value = int(self.shader_id)
        program["u_base_color"].value = self.base_color
        program["u_secondary_color"].value = self.secondary_color
        program["u_scale"].value = self.scale
        program["u_frequency"].value = self.frequency
        program["u_contrast"].value = self.contrast
        program["u_noise_strength"].value = self.noise_strength
        program["u_time"].value = self.time


def default_materials() -> dict[MaterialType, ProceduralMaterial]:
    """Return the default procedural material library."""
    return {
        MaterialType.SOLID: ProceduralMaterial(
            material_type=MaterialType.SOLID,
            name="Solid Color",
            base_color=(0.25, 0.58, 0.95),
        ),
        MaterialType.CHECKER: ProceduralMaterial(
            material_type=MaterialType.CHECKER,
            name="Checker",
            base_color=(0.95, 0.92, 0.82),
            secondary_color=(0.08, 0.10, 0.13),
            scale=10.0,
        ),
        MaterialType.STRIPES: ProceduralMaterial(
            material_type=MaterialType.STRIPES,
            name="Stripes",
            base_color=(0.12, 0.34, 0.90),
            secondary_color=(0.93, 0.98, 1.0),
            scale=14.0,
            contrast=1.2,
        ),
        MaterialType.GRADIENT: ProceduralMaterial(
            material_type=MaterialType.GRADIENT,
            name="Gradient",
            base_color=(0.12, 0.20, 0.55),
            secondary_color=(0.98, 0.48, 0.20),
        ),
        MaterialType.MARBLE: ProceduralMaterial(
            material_type=MaterialType.MARBLE,
            name="Marble",
            base_color=(0.88, 0.90, 0.86),
            secondary_color=(0.20, 0.25, 0.32),
            scale=5.5,
            frequency=7.0,
            contrast=1.1,
            noise_strength=0.7,
        ),
        MaterialType.WOOD: ProceduralMaterial(
            material_type=MaterialType.WOOD,
            name="Wood",
            base_color=(0.56, 0.30, 0.12),
            secondary_color=(0.95, 0.68, 0.32),
            scale=9.0,
            frequency=14.0,
            contrast=1.35,
            noise_strength=0.45,
        ),
        MaterialType.CLOUDS: ProceduralMaterial(
            material_type=MaterialType.CLOUDS,
            name="Noise / Clouds",
            base_color=(0.15, 0.32, 0.62),
            secondary_color=(0.92, 0.96, 1.0),
            scale=4.0,
            contrast=1.15,
            noise_strength=0.9,
        ),
        MaterialType.LAVA: ProceduralMaterial(
            material_type=MaterialType.LAVA,
            name="Lava / Energy",
            base_color=(1.0, 0.24, 0.02),
            secondary_color=(0.06, 0.02, 0.01),
            scale=6.0,
            frequency=9.0,
            contrast=1.55,
            noise_strength=0.8,
        ),
    }


class MaterialLibrary:
    """Small registry for procedural materials."""

    def __init__(self, materials: dict[MaterialType, ProceduralMaterial] | None = None) -> None:
        self._materials = materials or default_materials()

    def get(self, material_type: MaterialType | str) -> ProceduralMaterial:
        """Return a material by type."""
        return self._materials[MaterialType(material_type)]


MATERIAL_FRAGMENT_SHADER = """
#version 330

in vec3 v_position;
in vec3 v_normal;
in vec2 v_uv;

uniform int u_material_type;
uniform vec3 u_base_color;
uniform vec3 u_secondary_color;
uniform float u_scale;
uniform float u_frequency;
uniform float u_contrast;
uniform float u_noise_strength;
uniform float u_time;

out vec4 frag_color;

float hash(vec3 p) {
    p = fract(p * 0.3183099 + vec3(0.11, 0.17, 0.23));
    p += dot(p, p.yzx + 19.19);
    return fract((p.x + p.y) * p.z);
}

float value_noise(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);

    float n000 = hash(i + vec3(0.0, 0.0, 0.0));
    float n100 = hash(i + vec3(1.0, 0.0, 0.0));
    float n010 = hash(i + vec3(0.0, 1.0, 0.0));
    float n110 = hash(i + vec3(1.0, 1.0, 0.0));
    float n001 = hash(i + vec3(0.0, 0.0, 1.0));
    float n101 = hash(i + vec3(1.0, 0.0, 1.0));
    float n011 = hash(i + vec3(0.0, 1.0, 1.0));
    float n111 = hash(i + vec3(1.0, 1.0, 1.0));

    float nx00 = mix(n000, n100, f.x);
    float nx10 = mix(n010, n110, f.x);
    float nx01 = mix(n001, n101, f.x);
    float nx11 = mix(n011, n111, f.x);
    float nxy0 = mix(nx00, nx10, f.y);
    float nxy1 = mix(nx01, nx11, f.y);
    return mix(nxy0, nxy1, f.z);
}

float fbm(vec3 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int octave = 0; octave < 5; octave++) {
        value += amplitude * value_noise(p);
        p *= 2.03;
        amplitude *= 0.5;
    }
    return value;
}

vec3 apply_contrast(vec3 color) {
    return clamp((color - 0.5) * u_contrast + 0.5, 0.0, 1.0);
}

void main() {
    vec3 p = v_position;
    vec2 uv = v_uv;
    float n = fbm(p * u_scale + vec3(0.0, 0.0, u_time * 0.15));
    vec3 color = u_base_color;

    if (u_material_type == 1) {
        vec2 cells = floor(uv * u_scale);
        float checker = mod(cells.x + cells.y, 2.0);
        color = mix(u_base_color, u_secondary_color, checker);
    } else if (u_material_type == 2) {
        float stripe = smoothstep(0.42, 0.58, sin((uv.x + uv.y * 0.2) * u_scale) * 0.5 + 0.5);
        color = mix(u_base_color, u_secondary_color, stripe);
    } else if (u_material_type == 3) {
        color = mix(u_base_color, u_secondary_color, clamp(uv.y, 0.0, 1.0));
    } else if (u_material_type == 4) {
        float veins = sin((p.y + n * u_noise_strength) * u_frequency);
        float t = smoothstep(0.18, 0.92, veins * 0.5 + 0.5);
        color = mix(u_secondary_color, u_base_color, t);
    } else if (u_material_type == 5) {
        float rings = length(p.xz) * u_frequency + n * u_noise_strength * 3.0;
        float grain = sin(rings) * 0.5 + 0.5;
        color = mix(u_base_color, u_secondary_color, smoothstep(0.28, 0.78, grain));
    } else if (u_material_type == 6) {
        float cloud = smoothstep(0.22, 0.92, n * (1.0 + u_noise_strength));
        color = mix(u_base_color, u_secondary_color, cloud);
    } else if (u_material_type == 7) {
        float energy = sin((p.y + p.x * 0.55 + n * u_noise_strength) * u_frequency) * 0.5 + 0.5;
        float cracks = smoothstep(0.62, 0.92, energy);
        vec3 hot = mix(vec3(1.0, 0.85, 0.18), u_base_color, 0.45);
        color = mix(u_secondary_color, hot, cracks);
    }

    vec3 normal_tint = normalize(v_normal) * 0.08 + 0.92;
    frag_color = vec4(apply_contrast(color * normal_tint), 1.0);
}
"""


def _validate_color(name: str, color: tuple[float, float, float]) -> None:
    if len(color) != 3:
        raise ValueError(f"{name} must contain exactly three components")
    if any(component < 0 or component > 1 for component in color):
        raise ValueError(f"{name} components must be between 0 and 1")


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")
