"""Renderer for the initial procedural geometry demo."""

from __future__ import annotations

from typing import Any

import moderngl

from interactive_graphics_lab.geometry import MeshGenerator, PrimitiveType
from interactive_graphics_lab.materials import MATERIAL_FRAGMENT_SHADER, MaterialLibrary, MaterialType
from interactive_graphics_lab.rendering.gpu_mesh import GpuMesh


class Renderer:
    """Small rendering facade for the current procedural mesh demo."""

    def __init__(self, context: Any) -> None:
        self._context = context
        self.clear_color = (0.08, 0.10, 0.13, 1.0)
        self._context.enable(moderngl.DEPTH_TEST)
        self._program = self._context.program(vertex_shader=_VERTEX_SHADER, fragment_shader=MATERIAL_FRAGMENT_SHADER)
        self._material = MaterialLibrary().get(MaterialType.MARBLE)
        self._mesh = GpuMesh(
            self._context,
            self._program,
            MeshGenerator.create(PrimitiveType.SPHERE),
        )

    def clear(self) -> None:
        """Clear the current frame to the configured background color."""
        self._context.clear(*self.clear_color)

    def render(self) -> None:
        """Render the current procedural mesh."""
        self.clear()
        self._material.apply(self._program)
        self._mesh.render()


_VERTEX_SHADER = """
#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

out vec3 v_normal;
out vec3 v_position;
out vec2 v_uv;

void main() {
    vec3 p = in_position;
    gl_Position = vec4(
        p.x * 0.78 + p.z * 0.22,
        p.y * 0.78 - p.z * 0.12,
        p.z * 0.10,
        1.0
    );
    v_position = in_position;
    v_normal = normalize(in_normal);
    v_uv = in_uv;
}
"""
