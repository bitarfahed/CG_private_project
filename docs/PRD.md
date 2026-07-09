# Interactive Graphics Lab PRD

## Project Vision

Interactive Graphics Lab is a desktop application for exploring core Computer Graphics topics in one cohesive, interactive environment. The application should let users switch between procedural objects, materials, lighting setups, animations, and post-processing effects while seeing the results immediately in a rendered scene.

The project is designed for incremental development through a Vibe Coding workflow. Each stage should add a focused graphics capability while preserving a clean, understandable codebase suitable for a small academic project.

## Educational Goals

- Demonstrate how geometry can be generated mathematically instead of loaded from asset files.
- Show how procedural materials can be created from coordinates, patterns, and noise.
- Provide interactive examples of common lighting components such as ambient, diffuse, specular, and Phong shading.
- Illustrate animation of objects, lights, and material parameters.
- Demonstrate post-processing effects applied after scene rendering.
- Encourage modular graphics programming practices that separate geometry, materials, rendering, animation, and user interface concerns.

## Scope

The application will focus on a compact but polished set of graphics demonstrations:

- Procedural geometry: sphere, torus, plane, cylinder, and cone.
- Procedural materials: checker, stripes, marble, wood, clouds, lava, and noise-based patterns.
- Lighting: ambient, diffuse, specular, Phong shading, and multiple colored lights if practical.
- Animation: object motion, light motion, and animated procedural material parameters.
- Post processing: Gaussian blur, Sobel, sharpen, pixelate, gamma correction, and grayscale.
- Interactive GUI controls for choosing geometry, materials, lighting settings, animation options, and post-processing effects.

The expected implementation size should remain realistic for approximately two days of focused development work.

## Out of Scope

- CPU software rasterization.
- Manual triangle rasterization.
- Manual Z-buffer implementation.
- Custom CPU framebuffer rendering pipeline.
- OBJ or external mesh loading for the core geometry demonstrations.
- Complex scene editors or full asset pipelines.
- Advanced physically based rendering.
- Networked or web-based deployment.
- Production-grade modeling, animation, or material authoring tools.

## Rendering Direction

This project uses a modern GPU/OpenGL rendering backend, with ModernGL or an equivalent solution as the expected default. The educational focus is on graphics techniques, algorithms, shaders, interaction, and visual experimentation rather than rebuilding a software rasterizer.

## Target User

The primary target user is a Computer Graphics student, instructor, or reviewer who wants to inspect and interact with visual demonstrations of course topics. The application should be approachable enough for classroom demonstration while remaining structured enough to show thoughtful graphics engineering.

## Main Application Workflow

1. Launch the desktop application.
2. View a rendered scene containing the currently selected procedural object.
3. Select a geometry type from the GUI.
4. Choose a procedural material and adjust its visible parameters.
5. Modify lighting settings such as color, intensity, position, and shading mode.
6. Enable or disable animation for objects, lights, or materials.
7. Apply a post-processing effect and compare the result interactively.
8. Iterate between settings to explore how each graphics topic affects the final image.

## High-Level Features

- Real-time GPU-rendered scene viewport.
- Procedural mesh generation for several common primitives.
- Procedural material library driven by shader-friendly parameters.
- Configurable lighting model with clear visual feedback.
- Simple animation system for time-based demonstrations.
- Post-processing pass system for image-space effects.
- Desktop GUI for interactive experimentation.
- Organized project structure that supports incremental additions.

## Non-Functional Goals

### Modularity

The project should separate major concerns such as geometry generation, material definitions, rendering, animation, post-processing, and GUI controls. Each topic should be understandable in isolation.

### Maintainability

The implementation should favor small, focused modules and clear data flow. Features should be added in a way that avoids large, tightly coupled systems.

### Readability

Code and documentation should be written for students and reviewers. Naming should be explicit, behavior should be discoverable, and complex graphics concepts should be kept approachable.

### Extensibility

The architecture should make it practical to add new primitives, materials, lights, animations, and post-processing effects without rewriting the rest of the application.

### Performance

The application should remain responsive for the planned feature set by relying on GPU/OpenGL rendering for real-time visual output.
