# Interactive Graphics Lab Architecture

## Overview

Interactive Graphics Lab is organized as a small Python package with clear boundaries between application orchestration, rendering, and future graphics feature areas. The current skeleton opens a GPU/OpenGL window and clears the framebuffer to a fixed background color. No scene, geometry, material, lighting, animation, post-processing, or GUI behavior is implemented yet.

## Package Responsibilities

- `interactive_graphics_lab.main`: Command-line entry point that starts the application.
- `interactive_graphics_lab.core`: Application-level orchestration and window lifecycle.
- `interactive_graphics_lab.rendering`: GPU rendering integration and frame-level rendering helpers.
- `interactive_graphics_lab.geometry`: Future procedural mesh generation.
- `interactive_graphics_lab.materials`: Future procedural material definitions and parameters.
- `interactive_graphics_lab.lighting`: Future lighting configuration and shading-related data.
- `interactive_graphics_lab.animation`: Future time-based object, light, and material animation.
- `interactive_graphics_lab.postprocessing`: Future framebuffer and image-space effects.
- `interactive_graphics_lab.ui`: Future interactive controls.
- `interactive_graphics_lab.utils`: Future shared helpers that do not belong to a specific graphics topic.

## Rendering Backend Selection

The selected backend is ModernGL with `moderngl-window`.

ModernGL provides a Python interface for modern OpenGL rendering, while `moderngl-window` handles practical window and context creation. This combination is a good fit for the project because it keeps the setup compact, exposes GPU rendering concepts directly, and avoids spending project time on platform-specific window management.

Alternatives such as raw PyOpenGL, pyglet-only rendering, pygame OpenGL setup, and higher-level engines were considered less suitable for this scope. Raw PyOpenGL would require more boilerplate, while higher-level engines would hide too much of the rendering pipeline for a Computer Graphics course demonstration.

## Why GPU Rendering

The project is explicitly focused on modern GPU/OpenGL rendering. It is not a CPU software rasterizer and does not include manual triangle rasterization, a manual depth buffer, a software framebuffer pipeline, or a scanline renderer.

Using the GPU keeps the project aligned with real-time graphics practice and leaves room to explore shader-based materials, lighting, animation, and post-processing within a small academic timeline.

## Module Interaction

The entry point starts the application window. The core application owns the window lifecycle and delegates per-frame drawing to the rendering layer. As future phases are added, the renderer will consume data prepared by geometry, materials, lighting, animation, post-processing, and UI modules.

At this stage, the only active interaction is:

```text
main -> core application -> renderer -> OpenGL context clear
```

## Future Extension Strategy

New graphics topics should be added in focused modules without expanding the initial skeleton into a large framework. Geometry should produce GPU-ready mesh data, materials should expose shader-friendly parameters, lighting should provide clear render inputs, animation should update scene parameters over time, and post-processing should operate through framebuffer passes.

The architecture should stay practical for a two-day implementation effort: small modules, readable names, minimal abstractions, and direct rendering behavior where possible.
