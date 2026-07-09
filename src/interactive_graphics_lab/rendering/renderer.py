"""Renderer for the initial procedural geometry demo."""

from __future__ import annotations

from typing import Any

import moderngl

from interactive_graphics_lab.geometry import MeshGenerator, PrimitiveType
from interactive_graphics_lab.rendering.gpu_mesh import GpuMesh


class Renderer:
    """Small rendering facade for the current procedural mesh demo."""

    def __init__(self, context: Any) -> None:
        self._context = context
        self.clear_color = (0.08, 0.10, 0.13, 1.0)
        self._context.enable(moderngl.DEPTH_TEST)
        self._program = self._context.program(vertex_shader=_VERTEX_SHADER, fragment_shader=_FRAGMENT_SHADER)
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
        self._mesh.render()


_VERTEX_SHADER = """
#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

out vec3 v_normal;
out vec2 v_uv;

void main() {
    vec3 p = in_position;
    gl_Position = vec4(
        p.x * 0.78 + p.z * 0.22,
        p.y * 0.78 - p.z * 0.12,
        p.z * 0.10,
        1.0
    );
    v_normal = normalize(in_normal);
    v_uv = in_uv;
}
"""

_FRAGMENT_SHADER = """
#version 330

in vec3 v_normal;
in vec2 v_uv;

out vec4 frag_color;

void main() {
    vec3 normal_color = v_normal * 0.5 + 0.5;
    frag_color = vec4(mix(normal_color, vec3(v_uv, 0.35), 0.18), 1.0);
}
"""
