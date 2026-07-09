"""Minimal ModernGL window application."""

from __future__ import annotations

from moderngl_window import WindowConfig

from interactive_graphics_lab.animation import AnimationSystem
from interactive_graphics_lab.core import create_default_scene
from interactive_graphics_lab.rendering.renderer import Renderer
from interactive_graphics_lab.ui import GuiController


class InteractiveGraphicsLabApp(WindowConfig):
    """Initial GPU window for the project skeleton."""

    title = "Interactive Graphics Lab"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resource_dir = "."

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._released = False
        self.scene = create_default_scene()
        self.animation = AnimationSystem(enabled=True)
        self.renderer = Renderer(self.ctx, self.scene)
        self.gui = GuiController(self.wnd._window, self.scene, self.renderer, self.animation)

    def on_render(self, time: float, frame_time: float) -> None:
        """Draw one frame."""
        width, height = self.wnd.size
        aspect_ratio = width / height if height else self.aspect_ratio
        self.animation.update(self.scene, frame_time)
        self.renderer.render(self.scene, aspect_ratio, (width, height))
        self.gui.render()

    def on_close(self) -> None:
        """Release GPU resources on shutdown."""
        if self._released:
            return
        self.gui.release()
        self.renderer.release()
        self._released = True
