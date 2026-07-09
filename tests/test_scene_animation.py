"""Tests for pure Python scene and animation state."""

from __future__ import annotations

import pytest

from interactive_graphics_lab.animation import AnimationSystem
from interactive_graphics_lab.core import create_default_scene
from interactive_graphics_lab.geometry import MeshGenerator, PrimitiveType
from interactive_graphics_lab.materials import MaterialLibrary, MaterialType
from interactive_graphics_lab.postprocessing import PostProcessEffect, PostProcessSettings


def test_default_scene_has_expected_state() -> None:
    scene = create_default_scene()

    assert scene.mesh.vertex_count > 0
    assert scene.active_primitive == PrimitiveType.SPHERE
    assert scene.active_material == MaterialType.MARBLE
    assert scene.material.material_type == MaterialType.MARBLE
    assert len(scene.lighting.point_lights) >= 1
    assert scene.camera.position == (0.0, 0.0, 2.5)


def test_camera_orbits_around_fixed_target() -> None:
    scene = create_default_scene()

    scene.camera.orbit(90.0, 30.0)

    assert scene.camera.target == (0.0, 0.0, 0.0)
    assert scene.camera.position[0] > 0.0
    assert scene.camera.position[1] > 0.0
    assert scene.camera.position[2] == pytest.approx(0.0, abs=1e-6)


def test_camera_zoom_is_clamped_and_resettable() -> None:
    scene = create_default_scene()

    scene.camera.zoom(100.0)
    assert scene.camera.distance == scene.camera.min_distance
    assert scene.camera.vertical_size == scene.camera.min_vertical_size

    scene.camera.zoom(-100.0)
    assert scene.camera.distance == scene.camera.max_distance
    assert scene.camera.vertical_size == scene.camera.max_vertical_size

    scene.camera.orbit(45.0, 45.0)
    scene.camera.reset()

    assert scene.camera.position == (0.0, 0.0, 2.5)
    assert scene.camera.vertical_size == pytest.approx(2.4)


def test_scene_geometry_and_material_can_be_changed_without_gpu() -> None:
    scene = create_default_scene()

    scene.active_primitive = PrimitiveType.TORUS
    scene.mesh = MeshGenerator.create(scene.active_primitive)
    scene.active_material = MaterialType.WOOD
    scene.material = MaterialLibrary().get(scene.active_material)

    assert scene.active_primitive == PrimitiveType.TORUS
    assert scene.mesh.triangle_count > 0
    assert scene.material.material_type == MaterialType.WOOD


def test_animation_updates_scene_from_delta_time() -> None:
    scene = create_default_scene()
    animation = AnimationSystem(rotation_speed_degrees=30.0)
    initial_rotation = scene.transform.rotation_y_degrees
    initial_light_position = scene.lighting.point_lights[0].position

    animation.update(scene, 0.5)

    assert scene.transform.rotation_y_degrees == pytest.approx(initial_rotation + 15.0)
    assert scene.material.time == pytest.approx(0.5)
    assert scene.lighting.point_lights[0].position != initial_light_position


def test_disabled_animation_does_not_modify_scene() -> None:
    scene = create_default_scene()
    animation = AnimationSystem(enabled=False)
    initial_rotation = scene.transform.rotation_y_degrees
    initial_material = scene.material
    initial_lighting = scene.lighting

    animation.update(scene, 1.0)

    assert scene.transform.rotation_y_degrees == initial_rotation
    assert scene.material == initial_material
    assert scene.lighting == initial_lighting


def test_post_processing_effect_setting_can_change_without_gpu() -> None:
    settings = PostProcessSettings()

    settings.effect = PostProcessEffect.SOBEL

    assert settings.effect == PostProcessEffect.SOBEL
