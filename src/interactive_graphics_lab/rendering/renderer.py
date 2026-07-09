"""Minimal renderer for clearing the GPU framebuffer."""

from __future__ import annotations

from typing import Protocol


class ClearableContext(Protocol):
    """Subset of the ModernGL context used by the skeleton renderer."""

    def clear(
        self,
        red: float = 0.0,
        green: float = 0.0,
        blue: float = 0.0,
        alpha: float = 0.0,
        depth: float = 1.0,
        viewport: object = None,
    ) -> None:
        """Clear the active framebuffer."""


class Renderer:
    """Small rendering facade for the initial application skeleton."""

    def __init__(self, context: ClearableContext) -> None:
        self._context = context
        self.clear_color = (0.08, 0.10, 0.13, 1.0)

    def clear(self) -> None:
        """Clear the current frame to the configured background color."""
        self._context.clear(*self.clear_color)
