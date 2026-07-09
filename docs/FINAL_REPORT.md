# Interactive Graphics Lab Final Report

## 1. Introduction

Interactive Graphics Lab is a compact desktop application for demonstrating several Computer Graphics course topics in one interactive GPU-rendered scene. The project combines procedural geometry, procedural shader materials, Phong lighting, animation, post-processing, and GUI controls into a small application suitable for academic review.

The project uses a modern GPU/OpenGL rendering backend. It does not implement a CPU software rasterizer, manual triangle rasterization, manual Z-buffer, software framebuffer pipeline, or scanline renderer. The educational focus is on higher-level graphics techniques that are commonly built on top of the GPU pipeline.

## 2. Project Goals

The main goals were:

- Generate geometry procedurally rather than loading mesh assets.
- Demonstrate shader-based procedural materials.
- Implement standard Phong lighting concepts.
- Add simple real-time animation.
- Demonstrate framebuffer-based post-processing.
- Provide a compact GUI for interacting with the graphics modules.
- Keep the implementation realistic for a small university graphics project.

## 3. System Architecture

The application is organized as a Python package under `src/interactive_graphics_lab`. The major modules are separated by responsibility:

- `core`: application orchestration and minimal scene state
- `rendering`: ModernGL rendering and GPU mesh upload
- `geometry`: procedural mesh generation
- `materials`: procedural material definitions and shader logic
- `lighting`: ambient and point-light settings
- `animation`: frame-rate independent scene updates
- `postprocessing`: offscreen framebuffer and screen-space effects
- `ui`: ImGui control panel

The runtime flow is:

```text
Application loop
-> animation update
-> scene state
-> GPU scene render
-> offscreen framebuffer
-> post-processing pass
-> GUI overlay
-> screen
```

The scene layer is deliberately small. It contains one active mesh, one material, lighting settings, transform data, and fixed camera values. It is not a scene graph.

## 4. Rendering Backend Decision

The project uses ModernGL with `moderngl-window`. ModernGL provides direct access to modern OpenGL concepts from Python, while `moderngl-window` handles window and context creation.

This backend was chosen because it supports GPU rendering without hiding the rendering pipeline behind a full game engine. That makes it appropriate for a Computer Graphics course project where shader logic, vertex data, framebuffers, and render passes should remain visible in the implementation.

## 5. Procedural Geometry

The geometry module defines a reusable `Mesh` structure containing:

- vertex positions
- vertex normals
- UV coordinates
- triangle indices

The implemented primitives are:

- Plane
- Cube
- UV sphere
- Cylinder
- Cone
- Torus

All of these are generated mathematically. The project does not load OBJ, STL, GLTF, or other external mesh formats. The GUI can switch between the implemented primitives.

## 6. Procedural Materials

The material system defines CPU-side material parameters and a GLSL shader that computes procedural appearance. Implemented material types are:

- Solid Color
- Checker
- Stripes
- Gradient
- Marble
- Wood
- Noise / Clouds
- Lava / Energy

Materials provide the base surface color. The lighting shader then modifies that color using the Phong model. No image textures are loaded for the procedural material system.

## 7. Lighting / Phong Model

The lighting module supports ambient lighting and point lights. The shader computes:

- ambient contribution
- diffuse Lambert contribution
- specular Phong contribution

The renderer uploads camera position, light position, light color, light intensity, specular strength, shininess, and a normal matrix. Normals from the generated meshes are transformed correctly before lighting. The GUI exposes controls for one editable point light.

## 8. Animation

The animation system updates scene state using `delta_time`, not frame count. It currently animates:

- object rotation
- one moving point light
- procedural material time

Animation can be enabled or disabled in code and through the GUI. The renderer does not own animation logic; it only renders the current scene state.

## 9. Post Processing

The post-processing system renders the scene into an offscreen framebuffer with a color texture and depth buffer. A fullscreen quad then samples the color texture and applies the selected image-space shader.

Implemented effects are:

- None / passthrough
- Grayscale
- Pixelate
- Sobel edge detection

Framebuffer resources are recreated when the window size changes. The active effect can be selected from the GUI.

## 10. GUI and Interaction

The GUI uses ImGui with the pyglet backend. It is drawn as an overlay after the post-processing pass so that the scene can be post-processed while the controls remain readable.

The GUI exposes:

- active geometry
- active procedural material
- point light color
- point light position
- point light intensity
- animation enable/disable
- animation rotation speed
- active post-processing effect

The GUI only edits existing scene and renderer state. It does not implement graphics algorithms itself.

## 11. Testing Strategy

The test suite uses pytest and focuses on deterministic CPU-side behavior. It covers:

- procedural geometry mesh invariants
- invalid geometry parameters
- material registry behavior
- post-processing effect configuration
- default scene state
- animation updates and disabled animation behavior

The tests intentionally avoid:

- GUI automation
- OpenGL context creation
- shader compilation
- screenshots
- visual correctness checks
- performance measurements

This keeps the tests fast and reliable while still improving confidence in the project's algorithmic foundations.

## 12. Vibe Coding Workflow

The project was developed through a Vibe Coding / LLM-assisted workflow. Development was divided into focused prompts, each targeting one phase:

1. Documentation bootstrap
2. Architecture and backend decision
3. Procedural geometry
4. Procedural materials
5. Phong lighting
6. Renderer and scene integration
7. Animation
8. Post-processing
9. GUI integration
10. Basic tests
11. Polish and refactor
12. Final documentation

This approach encouraged incremental implementation, frequent verification, and clear boundaries between modules.

## 13. Challenges and Design Tradeoffs

One challenge was keeping the project small while still demonstrating several graphics topics. The solution was to use a single-object scene rather than building a full editor or scene graph.

Another tradeoff was GUI integration. ImGui was selected because it is lightweight and works well for demonstration controls. The GUI required careful coordinate handling so that rendered controls and mouse hitboxes matched correctly.

The project also balances shader complexity against readability. Procedural materials and post-processing effects are intentionally simple enough to be understandable in a course context.

## 14. Limitations

The project does not include:

- asset loading
- scene graph
- camera controls
- multiple object editing
- shadow mapping
- physically based rendering
- normal mapping
- image texture loading
- advanced material parameter editing
- visual regression tests

The test suite validates pure Python logic but does not verify rendered output.

## 15. Possible Future Improvements

Possible extensions include:

- camera orbit and zoom controls
- more post-processing effects
- additional material parameter controls in the GUI
- small scene presets
- Shadow Mapping
- Additional Procedural Materials
- Bezier/Spline Camera Paths
- Procedural Terrain Generation
- Multiple Dynamic Lights
- HDR/Bloom Pipeline
- Normal Mapping
- Subdivision Surfaces
- better separation of GLSL shader sources into dedicated files

## 16. Conclusion

Interactive Graphics Lab demonstrates a practical subset of Computer Graphics course topics in a cohesive desktop application. It uses GPU/OpenGL rendering to show procedural geometry, procedural materials, Phong lighting, animation, post-processing, and GUI-driven interaction without attempting to become a full engine.

The result is a compact, modular, and understandable graphics project suitable for academic presentation and further extension.
