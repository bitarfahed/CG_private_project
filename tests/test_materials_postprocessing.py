"""Tests for pure Python material and post-processing configuration."""

from __future__ import annotations

import pytest

from interactive_graphics_lab.materials import MaterialLibrary, MaterialType, ProceduralMaterial
from interactive_graphics_lab.postprocessing import PostProcessEffect, PostProcessSettings


def test_material_library_contains_all_material_types() -> None:
    library = MaterialLibrary()

    for material_type in MaterialType:
        material = library.get(material_type)
        assert material.material_type == material_type
        assert material.name
        assert len(material.base_color) == 3
        assert len(material.secondary_color) == 3
        assert material.scale > 0
        assert material.frequency > 0
        assert material.contrast >= 0
        assert material.noise_strength >= 0


def test_material_library_accepts_string_material_type() -> None:
    material = MaterialLibrary().get("marble")

    assert material.material_type == MaterialType.MARBLE


def test_invalid_material_selection_fails_clearly() -> None:
    with pytest.raises(ValueError):
        MaterialLibrary().get("not-a-material")


def test_invalid_material_parameters_raise_value_error() -> None:
    with pytest.raises(ValueError):
        ProceduralMaterial(
            material_type=MaterialType.SOLID,
            name="Invalid",
            base_color=(2.0, 0.0, 0.0),
        )


def test_post_processing_effects_and_default_setting() -> None:
    expected = {
        PostProcessEffect.NONE,
        PostProcessEffect.GRAYSCALE,
        PostProcessEffect.PIXELATE,
        PostProcessEffect.SOBEL,
    }

    assert set(PostProcessEffect) == expected
    assert PostProcessSettings().effect in expected


def test_invalid_post_processing_effect_selection_fails_clearly() -> None:
    with pytest.raises(ValueError):
        PostProcessEffect("not-an-effect")
