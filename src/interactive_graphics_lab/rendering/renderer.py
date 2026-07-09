"""Renderer for the initial procedural geometry demo."""

from __future__ import annotations

from array import array
from math import cos, radians, sin
from typing import Any

import moderngl

from interactive_graphics_lab.geometry import MeshGenerator, PrimitiveType
from interactive_graphics_lab.lighting import LightingSettings
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
        self._lighting = LightingSettings()
        self._camera_position = (0.0, 0.0, 2.5)
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
        view = _translation(0.0, 0.0, -2.5)
        projection = _orthographic(aspect_ratio, vertical_size=2.4, near=0.1, far=10.0)
        model_view = _multiply_matrix(view, model)
        mvp = _multiply_matrix(projection, model_view)
        normal_matrix = _normal_matrix(model)

        self._write_matrix("u_model", model)
        self._write_matrix("u_view", view)
        self._write_matrix("u_projection", projection)
        self._write_matrix("u_mvp", mvp)
        self._write_matrix3("u_normal_matrix", normal_matrix)
        self._program["u_camera_position"].value = self._camera_position
        self._material.apply(self._program)
        self._lighting.apply(self._program)
        self._mesh.render()

    def _write_matrix(self, uniform_name: str, matrix: tuple[float, ...]) -> None:
        """Upload a 4x4 row-major matrix to GLSL as column-major bytes."""
        self._program[uniform_name].write(_matrix_bytes(matrix))

    def _write_matrix3(self, uniform_name: str, matrix: tuple[float, ...]) -> None:
        """Upload a 3x3 row-major matrix to GLSL as column-major bytes."""
        self._program[uniform_name].write(_matrix3_bytes(matrix))


_VERTEX_SHADER = """
#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform mat4 u_mvp;
uniform mat3 u_normal_matrix;

out vec3 v_normal;
out vec3 v_position;
out vec2 v_uv;

void main() {
    vec4 world_position = u_model * vec4(in_position, 1.0);
    vec4 projected_position = u_projection * u_view * world_position;
    vec4 mvp_position = u_mvp * vec4(in_position, 1.0);
    gl_Position = mix(projected_position, mvp_position, 0.5);
    v_position = world_position.xyz;
    v_normal = normalize(u_normal_matrix * in_normal);
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


def _orthographic(aspect_ratio: float, vertical_size: float, near: float, far: float) -> tuple[float, ...]:
    half_height = vertical_size / 2.0
    half_width = half_height * aspect_ratio
    left = -half_width
    right = half_width
    bottom = -half_height
    top = half_height
    depth = far - near
    return (
        2.0 / (right - left), 0.0, 0.0, -(right + left) / (right - left),
        0.0, 2.0 / (top - bottom), 0.0, -(top + bottom) / (top - bottom),
        0.0, 0.0, -2.0 / depth, -(far + near) / depth,
        0.0, 0.0, 0.0, 1.0,
    )


def _multiply_matrix(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    result = [0.0] * 16
    for row in range(4):
        for column in range(4):
            result[row * 4 + column] = sum(left[row * 4 + k] * right[k * 4 + column] for k in range(4))
    return tuple(result)


def _normal_matrix(model: tuple[float, ...]) -> tuple[float, ...]:
    upper_left = (
        model[0], model[1], model[2],
        model[4], model[5], model[6],
        model[8], model[9], model[10],
    )
    return _transpose_matrix3(_inverse_matrix3(upper_left))


def _inverse_matrix3(matrix: tuple[float, ...]) -> tuple[float, ...]:
    a, b, c, d, e, f, g, h, i = matrix
    determinant = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if abs(determinant) < 1e-8:
        raise ValueError("model matrix cannot produce a valid normal matrix")
    inv_det = 1.0 / determinant
    return (
        (e * i - f * h) * inv_det,
        (c * h - b * i) * inv_det,
        (b * f - c * e) * inv_det,
        (f * g - d * i) * inv_det,
        (a * i - c * g) * inv_det,
        (c * d - a * f) * inv_det,
        (d * h - e * g) * inv_det,
        (b * g - a * h) * inv_det,
        (a * e - b * d) * inv_det,
    )


def _transpose_matrix3(matrix: tuple[float, ...]) -> tuple[float, ...]:
    return (
        matrix[0], matrix[3], matrix[6],
        matrix[1], matrix[4], matrix[7],
        matrix[2], matrix[5], matrix[8],
    )


def _matrix_bytes(row_major_matrix: tuple[float, ...]) -> bytes:
    column_major = [row_major_matrix[row * 4 + column] for column in range(4) for row in range(4)]
    return array("f", column_major).tobytes()


def _matrix3_bytes(row_major_matrix: tuple[float, ...]) -> bytes:
    column_major = [row_major_matrix[row * 3 + column] for column in range(3) for row in range(3)]
    return array("f", column_major).tobytes()
