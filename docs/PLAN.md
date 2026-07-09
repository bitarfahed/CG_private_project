# Interactive Graphics Lab Development Plan

## 1. Documentation

Establish the product direction, scope, and roadmap before implementation begins. This phase defines what the project is intended to demonstrate and what should remain out of scope.

## 2. Architecture

Design a small, modular structure for geometry, materials, rendering, animation, post-processing, and GUI integration. The goal is to support incremental development without creating unnecessary framework overhead.

## 3. Procedural Geometry

Implement mathematical generation of core primitives: sphere, torus, plane, cylinder, and cone. This phase should focus on producing clean vertex data suitable for GPU rendering.

## 4. Procedural Materials

Add a compact material system for shader-driven patterns such as checker, stripes, marble, wood, clouds, lava, and noise-based effects. Materials should expose a small number of clear parameters for interaction.

## 5. Lighting

Introduce basic real-time lighting controls, including ambient, diffuse, specular, and Phong shading. If time permits, support multiple colored lights while keeping the interface simple.

## 6. Renderer Integration

Connect geometry, materials, lighting, and camera behavior into a working GPU/OpenGL render loop. This phase should produce the first cohesive interactive scene.

## 7. Animation

Add time-based controls for object transforms, light movement, and animated material parameters. Animation should be easy to enable, disable, and observe from the GUI.

## 8. Post Processing

Add framebuffer-based post-processing effects such as Gaussian blur, Sobel, sharpen, pixelate, gamma correction, and grayscale. Effects should be selectable and visually distinct.

## 9. GUI

Build the interactive desktop controls for selecting geometry, materials, lighting options, animation modes, and post-processing effects. The GUI should prioritize clarity and fast experimentation.

## 10. Basic Tests

Add lightweight tests for deterministic, non-visual logic such as procedural geometry generation and parameter validation. The goal is confidence without overbuilding a test suite for a short academic project.

## 11. Polish

Improve usability, default settings, visual consistency, error handling, and scene presentation. This phase should make the application feel coherent rather than like disconnected demonstrations.

## 12. Final Documentation

Update project documentation to reflect the completed implementation, supported features, limitations, and usage instructions. The final documentation should help reviewers understand both the application and the development choices.
