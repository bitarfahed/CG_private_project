"""Tests for procedural geometry generation."""

from __future__ import annotations

from math import isfinite, sqrt

import pytest

from interactive_graphics_lab.geometry import (
    MeshGenerator,
    PrimitiveType,
    generate_cone,
    generate_cylinder,
    generate_plane,
    generate_sphere,
    generate_torus,
)


@pytest.mark.parametrize("primitive", list(PrimitiveType))
def test_generated_mesh_has_valid_render_data(primitive: PrimitiveType) -> None:
    mesh = MeshGenerator.create(primitive)

    assert mesh.vertex_count > 0
    assert mesh.triangle_count > 0
    assert len(mesh.positions) == mesh.vertex_count * 3
    assert len(mesh.normals) == mesh.vertex_count * 3
    assert len(mesh.uvs) == mesh.vertex_count * 2
    assert len(mesh.indices) == mesh.triangle_count * 3
    assert min(mesh.indices) >= 0
    assert max(mesh.indices) < mesh.vertex_count
    assert all(isfinite(value) for value in mesh.positions)
    assert all(isfinite(value) for value in mesh.normals)
    assert all(isfinite(value) for value in mesh.uvs)


@pytest.mark.parametrize("primitive", list(PrimitiveType))
def test_generated_mesh_normals_are_unit_length(primitive: PrimitiveType) -> None:
    mesh = MeshGenerator.create(primitive)

    for offset in range(0, len(mesh.normals), 3):
        x, y, z = mesh.normals[offset : offset + 3]
        length = sqrt(x * x + y * y + z * z)
        assert length == pytest.approx(1.0, abs=1e-6)


@pytest.mark.parametrize(
    ("generator", "kwargs"),
    [
        (generate_plane, {"subdivisions": 0}),
        (generate_sphere, {"latitude_segments": 2}),
        (generate_sphere, {"longitude_segments": 2}),
        (generate_cylinder, {"radial_segments": 2}),
        (generate_cylinder, {"height_segments": 0}),
        (generate_cone, {"radial_segments": 2}),
        (generate_torus, {"major_segments": 2}),
        (generate_torus, {"minor_segments": 2}),
    ],
)
def test_invalid_segment_counts_raise_value_error(generator, kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        generator(**kwargs)


@pytest.mark.parametrize(
    ("generator", "kwargs"),
    [
        (generate_plane, {"width": 0}),
        (generate_sphere, {"radius": 0}),
        (generate_cylinder, {"height": 0}),
        (generate_cone, {"radius": -1}),
        (generate_torus, {"minor_radius": 0}),
    ],
)
def test_invalid_dimensions_raise_value_error(generator, kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        generator(**kwargs)
