# Prompt Log

This project was developed through an incremental Vibe Coding workflow. Each prompt focused on one bounded task so that the codebase could grow from documentation to a complete interactive graphics demo without attempting a large rewrite at any stage.

## 1. Repository Documentation Bootstrap

- Purpose: Establish the project vision, scope, and development plan before implementation.
- Expected output: Initial documentation files for product requirements, plan, and TODO checklist.
- Actual role: Created the documentation foundation and explicitly defined the project as a GPU/OpenGL graphics application rather than a CPU software rasterizer.

## 2. Architecture Skeleton + GPU Rendering Backend Decision

- Purpose: Create the initial package structure and select the rendering backend.
- Expected output: Minimal Python package, renderer entry point, and architecture documentation.
- Actual role: Established the `interactive_graphics_lab` package, selected ModernGL with `moderngl-window`, and created a minimal GPU window that cleared the screen.

## 3. Procedural Geometry

- Purpose: Implement mathematical mesh generation.
- Expected output: Reusable mesh representation and generators for core primitives.
- Actual role: Added `Mesh`, `MeshGenerator`, and procedural generators for plane, cube, sphere, cylinder, cone, and torus. Integrated one generated mesh into the renderer for display.

## 4. Procedural Materials

- Purpose: Add shader-based procedural appearance.
- Expected output: Material abstraction, material defaults, and GLSL procedural material logic.
- Actual role: Added CPU-side material definitions and a material shader supporting solid, checker, stripes, gradient, marble, wood, clouds, and lava/energy materials. Later preview corrections improved the default marble appearance and sphere proportions.

## 5. Lighting / Phong Shader Pipeline

- Purpose: Add course-level lighting concepts to the shader pipeline.
- Expected output: Ambient, diffuse, and specular lighting using the Phong reflection model.
- Actual role: Added ambient and point-light data structures, camera position uniforms, normal transformation, and shader-side Phong lighting that modifies procedural material color.

## 6. Renderer / Scene Integration

- Purpose: Stabilize the flow between geometry, material, lighting, scene state, and the renderer.
- Expected output: Minimal scene abstraction and cleaner renderer responsibilities.
- Actual role: Introduced a lightweight `Scene` containing one mesh, one material, one lighting setup, transform values, and fixed camera data. The renderer became responsible for GPU drawing rather than procedural content creation.

## 7. Animation System

- Purpose: Add frame-rate independent real-time updates.
- Expected output: A simple animation layer that updates scene data before rendering.
- Actual role: Added `AnimationSystem`, which updates object rotation, light movement, and procedural material time from `delta_time`.

## 8. Post Processing Pipeline

- Purpose: Demonstrate framebuffer-based screen-space effects.
- Expected output: Render-to-texture pass, fullscreen quad, and post-processing shaders.
- Actual role: Added an offscreen framebuffer, color texture, depth renderbuffer, fullscreen quad, and effects for passthrough, grayscale, pixelate, and Sobel edge detection.

## 9. GUI Integration

- Purpose: Expose the main graphics modules through a compact interactive control panel.
- Expected output: GUI controls for geometry, material, lighting, animation, and post-processing.
- Actual role: Added ImGui integration with controls for implemented primitives, materials, one editable point light, animation enable/speed, and post-processing effect selection. A later fix corrected GUI coordinate and hitbox mapping.

## 10. Basic Tests

- Purpose: Add deterministic tests for pure Python logic.
- Expected output: Small pytest suite without GUI or OpenGL context requirements.
- Actual role: Added tests for procedural geometry invariants, material registry behavior, post-processing settings, scene defaults, and animation updates.

## 11. Polish / Refactor Pass

- Purpose: Improve maintainability and robustness without adding features.
- Expected output: Small cleanup pass, resource management improvements, and stable behavior.
- Actual role: Added idempotent resource release paths, clearer runtime errors for released resources or invalid scene meshes, and minor GUI spacing polish.

## 12. README + Prompt Log + Final Report

- Purpose: Prepare final documentation for academic submission and GitHub presentation.
- Expected output: README, prompt log, and final report based on the current repository state.
- Actual role: Documents the completed project accurately, including implemented features, design decisions, workflow, limitations, and future improvements.
