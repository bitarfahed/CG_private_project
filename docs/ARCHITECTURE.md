# Interactive Graphics Lab Architecture

## Overview

Interactive Graphics Lab is organized as a small Python package with clear boundaries between application orchestration, rendering, and future graphics feature areas. The current application opens a GPU/OpenGL window and renders one procedurally generated mesh with a shader-based procedural material and Phong lighting. No scene management, animation, post-processing, or GUI behavior is implemented yet.

## Package Responsibilities

- `interactive_graphics_lab.main`: Command-line entry point that starts the application.
- `interactive_graphics_lab.core`: Application-level orchestration and window lifecycle.
- `interactive_graphics_lab.rendering`: GPU rendering integration, mesh buffer upload, and frame-level rendering helpers.
- `interactive_graphics_lab.geometry`: Procedural mesh generation and reusable mesh data structures.
- `interactive_graphics_lab.materials`: Procedural material definitions, defaults, shader logic, and uniform upload.
- `interactive_graphics_lab.lighting`: Ambient and point-light data used by the Phong shader pipeline.
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

The entry point starts the application window. The core application owns the window lifecycle and delegates per-frame drawing to the rendering layer. The renderer currently requests one procedural mesh from the geometry module, uploads its vertex and index data to the GPU, applies one procedural material, uploads lighting uniforms, and draws it with a Phong shader.

At this stage, the active interaction is:

```text
main -> core application -> renderer -> geometry mesh + material + lighting -> GPU buffers -> OpenGL draw
```

## Geometry Module

The geometry module exposes a `Mesh` representation containing positions, normals, UV coordinates, and triangle indices. Primitive generation is available through individual generator functions and the `MeshGenerator` factory. Supported primitives are plane, cube, UV sphere, cylinder, cone, and torus.

All mesh data is generated mathematically. The project does not load OBJ, STL, GLTF, or other external mesh formats.

## Materials Module

The materials module exposes a `ProceduralMaterial` abstraction with a material type, display name, color parameters, scale, frequency, contrast, noise strength, and a time placeholder for future animation. A small `MaterialLibrary` provides defaults for solid color, checker, stripes, gradient, marble, wood, clouds, and lava/energy materials.

Procedural appearance is generated in GLSL from UV coordinates, positions, normals, and shader noise. The project does not load image texture files for these materials.

## Lighting Module

The lighting module defines ambient lighting settings and point-light data for shader-based Phong shading. The current renderer uploads camera position, ambient light, point-light color, point-light position, intensity, specular strength, and shininess. Lighting modifies the procedural material color rather than replacing it.

## Future Extension Strategy

New graphics topics should be added in focused modules without expanding the initial skeleton into a large framework. Geometry should produce GPU-ready mesh data, materials should expose shader-friendly parameters, lighting should provide clear render inputs, animation should update scene parameters over time, and post-processing should operate through framebuffer passes.

The architecture should stay practical for a two-day implementation effort: small modules, readable names, minimal abstractions, and direct rendering behavior where possible.
