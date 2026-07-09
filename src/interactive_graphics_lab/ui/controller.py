"""ImGui controls for the existing graphics modules."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import imgui
from imgui.integrations.pyglet import create_renderer

from interactive_graphics_lab.animation import AnimationSystem
from interactive_graphics_lab.core import Scene
from interactive_graphics_lab.geometry import MeshGenerator, PrimitiveType
from interactive_graphics_lab.lighting import PointLight
from interactive_graphics_lab.materials import MaterialLibrary, MaterialType
from interactive_graphics_lab.postprocessing import PostProcessEffect
from interactive_graphics_lab.rendering.renderer import Renderer


class GuiController:
    """Small ImGui panel that edits scene and renderer state."""

    def __init__(self, window: Any, scene: Scene, renderer: Renderer, animation: AnimationSystem) -> None:
        imgui.create_context()
        self._renderer_impl = create_renderer(window)
        self._scene = scene
        self._renderer = renderer
        self._animation = animation
        self._materials = MaterialLibrary()

    def render(self) -> None:
        """Render the GUI overlay for the current frame."""
        self._renderer_impl.process_inputs()
        imgui.new_frame()
        self._draw_panel()
        imgui.render()
        self._renderer_impl.render(imgui.get_draw_data())

    def release(self) -> None:
        """Release ImGui renderer resources."""
        self._renderer_impl.shutdown()

    def _draw_panel(self) -> None:
        imgui.set_next_window_position(12, 12, condition=imgui.ONCE)
        imgui.set_next_window_size(330, 430, condition=imgui.ONCE)
        imgui.begin("Interactive Graphics Lab", True)
        self._draw_geometry_controls()
        imgui.separator()
        self._draw_material_controls()
        imgui.separator()
        self._draw_lighting_controls()
        imgui.separator()
        self._draw_animation_controls()
        imgui.separator()
        self._draw_postprocessing_controls()
        imgui.end()

    def _draw_geometry_controls(self) -> None:
        imgui.text("Geometry")
        primitives = [
            PrimitiveType.SPHERE,
            PrimitiveType.TORUS,
            PrimitiveType.CONE,
            PrimitiveType.CYLINDER,
            PrimitiveType.PLANE,
            PrimitiveType.CUBE,
        ]
        labels = [_title_label(primitive.value) for primitive in primitives]
        current_index = primitives.index(self._scene.active_primitive)
        changed, selected_index = imgui.combo("Primitive", current_index, labels)
        if changed:
            primitive = primitives[selected_index]
            self._scene.active_primitive = primitive
            self._scene.mesh = MeshGenerator.create(primitive)

    def _draw_material_controls(self) -> None:
        imgui.text("Material")
        materials = list(MaterialType)
        labels = [self._materials.get(material).name for material in materials]
        current_index = materials.index(self._scene.active_material)
        changed, selected_index = imgui.combo("Material", current_index, labels)
        if changed:
            material_type = materials[selected_index]
            current_time = self._scene.material.time
            self._scene.active_material = material_type
            self._scene.material = replace(self._materials.get(material_type), time=current_time)

    def _draw_lighting_controls(self) -> None:
        imgui.text("Lighting")
        lights = self._scene.lighting.point_lights
        if not lights:
            return

        light_index = 1 if len(lights) > 1 else 0
        light = lights[light_index]
        imgui.text(f"Editing Light {light_index + 1}")
        changed_color, color = imgui.color_edit3("Light Color", *light.color)
        changed_x, x = imgui.slider_float("Light X", light.position[0], -4.0, 4.0)
        changed_y, y = imgui.slider_float("Light Y", light.position[1], -1.0, 4.0)
        changed_z, z = imgui.slider_float("Light Z", light.position[2], -4.0, 4.0)
        changed_intensity, intensity = imgui.slider_float("Intensity", light.intensity, 0.0, 3.0)

        if changed_color or changed_x or changed_y or changed_z or changed_intensity:
            updated = PointLight(
                position=(x, y, z),
                color=tuple(color),
                intensity=intensity,
            )
            updated_lights = list(lights)
            updated_lights[light_index] = updated
            self._scene.lighting = replace(
                self._scene.lighting,
                point_lights=tuple(updated_lights),
            )

    def _draw_animation_controls(self) -> None:
        imgui.text("Animation")
        changed, enabled = imgui.checkbox("Animation On", self._animation.enabled)
        if changed:
            self._animation.enabled = enabled
        changed_speed, speed = imgui.slider_float("Rotation Speed", self._animation.rotation_speed_degrees, 0.0, 90.0)
        if changed_speed:
            self._animation.rotation_speed_degrees = speed

    def _draw_postprocessing_controls(self) -> None:
        imgui.text("Post Processing")
        effects = list(PostProcessEffect)
        labels = [_title_label(effect.value) for effect in effects]
        current_index = effects.index(self._renderer.post_process_effect)
        changed, selected_index = imgui.combo("Effect", current_index, labels)
        if changed:
            self._renderer.set_post_process_effect(effects[selected_index])


def _title_label(value: str) -> str:
    return value.replace("_", " ").replace("/", " / ").title()
