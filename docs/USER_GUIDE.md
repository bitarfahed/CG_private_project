# Interactive Graphics Lab User Guide

## Project Purpose

Interactive Graphics Lab is a compact desktop application for demonstrating core Computer Graphics course topics in one GPU-rendered scene. It shows procedural geometry, shader-based procedural materials, Phong lighting, real-time animation, framebuffer post-processing, and a small ImGui control panel.

The project uses ModernGL and OpenGL for rendering. It is not a CPU software rasterizer and does not implement manual triangle rasterization, a manual Z-buffer, or a software framebuffer pipeline.

## System Requirements

- Python 3.11 or newer
- `uv` for dependency installation and command execution
- A desktop environment capable of opening an OpenGL window
- A graphics driver with support for the OpenGL features required by ModernGL

The project is intended to run as a local desktop application, not as a web application or command-line renderer.

## Installing Dependencies

From the repository root, install the project dependencies with:

```bash
uv sync
```

This reads `pyproject.toml` and `uv.lock`, creates or updates the local environment, and installs the runtime dependencies used by the application.

## Running the Application

Start the application with:

```bash
uv run interactive-graphics-lab
```

The application opens a window containing the rendered scene and an ImGui control panel titled `Interactive Graphics Lab`.

## Running Tests

Run the test suite with:

```bash
uv run pytest
```

The tests focus on deterministic Python-side logic such as procedural mesh validity, material registry behavior, post-processing configuration, scene defaults, and animation updates. They do not test GUI interaction, OpenGL context creation, shader compilation, screenshots, or visual correctness.

## GUI Controls

### Geometry

The Geometry section selects the active procedural primitive. Implemented options are:

- Sphere
- Torus
- Cone
- Cylinder
- Plane
- Cube

Selecting a new primitive regenerates the active mesh and uploads it for rendering.

### Material

The Material section selects the procedural shader material applied to the current mesh. Implemented materials are:

- Solid Color
- Checker
- Stripes
- Gradient
- Marble
- Wood
- Clouds
- Lava

Materials are generated mathematically in shaders. The application does not load image texture files.

### Lighting

The Lighting section edits one point light from the scene's lighting setup. Controls include:

- Light Color
- Light X
- Light Y
- Light Z
- Intensity

These controls affect the visible Phong lighting response, including diffuse shading and specular highlights.

### Animation

The Animation section controls the simple real-time animation system:

- `Animation On`: enables or disables animation updates
- `Rotation Speed`: adjusts object rotation speed

When animation is enabled, the object rotates and one light moves over time. The procedural material time value is also updated.

### Post Processing

The Post Processing section selects the active screen-space effect. Implemented options are:

- None
- Grayscale
- Pixelate
- Sobel

The scene is rendered to an offscreen framebuffer first, then the selected effect is applied through a fullscreen post-processing pass.

## Recommended Instructor Demo Flow

1. Launch the application with `uv run interactive-graphics-lab`.
2. Start with the default scene and point out the procedural material, Phong lighting, and animated motion.
3. Open the Geometry combo box and switch between Sphere, Torus, Cone, Cylinder, Plane, and Cube.
4. Switch materials, especially Marble, Wood, Checker, Clouds, and Lava, to show shader-based procedural appearance.
5. Adjust the editable light's position, color, and intensity to demonstrate the effect of point-light location and color on Phong shading.
6. Toggle animation off and on to show that scene updates are separated from rendering.
7. Change the post-processing effect from None to Grayscale, Pixelate, and Sobel to demonstrate framebuffer-based image-space rendering.
8. Run `uv run pytest` to show the basic non-visual test suite.

## Known Limitations

- The application renders a single active object rather than a multi-object scene.
- There is no scene graph.
- There are no camera controls.
- There is no asset loading; geometry is procedural.
- There is no image texture loading.
- There are no shadows, shadow maps, or physically based rendering.
- Material parameters are mostly code-defined rather than fully exposed in the GUI.
- The GUI is intentionally compact and demonstration-oriented.
- Tests do not verify rendered output or visual correctness.

## Troubleshooting

### `uv` is not recognized

Install `uv` and ensure it is available on your system `PATH`, then run `uv sync` again from the repository root.

### The application window does not open

Confirm that dependencies are installed with `uv sync`. Also verify that the machine has a working desktop session and graphics driver capable of creating an OpenGL context.

### OpenGL or ModernGL context errors occur

Update the graphics driver and try running the application again. The project requires a GPU/OpenGL environment; it is not designed to run as a headless CPU renderer.

### The scene appears black

Try selecting a different geometry, material, or post-processing effect from the GUI. Also check the Lighting section and increase light intensity if it has been reduced to zero.

### GUI controls do not respond

Make sure the application window has focus and click directly on the visible control. If the panel has been dragged near an edge, move it back into the window before interacting with sliders or combo boxes.

### Tests fail after dependency changes

Run `uv sync` to restore the environment from the project configuration, then run `uv run pytest` again.
