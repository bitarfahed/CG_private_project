"""Minimal ModernGL window application."""

from __future__ import annotations

from moderngl_window import WindowConfig

from interactive_graphics_lab.rendering.renderer import Renderer


class InteractiveGraphicsLabApp(WindowConfig):
    """Initial GPU window for the project skeleton."""

    title = "Interactive Graphics Lab"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resource_dir = "."

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.renderer = Renderer(self.ctx)

    def on_render(self, time: float, frame_time: float) -> None:
        """Draw one empty frame."""
        self.renderer.clear()
