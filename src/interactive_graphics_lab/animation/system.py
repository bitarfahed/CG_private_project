"""Small frame-rate independent animation system."""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import cos, sin

from interactive_graphics_lab.core import Scene
from interactive_graphics_lab.lighting import PointLight


@dataclass
class AnimationSystem:
    """Updates scene properties over elapsed time."""

    enabled: bool = True
    elapsed_time: float = 0.0
    rotation_speed_degrees: float = 28.0
    light_orbit_speed: float = 0.75
    light_orbit_radius: float = 2.4

    def update(self, scene: Scene, delta_time: float) -> None:
        """Update the scene using elapsed seconds, not frame count."""
        if not self.enabled:
            return

        stable_delta = max(0.0, delta_time)
        self.elapsed_time += stable_delta

        scene.transform.rotation_y_degrees += self.rotation_speed_degrees * stable_delta
        scene.material = replace(scene.material, time=self.elapsed_time)
        scene.lighting = replace(scene.lighting, point_lights=self._animated_point_lights(scene))

    def _animated_point_lights(self, scene: Scene) -> tuple[PointLight, ...]:
        lights = scene.lighting.point_lights
        if not lights:
            return lights

        angle = self.elapsed_time * self.light_orbit_speed
        primary = lights[0]
        animated_primary = replace(
            primary,
            position=(
                cos(angle) * self.light_orbit_radius,
                1.8 + sin(angle * 0.7) * 0.35,
                sin(angle) * self.light_orbit_radius,
            ),
        )

        if len(lights) == 1:
            return (animated_primary,)

        secondary = lights[1]
        animated_secondary = replace(
            secondary,
            position=(
                cos(angle + 2.6) * 2.1,
                1.1,
                sin(angle + 2.6) * 1.8,
            ),
        )
        return (animated_primary, animated_secondary, *lights[2:])
