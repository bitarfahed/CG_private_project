"""ImGui controls for the existing graphics modules."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import imgui
from pyglet.window import key, mouse
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
        self._window = window
        self._renderer_impl = create_renderer(window, attach_callbacks=False)
        self._renderer_impl._window = window
        self._scene = scene
        self._renderer = renderer
        self._animation = animation
        self._materials = MaterialLibrary()
        self._released = False
        self._panel_position = (12.0, 12.0)
        self._panel_size = (330.0, 430.0)
        self._attach_callbacks()

    def render(self) -> None:
        """Render the GUI overlay for the current frame."""
        if self._released:
            return
        self._sync_display_metrics()
        self._renderer_impl.process_inputs()
        imgui.new_frame()
        self._draw_panel()
        imgui.render()
        self._renderer_impl.render(imgui.get_draw_data())

    def release(self) -> None:
        """Release ImGui renderer resources."""
        if self._released:
            return
        self._renderer_impl.shutdown()
        self._released = True

    def _attach_callbacks(self) -> None:
        self._window.push_handlers(
            on_mouse_motion=self._on_mouse_motion,
            on_mouse_drag=self._on_mouse_drag,
            on_mouse_press=self._on_mouse_press,
            on_mouse_release=self._on_mouse_release,
            on_mouse_scroll=self._on_mouse_scroll,
            on_key_press=self._on_key_press,
            on_key_release=self._on_key_release,
            on_text=self._on_text,
            on_resize=self._on_resize,
        )

    def _sync_display_metrics(self) -> None:
        io = imgui.get_io()
        width, height = self._window.get_size()
        framebuffer_width, framebuffer_height = self._window.get_framebuffer_size()
        width = max(1, int(width))
        height = max(1, int(height))
        io.display_size = (float(width), float(height))
        io.display_fb_scale = (
            float(framebuffer_width) / float(width),
            float(framebuffer_height) / float(height),
        )

    def _set_mouse_position(self, x: float, y: float) -> None:
        self._sync_display_metrics()
        io = imgui.get_io()
        io.mouse_pos = (float(x), float(io.display_size.y - y))

    def _on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self._set_mouse_position(x, y)

    def _on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, modifiers: int) -> None:
        self._set_mouse_position(x, y)
        self._set_mouse_button(button, True)
        if button == mouse.RIGHT and not imgui.get_io().want_capture_mouse:
            self._scene.camera.orbit(-dx * 0.35, dy * 0.35)

    def _on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        self._set_mouse_position(x, y)
        self._set_mouse_button(button, True)

    def _on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        self._set_mouse_position(x, y)
        self._set_mouse_button(button, False)

    def _on_mouse_scroll(self, x: float, y: float, scroll_x: float, scroll_y: float) -> None:
        self._set_mouse_position(x, y)
        imgui.get_io().mouse_wheel = scroll_y
        if not imgui.get_io().want_capture_mouse:
            self._scene.camera.zoom(scroll_y)

    def _on_key_press(self, symbol: int, modifiers: int) -> None:
        self._renderer_impl.on_key_press(symbol, modifiers)
        if symbol == key.R and not imgui.get_io().want_capture_keyboard:
            self._scene.camera.reset()

    def _on_key_release(self, symbol: int, modifiers: int) -> None:
        self._renderer_impl.on_key_release(symbol, modifiers)

    def _on_text(self, text: str) -> None:
        self._renderer_impl.on_text(text)

    def _on_resize(self, width: int, height: int) -> None:
        self._sync_display_metrics()

    def _set_mouse_button(self, button: int, pressed: bool) -> None:
        io = imgui.get_io()
        if button == mouse.LEFT:
            io.mouse_down[0] = pressed
        elif button == mouse.MIDDLE:
            io.mouse_down[1] = pressed
        elif button == mouse.RIGHT:
            io.mouse_down[2] = pressed

    def _draw_panel(self) -> None:
        self._panel_position = _clamp_panel_position(self._panel_position, self._panel_size)
        imgui.set_next_window_position(*self._panel_position, condition=imgui.ALWAYS)
        imgui.set_next_window_size(330, 430, condition=imgui.ONCE)
        imgui.begin("Interactive Graphics Lab", True)
        self._draw_geometry_controls()
        imgui.spacing()
        imgui.separator()
        self._draw_material_controls()
        imgui.spacing()
        imgui.separator()
        self._draw_lighting_controls()
        imgui.spacing()
        imgui.separator()
        self._draw_animation_controls()
        imgui.spacing()
        imgui.separator()
        self._draw_postprocessing_controls()
        self._panel_position = _vec2_to_tuple(imgui.get_window_position())
        self._panel_size = _vec2_to_tuple(imgui.get_window_size())
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


def _clamp_panel_position(position: tuple[float, float], size: tuple[float, float]) -> tuple[float, float]:
    io = imgui.get_io()
    margin = 8.0
    max_x = max(margin, float(io.display_size.x) - size[0] - margin)
    max_y = max(margin, float(io.display_size.y) - size[1] - margin)
    x = min(max(position[0], margin), max_x)
    y = min(max(position[1], margin), max_y)
    return (x, y)


def _vec2_to_tuple(value: Any) -> tuple[float, float]:
    return (float(value.x), float(value.y))
