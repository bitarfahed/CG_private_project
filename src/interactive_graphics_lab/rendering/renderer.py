"""Renderer for the initial procedural geometry demo."""

from __future__ import annotations

from array import array
from math import cos, radians, sin, tan
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

    def render(self, aspect_ratio: float) -> None:
        """Render the current procedural mesh."""
        self.clear()
        model = _rotation_y(radians(-24.0))
        view = _translation(0.0, 0.0, -3.0)
        projection = _perspective(radians(42.0), aspect_ratio, 0.1, 100.0)
        self._write_matrix("u_model", model)
        self._write_matrix("u_mvp", _multiply_matrix(projection, _multiply_matrix(view, model)))
        self._material.apply(self._program)
        self._mesh.render()

    def _write_matrix(self, uniform_name: str, matrix: tuple[float, ...]) -> None:
        """Upload a 4x4 row-major matrix to GLSL as column-major bytes."""
        self._program[uniform_name].write(_matrix_bytes(matrix))


_VERTEX_SHADER = """
#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 u_model;
uniform mat4 u_mvp;

out vec3 v_normal;
out vec3 v_position;
out vec2 v_uv;

void main() {
    vec4 world_position = u_model * vec4(in_position, 1.0);
    gl_Position = u_mvp * vec4(in_position, 1.0);
    v_position = world_position.xyz;
    v_normal = normalize(mat3(u_model) * in_normal);
    v_uv = in_uv;
}
"""


def _identity() -> tuple[float, ...]:
    return (
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


def _translation(x: float, y: float, z: float) -> tuple[float, ...]:
    matrix = list(_identity())
    matrix[3] = x
    matrix[7] = y
    matrix[11] = z
    return tuple(matrix)


def _rotation_y(angle: float) -> tuple[float, ...]:
    c = cos(angle)
    s = sin(angle)
    return (
        c, 0.0, s, 0.0,
        0.0, 1.0, 0.0, 0.0,
        -s, 0.0, c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


def _perspective(fov_y: float, aspect_ratio: float, near: float, far: float) -> tuple[float, ...]:
    f = 1.0 / tan(fov_y / 2.0)
    depth = near - far
    return (
        f / aspect_ratio, 0.0, 0.0, 0.0,
        0.0, f, 0.0, 0.0,
        0.0, 0.0, (far + near) / depth, (2.0 * far * near) / depth,
        0.0, 0.0, -1.0, 0.0,
    )


def _multiply_matrix(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    result = [0.0] * 16
    for row in range(4):
        for column in range(4):
            result[row * 4 + column] = sum(left[row * 4 + k] * right[k * 4 + column] for k in range(4))
    return tuple(result)


def _matrix_bytes(row_major_matrix: tuple[float, ...]) -> bytes:
    column_major = [row_major_matrix[row * 4 + column] for column in range(4) for row in range(4)]
    return array("f", column_major).tobytes()
