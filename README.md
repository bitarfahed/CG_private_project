# Interactive Graphics Lab

Interactive Graphics Lab is a compact Python desktop application for exploring core Computer Graphics course topics in one cohesive GPU-rendered scene. It demonstrates procedural geometry, shader-based procedural materials, Phong lighting, animation, framebuffer post-processing, and a small interactive GUI.

This project uses a modern GPU/OpenGL pipeline through ModernGL. It is not a CPU software rasterizer and does not implement manual triangle rasterization, a manual Z-buffer, or a software framebuffer pipeline.

## Screenshot

No screenshot is included in the repository yet.

> Placeholder: add a screenshot of the running application here for GitHub presentation.

## Features

- GPU/OpenGL rendering with ModernGL and `moderngl-window`
- Procedural mesh generation for:
  - Plane
  - Cube
  - Sphere
  - Cylinder
  - Cone
  - Torus
- Procedural shader materials:
  - Solid Color
  - Checker
  - Stripes
  - Gradient
  - Marble
  - Wood
  - Noise / Clouds
  - Lava / Energy
- Phong lighting with ambient, diffuse, and specular components
- Configurable point lights in code and through the GUI
- Frame-rate independent animation for object rotation, light motion, and material time
- Framebuffer-based post-processing:
  - None / passthrough
  - Grayscale
  - Pixelate
  - Sobel edge detection
- ImGui control panel for selecting geometry, material, lighting values, animation state, and post-processing effect
- Simple orbit camera controls for inspecting the scene
- Basic CPU-side unit tests for deterministic non-visual logic

## Demonstrated Graphics Concepts

- Procedural mesh construction from mathematical equations
- Vertex attributes: positions, normals, UV coordinates, and triangle indices
- GPU buffer upload and indexed drawing
- Shader-based procedural appearance
- Phong reflection model
- Normal transformation for lighting
- Real-time animation using delta time
- Orbit camera view transformation
- Render-to-texture and fullscreen post-processing
- Immediate-mode GUI integration with a GPU render loop

## Technology Stack

- Python 3.11+
- ModernGL
- `moderngl-window`
- ImGui via `imgui`
- PyOpenGL for the ImGui backend
- pytest
- uv for dependency and command management

## Installation

Install `uv` if it is not already available, then clone the repository and run:

```bash
uv sync
```

This installs the application dependencies from `pyproject.toml` and `uv.lock`.

## Running The Application

```bash
uv run interactive-graphics-lab
```

The application opens a desktop window with an animated procedural scene and an ImGui control panel.

## GUI Overview

The GUI panel provides compact controls for:

- Geometry selection: sphere, torus, cone, cylinder, plane, cube
- Material selection: all implemented procedural materials
- Lighting: color, position, and intensity for one editable point light
- Animation: enable/disable animation and adjust rotation speed
- Post Processing: select one of the implemented image-space effects

The GUI edits existing scene and renderer state. It does not own geometry generation, material formulas, lighting calculations, or post-processing shader logic.

## Camera Controls

- Right Mouse Button + Drag: orbit the camera around the center of the scene
- Mouse Wheel: zoom in or out
- `R`: reset the camera to the default view

Camera controls work only when the cursor is not interacting with the GUI panel. On a touchpad, right-click may correspond to a two-finger click or the operating system's configured secondary-click gesture.

## Testing

Run the test suite with:

```bash
uv run pytest
```

The tests cover deterministic CPU-side behavior such as procedural mesh invariants, material registry behavior, post-processing effect configuration, scene defaults, and animation state updates. They intentionally avoid GUI automation, OpenGL context creation, shader compilation, screenshots, and visual correctness checks.

## Project Structure

```text
src/interactive_graphics_lab/
    main.py                 Application entry point
    core/                   Application orchestration and minimal scene state
    rendering/              ModernGL renderer and GPU mesh upload
    geometry/               Procedural mesh data and generators
    materials/              Procedural material definitions and GLSL shader logic
    lighting/               Ambient and point-light settings
    animation/              Delta-time scene updates
    postprocessing/         Offscreen framebuffer and screen-space effects
    ui/                     ImGui control panel
    utils/                  Reserved for shared helpers

tests/                      CPU-side unit tests
docs/                       Project planning, architecture, prompt log, and final report
```

## Academic Context

Interactive Graphics Lab was developed as a small university Computer Graphics project using an incremental Vibe Coding workflow. Each implementation step focused on one topic at a time, making the project suitable for demonstrating course concepts without attempting to become a full rendering engine.

## Limitations

- No asset loading; all core geometry is procedural.
- No scene graph or multi-object editor.
- No shadow mapping.
- No physically based rendering.
- No normal mapping or image texture loading.
- No CPU rasterizer, manual Z-buffer, or software framebuffer pipeline.
- GUI is intentionally compact and demonstration-oriented.
- Tests do not verify visual output or shader rendering.