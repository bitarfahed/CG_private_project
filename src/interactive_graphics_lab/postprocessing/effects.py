"""Framebuffer-based post-processing effects."""

from __future__ import annotations

from array import array
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import moderngl


class PostProcessEffect(StrEnum):
    """Available post-processing effects."""

    NONE = "none"
    GRAYSCALE = "grayscale"
    PIXELATE = "pixelate"
    SOBEL = "sobel"


@dataclass
class PostProcessSettings:
    """Runtime-selectable post-processing parameters."""

    effect: PostProcessEffect = PostProcessEffect.PIXELATE
    pixel_size: float = 7.0


class PostProcessor:
    """Render-to-texture pipeline and fullscreen post-processing pass."""

    def __init__(self, context: Any, settings: PostProcessSettings | None = None) -> None:
        self._context = context
        self.settings = settings or PostProcessSettings()
        self._size = (0, 0)
        self._color_texture: Any | None = None
        self._depth_buffer: Any | None = None
        self._framebuffer: Any | None = None
        self._quad_buffer = self._context.buffer(_FULLSCREEN_QUAD.tobytes())
        self._programs = {
            effect: self._context.program(vertex_shader=_FULLSCREEN_VERTEX_SHADER, fragment_shader=shader)
            for effect, shader in _EFFECT_SHADERS.items()
        }
        self._quad_arrays = {
            effect: self._context.vertex_array(
                program,
                [(self._quad_buffer, "2f 2f", "in_position", "in_uv")],
            )
            for effect, program in self._programs.items()
        }

    def begin_scene(self, size: tuple[int, int], clear_color: tuple[float, float, float, float]) -> None:
        """Bind and clear the offscreen scene framebuffer."""
        self._ensure_size(size)
        if self._framebuffer is None:
            raise RuntimeError("post-processing framebuffer was not initialized")
        self._framebuffer.use()
        self._context.viewport = (0, 0, self._size[0], self._size[1])
        self._context.enable(moderngl.DEPTH_TEST)
        self._framebuffer.clear(*clear_color)

    def present(self) -> None:
        """Draw the selected effect to the default framebuffer."""
        if self._color_texture is None:
            raise RuntimeError("post-processing color texture was not initialized")

        program = self._programs[self.settings.effect]
        vertex_array = self._quad_arrays[self.settings.effect]

        self._context.screen.use()
        self._context.viewport = (0, 0, self._size[0], self._size[1])
        self._context.disable(moderngl.DEPTH_TEST)
        self._color_texture.use(location=0)
        _set_uniform(program, "u_scene_texture", 0)
        _set_uniform(program, "u_resolution", (float(self._size[0]), float(self._size[1])))
        _set_uniform(program, "u_pixel_size", self.settings.pixel_size)
        vertex_array.render(mode=moderngl.TRIANGLE_STRIP)
        self._context.enable(moderngl.DEPTH_TEST)

    def release(self) -> None:
        """Release all GPU resources owned by the post processor."""
        self._release_framebuffer_resources()
        for vertex_array in self._quad_arrays.values():
            vertex_array.release()
        for program in self._programs.values():
            program.release()
        self._quad_buffer.release()

    def _ensure_size(self, size: tuple[int, int]) -> None:
        width = max(1, int(size[0]))
        height = max(1, int(size[1]))
        if self._size == (width, height):
            return

        self._release_framebuffer_resources()
        self._size = (width, height)
        self._color_texture = self._context.texture(self._size, components=4)
        self._color_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self._depth_buffer = self._context.depth_renderbuffer(self._size)
        self._framebuffer = self._context.framebuffer(
            color_attachments=[self._color_texture],
            depth_attachment=self._depth_buffer,
        )

    def _release_framebuffer_resources(self) -> None:
        for resource in (self._framebuffer, self._depth_buffer, self._color_texture):
            if resource is not None:
                resource.release()
        self._framebuffer = None
        self._depth_buffer = None
        self._color_texture = None


def _set_uniform(program: Any, name: str, value: object) -> None:
    try:
        program[name].value = value
    except KeyError:
        pass


_FULLSCREEN_QUAD = array(
    "f",
    (
        -1.0, -1.0, 0.0, 0.0,
        1.0, -1.0, 1.0, 0.0,
        -1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
    ),
)

_FULLSCREEN_VERTEX_SHADER = """
#version 330

in vec2 in_position;
in vec2 in_uv;

out vec2 v_uv;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_uv = in_uv;
}
"""

_PASSTHROUGH_FRAGMENT_SHADER = """
#version 330

uniform sampler2D u_scene_texture;

in vec2 v_uv;
out vec4 frag_color;

void main() {
    frag_color = texture(u_scene_texture, v_uv);
}
"""

_GRAYSCALE_FRAGMENT_SHADER = """
#version 330

uniform sampler2D u_scene_texture;

in vec2 v_uv;
out vec4 frag_color;

void main() {
    vec3 color = texture(u_scene_texture, v_uv).rgb;
    float luminance = dot(color, vec3(0.2126, 0.7152, 0.0722));
    frag_color = vec4(vec3(luminance), 1.0);
}
"""

_PIXELATE_FRAGMENT_SHADER = """
#version 330

uniform sampler2D u_scene_texture;
uniform vec2 u_resolution;
uniform float u_pixel_size;

in vec2 v_uv;
out vec4 frag_color;

void main() {
    vec2 pixel_count = max(u_resolution / max(u_pixel_size, 1.0), vec2(1.0));
    vec2 pixelated_uv = (floor(v_uv * pixel_count) + 0.5) / pixel_count;
    frag_color = texture(u_scene_texture, pixelated_uv);
}
"""

_SOBEL_FRAGMENT_SHADER = """
#version 330

uniform sampler2D u_scene_texture;
uniform vec2 u_resolution;

in vec2 v_uv;
out vec4 frag_color;

float luminance_at(vec2 uv) {
    vec3 color = texture(u_scene_texture, uv).rgb;
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

void main() {
    vec2 texel = 1.0 / max(u_resolution, vec2(1.0));
    float tl = luminance_at(v_uv + texel * vec2(-1.0, 1.0));
    float tc = luminance_at(v_uv + texel * vec2(0.0, 1.0));
    float tr = luminance_at(v_uv + texel * vec2(1.0, 1.0));
    float ml = luminance_at(v_uv + texel * vec2(-1.0, 0.0));
    float mr = luminance_at(v_uv + texel * vec2(1.0, 0.0));
    float bl = luminance_at(v_uv + texel * vec2(-1.0, -1.0));
    float bc = luminance_at(v_uv + texel * vec2(0.0, -1.0));
    float br = luminance_at(v_uv + texel * vec2(1.0, -1.0));

    float gx = -tl - 2.0 * ml - bl + tr + 2.0 * mr + br;
    float gy = tl + 2.0 * tc + tr - bl - 2.0 * bc - br;
    float edge = clamp(length(vec2(gx, gy)), 0.0, 1.0);
    vec3 scene_color = texture(u_scene_texture, v_uv).rgb;
    vec3 edge_color = mix(scene_color * 0.25, vec3(1.0), edge);
    frag_color = vec4(edge_color, 1.0);
}
"""

_EFFECT_SHADERS = {
    PostProcessEffect.NONE: _PASSTHROUGH_FRAGMENT_SHADER,
    PostProcessEffect.GRAYSCALE: _GRAYSCALE_FRAGMENT_SHADER,
    PostProcessEffect.PIXELATE: _PIXELATE_FRAGMENT_SHADER,
    PostProcessEffect.SOBEL: _SOBEL_FRAGMENT_SHADER,
}
