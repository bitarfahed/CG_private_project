"""Renderer for the initial procedural geometry demo."""

from __future__ import annotations

from array import array
from math import cos, sin
from typing import Any

import moderngl

from interactive_graphics_lab.core import Scene
from interactive_graphics_lab.materials import MATERIAL_FRAGMENT_SHADER
from interactive_graphics_lab.postprocessing import PostProcessEffect, PostProcessor
from interactive_graphics_lab.rendering.gpu_mesh import GpuMesh


class Renderer:
    """GPU renderer for the current single-object scene."""

    def __init__(self, context: Any, scene: Scene) -> None:
        self._context = context
        self._released = False
        self.clear_color = (0.08, 0.10, 0.13, 1.0)
        self._context.enable(moderngl.DEPTH_TEST)
        self._program = self._context.program(vertex_shader=_VERTEX_SHADER, fragment_shader=MATERIAL_FRAGMENT_SHADER)
        self._mesh = GpuMesh(self._context, self._program, scene.mesh)
        self._mesh_source = scene.mesh
        self._post_processor = PostProcessor(self._context)

    def clear(self) -> None:
        """Clear the current frame to the configured background color."""
        self._context.clear(*self.clear_color)

    def render(self, scene: Scene, aspect_ratio: float, viewport_size: tuple[int, int]) -> None:
        """Render the current scene."""
        if self._released:
            raise RuntimeError("cannot render with a released renderer")
        self._ensure_scene_mesh(scene)
        self._post_processor.begin_scene(viewport_size, self.clear_color)
        self._render_scene(scene, aspect_ratio)
        self._post_processor.present()

    def set_post_process_effect(self, effect: PostProcessEffect) -> None:
        """Select the active post-processing effect."""
        self._post_processor.settings.effect = effect

    @property
    def post_process_effect(self) -> PostProcessEffect:
        """Return the active post-processing effect."""
        return self._post_processor.settings.effect

    def _render_scene(self, scene: Scene, aspect_ratio: float) -> None:
        """Render scene geometry into the currently bound framebuffer."""
        model = _rotation_y(scene.rotation_y_radians)
        view = _look_at(scene.camera.position, scene.camera.target)
        projection = _orthographic(aspect_ratio, scene.camera.vertical_size, scene.camera.near, scene.camera.far)
        model_view = _multiply_matrix(view, model)
        mvp = _multiply_matrix(projection, model_view)
        normal_matrix = _normal_matrix(model)

        self._write_matrix("u_model", model)
        self._write_matrix("u_mvp", mvp)
        self._write_matrix3("u_normal_matrix", normal_matrix)
        self._program["u_camera_position"].value = scene.camera.position
        scene.material.apply(self._program)
        scene.lighting.apply(self._program)
        self._mesh.render()

    def release(self) -> None:
        """Release GPU resources owned by the renderer."""
        if self._released:
            return
        self._post_processor.release()
        self._mesh.release()
        self._program.release()
        self._released = True

    def _ensure_scene_mesh(self, scene: Scene) -> None:
        if scene.mesh.vertex_count <= 0 or scene.mesh.triangle_count <= 0:
            raise ValueError("scene mesh must contain renderable triangle data")
        if scene.mesh is self._mesh_source:
            return
        self._mesh.release()
        self._mesh = GpuMesh(self._context, self._program, scene.mesh)
        self._mesh_source = scene.mesh

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
uniform mat4 u_mvp;
uniform mat3 u_normal_matrix;

out vec3 v_normal;
out vec3 v_position;
out vec2 v_uv;

void main() {
    vec4 world_position = u_model * vec4(in_position, 1.0);
    gl_Position = u_mvp * vec4(in_position, 1.0);
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


def _look_at(eye: tuple[float, float, float], target: tuple[float, float, float]) -> tuple[float, ...]:
    forward = _normalize((target[0] - eye[0], target[1] - eye[1], target[2] - eye[2]))
    side = _normalize(_cross(forward, (0.0, 1.0, 0.0)))
    up = _cross(side, forward)
    return (
        side[0], side[1], side[2], -_dot(side, eye),
        up[0], up[1], up[2], -_dot(up, eye),
        -forward[0], -forward[1], -forward[2], _dot(forward, eye),
        0.0, 0.0, 0.0, 1.0,
    )


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


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return left[0] * right[0] + left[1] * right[1] + left[2] * right[2]


def _cross(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _normalize(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = (vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2]) ** 0.5
    if length < 1e-8:
        raise ValueError("camera view vector cannot be zero length")
    return (vector[0] / length, vector[1] / length, vector[2] / length)


def _matrix_bytes(row_major_matrix: tuple[float, ...]) -> bytes:
    column_major = [row_major_matrix[row * 4 + column] for column in range(4) for row in range(4)]
    return array("f", column_major).tobytes()


def _matrix3_bytes(row_major_matrix: tuple[float, ...]) -> bytes:
    column_major = [row_major_matrix[row * 3 + column] for column in range(3) for row in range(3)]
    return array("f", column_major).tobytes()
