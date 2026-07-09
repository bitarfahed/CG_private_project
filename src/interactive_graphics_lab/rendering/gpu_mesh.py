"""GPU upload wrapper for procedural mesh data."""

from __future__ import annotations

from typing import Any

import moderngl

from interactive_graphics_lab.geometry import Mesh


class GpuMesh:
    """ModernGL buffers and vertex array for a mesh."""

    def __init__(self, context: Any, program: Any, mesh: Mesh) -> None:
        self._vertex_buffer = context.buffer(mesh.interleaved_vertex_bytes())
        self._index_buffer = context.buffer(mesh.index_bytes())
        self._vertex_array = context.vertex_array(
            program,
            [(self._vertex_buffer, "3f 3f 2f", "in_position", "in_normal", "in_uv")],
            self._index_buffer,
            index_element_size=4,
        )

    def render(self) -> None:
        """Render the indexed mesh."""
        self._vertex_array.render(mode=moderngl.TRIANGLES)

    def release(self) -> None:
        """Release GPU resources owned by this mesh."""
        self._vertex_array.release()
        self._index_buffer.release()
        self._vertex_buffer.release()
