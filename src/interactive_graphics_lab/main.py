"""Application entry point for Interactive Graphics Lab."""

from __future__ import annotations

import moderngl_window

from interactive_graphics_lab.core.application import InteractiveGraphicsLabApp


def main() -> None:
    """Run the application window."""
    moderngl_window.run_window_config(InteractiveGraphicsLabApp)


if __name__ == "__main__":
    main()
