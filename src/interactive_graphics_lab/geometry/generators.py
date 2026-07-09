"""Procedural mesh generators for basic primitives."""

from __future__ import annotations

from enum import StrEnum
from math import cos, pi, sin, sqrt

from interactive_graphics_lab.geometry.mesh import Mesh


class PrimitiveType(StrEnum):
    """Supported procedural primitive names."""

    PLANE = "plane"
    CUBE = "cube"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    CONE = "cone"
    TORUS = "torus"


class MeshGenerator:
    """Factory for procedural primitive meshes."""

    @staticmethod
    def create(primitive: PrimitiveType | str, **parameters: object) -> Mesh:
        """Create a mesh for the requested primitive."""
        primitive_type = PrimitiveType(primitive)
        generators = {
            PrimitiveType.PLANE: generate_plane,
            PrimitiveType.CUBE: generate_cube,
            PrimitiveType.SPHERE: generate_sphere,
            PrimitiveType.CYLINDER: generate_cylinder,
            PrimitiveType.CONE: generate_cone,
            PrimitiveType.TORUS: generate_torus,
        }
        return generators[primitive_type](**parameters)


def generate_plane(width: float = 2.0, depth: float = 2.0, subdivisions: int = 1) -> Mesh:
    """Generate a subdivided XY plane with camera-facing normals."""
    _require_positive("width", width)
    _require_positive("depth", depth)
    _require_minimum("subdivisions", subdivisions, 1)

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    indices: list[int] = []

    for z_index in range(subdivisions + 1):
        v = z_index / subdivisions
        y = (v - 0.5) * depth
        for x_index in range(subdivisions + 1):
            u = x_index / subdivisions
            x = (u - 0.5) * width
            positions.extend((x, y, 0.0))
            normals.extend((0.0, 0.0, 1.0))
            uvs.extend((u, v))

    row_size = subdivisions + 1
    for z_index in range(subdivisions):
        for x_index in range(subdivisions):
            lower_left = z_index * row_size + x_index
            lower_right = lower_left + 1
            upper_left = lower_left + row_size
            upper_right = upper_left + 1
            indices.extend((lower_left, lower_right, upper_left))
            indices.extend((lower_right, upper_right, upper_left))

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def generate_cube(size: float = 1.5) -> Mesh:
    """Generate a cube with separate vertices per face for crisp normals."""
    _require_positive("size", size)

    half_size = size / 2
    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    indices: list[int] = []

    def add_face(corners: tuple[tuple[float, float, float], ...], normal: tuple[float, float, float]) -> None:
        base_index = len(positions) // 3
        for corner, uv in zip(corners, ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)), strict=True):
            positions.extend(corner)
            normals.extend(normal)
            uvs.extend(uv)
        indices.extend((base_index, base_index + 1, base_index + 2))
        indices.extend((base_index, base_index + 2, base_index + 3))

    n = half_size
    add_face(((-n, -n, n), (n, -n, n), (n, n, n), (-n, n, n)), (0.0, 0.0, 1.0))
    add_face(((n, -n, -n), (-n, -n, -n), (-n, n, -n), (n, n, -n)), (0.0, 0.0, -1.0))
    add_face(((n, -n, n), (n, -n, -n), (n, n, -n), (n, n, n)), (1.0, 0.0, 0.0))
    add_face(((-n, -n, -n), (-n, -n, n), (-n, n, n), (-n, n, -n)), (-1.0, 0.0, 0.0))
    add_face(((-n, n, n), (n, n, n), (n, n, -n), (-n, n, -n)), (0.0, 1.0, 0.0))
    add_face(((-n, -n, -n), (n, -n, -n), (n, -n, n), (-n, -n, n)), (0.0, -1.0, 0.0))

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def generate_sphere(radius: float = 0.85, latitude_segments: int = 24, longitude_segments: int = 48) -> Mesh:
    """Generate a UV sphere without degenerate pole triangles."""
    _require_positive("radius", radius)
    _require_minimum("latitude_segments", latitude_segments, 3)
    _require_minimum("longitude_segments", longitude_segments, 3)

    positions: list[float] = [0.0, radius, 0.0]
    normals: list[float] = [0.0, 1.0, 0.0]
    uvs: list[float] = [0.5, 1.0]
    indices: list[int] = []

    ring_starts: list[int] = []
    for lat_index in range(1, latitude_segments):
        theta = pi * lat_index / latitude_segments
        y = cos(theta)
        ring_radius = sin(theta)
        ring_starts.append(len(positions) // 3)
        for lon_index in range(longitude_segments):
            phi = 2 * pi * lon_index / longitude_segments
            x = ring_radius * cos(phi)
            z = ring_radius * sin(phi)
            positions.extend((radius * x, radius * y, radius * z))
            normals.extend((x, y, z))
            uvs.extend((lon_index / longitude_segments, 1.0 - lat_index / latitude_segments))

    south_index = len(positions) // 3
    positions.extend((0.0, -radius, 0.0))
    normals.extend((0.0, -1.0, 0.0))
    uvs.extend((0.5, 0.0))

    first_ring = ring_starts[0]
    for lon_index in range(longitude_segments):
        next_lon = (lon_index + 1) % longitude_segments
        indices.extend((0, first_ring + next_lon, first_ring + lon_index))

    for ring_index in range(len(ring_starts) - 1):
        current_ring = ring_starts[ring_index]
        next_ring = ring_starts[ring_index + 1]
        for lon_index in range(longitude_segments):
            next_lon = (lon_index + 1) % longitude_segments
            current = current_ring + lon_index
            current_next = current_ring + next_lon
            below = next_ring + lon_index
            below_next = next_ring + next_lon
            indices.extend((current, current_next, below))
            indices.extend((current_next, below_next, below))

    last_ring = ring_starts[-1]
    for lon_index in range(longitude_segments):
        next_lon = (lon_index + 1) % longitude_segments
        indices.extend((south_index, last_ring + lon_index, last_ring + next_lon))

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def generate_cylinder(
    radius: float = 0.65,
    height: float = 1.5,
    radial_segments: int = 48,
    height_segments: int = 1,
) -> Mesh:
    """Generate a cylinder with capped ends."""
    _require_positive("radius", radius)
    _require_positive("height", height)
    _require_minimum("radial_segments", radial_segments, 3)
    _require_minimum("height_segments", height_segments, 1)

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    indices: list[int] = []
    half_height = height / 2

    for y_index in range(height_segments + 1):
        v = y_index / height_segments
        y = (v - 0.5) * height
        for radial_index in range(radial_segments + 1):
            u = radial_index / radial_segments
            phi = 2 * pi * u
            x = cos(phi)
            z = sin(phi)
            positions.extend((radius * x, y, radius * z))
            normals.extend((x, 0.0, z))
            uvs.extend((u, v))

    row_size = radial_segments + 1
    for y_index in range(height_segments):
        for radial_index in range(radial_segments):
            lower = y_index * row_size + radial_index
            lower_next = lower + 1
            upper = lower + row_size
            upper_next = upper + 1
            indices.extend((lower, upper, lower_next))
            indices.extend((lower_next, upper, upper_next))

    _add_cap(positions, normals, uvs, indices, radius, half_height, radial_segments, top=True)
    _add_cap(positions, normals, uvs, indices, radius, -half_height, radial_segments, top=False)

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def generate_cone(radius: float = 0.75, height: float = 1.6, radial_segments: int = 48) -> Mesh:
    """Generate a cone with a capped base."""
    _require_positive("radius", radius)
    _require_positive("height", height)
    _require_minimum("radial_segments", radial_segments, 3)

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    indices: list[int] = []
    half_height = height / 2
    slope_normal_y = radius / sqrt(radius * radius + height * height)
    slope_normal_radius = height / sqrt(radius * radius + height * height)

    for radial_index in range(radial_segments + 1):
        u = radial_index / radial_segments
        phi = 2 * pi * u
        x = cos(phi)
        z = sin(phi)
        normal = (slope_normal_radius * x, slope_normal_y, slope_normal_radius * z)
        positions.extend((radius * x, -half_height, radius * z))
        normals.extend(normal)
        uvs.extend((u, 0.0))
        positions.extend((0.0, half_height, 0.0))
        normals.extend(normal)
        uvs.extend((u, 1.0))

    for radial_index in range(radial_segments):
        base = radial_index * 2
        next_base = base + 2
        indices.extend((base, base + 1, next_base))

    _add_cap(positions, normals, uvs, indices, radius, -half_height, radial_segments, top=False)

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def generate_torus(
    major_radius: float = 0.6,
    minor_radius: float = 0.22,
    major_segments: int = 48,
    minor_segments: int = 16,
) -> Mesh:
    """Generate a torus around the Y axis."""
    _require_positive("major_radius", major_radius)
    _require_positive("minor_radius", minor_radius)
    _require_minimum("major_segments", major_segments, 3)
    _require_minimum("minor_segments", minor_segments, 3)

    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    indices: list[int] = []

    for major_index in range(major_segments + 1):
        u = major_index / major_segments
        major_angle = 2 * pi * u
        major_x = cos(major_angle)
        major_z = sin(major_angle)
        for minor_index in range(minor_segments + 1):
            v = minor_index / minor_segments
            minor_angle = 2 * pi * v
            minor_xz = cos(minor_angle)
            minor_y = sin(minor_angle)
            normal = (minor_xz * major_x, minor_y, minor_xz * major_z)
            distance_from_center = major_radius + minor_radius * minor_xz
            positions.extend((distance_from_center * major_x, minor_radius * minor_y, distance_from_center * major_z))
            normals.extend(normal)
            uvs.extend((u, v))

    row_size = minor_segments + 1
    for major_index in range(major_segments):
        for minor_index in range(minor_segments):
            current = major_index * row_size + minor_index
            current_next = current + 1
            outer = current + row_size
            outer_next = outer + 1
            indices.extend((current, current_next, outer))
            indices.extend((current_next, outer_next, outer))

    return Mesh(tuple(positions), tuple(normals), tuple(uvs), tuple(indices))


def _add_cap(
    positions: list[float],
    normals: list[float],
    uvs: list[float],
    indices: list[int],
    radius: float,
    y: float,
    radial_segments: int,
    *,
    top: bool,
) -> None:
    normal = (0.0, 1.0, 0.0) if top else (0.0, -1.0, 0.0)
    center_index = len(positions) // 3
    positions.extend((0.0, y, 0.0))
    normals.extend(normal)
    uvs.extend((0.5, 0.5))

    ring_start = len(positions) // 3
    for radial_index in range(radial_segments):
        u = radial_index / radial_segments
        phi = 2 * pi * u
        x = cos(phi)
        z = sin(phi)
        positions.extend((radius * x, y, radius * z))
        normals.extend(normal)
        uvs.extend((0.5 + 0.5 * x, 0.5 + 0.5 * z))

    for radial_index in range(radial_segments):
        current = ring_start + radial_index
        next_index = ring_start + (radial_index + 1) % radial_segments
        if top:
            indices.extend((center_index, next_index, current))
        else:
            indices.extend((center_index, current, next_index))


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def _require_minimum(name: str, value: int, minimum: int) -> None:
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
