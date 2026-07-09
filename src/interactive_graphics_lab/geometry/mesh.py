"""Reusable mesh data structures for procedural geometry."""

from __future__ import annotations

from array import array
from dataclasses import dataclass


@dataclass(frozen=True)
class Mesh:
    """Indexed triangle mesh data suitable for GPU upload."""

    positions: tuple[float, ...]
    normals: tuple[float, ...]
    uvs: tuple[float, ...]
    indices: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.positions) % 3 != 0:
            raise ValueError("positions must contain three floats per vertex")
        if len(self.normals) % 3 != 0:
            raise ValueError("normals must contain three floats per vertex")
        if len(self.uvs) % 2 != 0:
            raise ValueError("uvs must contain two floats per vertex")
        if len(self.indices) % 3 != 0:
            raise ValueError("indices must define triangles")

        vertex_count = self.vertex_count
        if len(self.normals) // 3 != vertex_count:
            raise ValueError("normals must match the position vertex count")
        if len(self.uvs) // 2 != vertex_count:
            raise ValueError("uvs must match the position vertex count")
        if self.indices and max(self.indices) >= vertex_count:
            raise ValueError("indices contain a vertex index outside the mesh")
        if self.indices and min(self.indices) < 0:
            raise ValueError("indices must be non-negative")

    @property
    def vertex_count(self) -> int:
        """Number of vertices in the mesh."""
        return len(self.positions) // 3

    @property
    def triangle_count(self) -> int:
        """Number of indexed triangles in the mesh."""
        return len(self.indices) // 3

    def interleaved_vertex_bytes(self) -> bytes:
        """Return position, normal, and UV data as interleaved float bytes."""
        vertex_data = array("f")
        for index in range(self.vertex_count):
            position_offset = index * 3
            uv_offset = index * 2
            vertex_data.extend(self.positions[position_offset : position_offset + 3])
            vertex_data.extend(self.normals[position_offset : position_offset + 3])
            vertex_data.extend(self.uvs[uv_offset : uv_offset + 2])
        return vertex_data.tobytes()

    def index_bytes(self) -> bytes:
        """Return triangle indices as unsigned integer bytes."""
        return array("I", self.indices).tobytes()
