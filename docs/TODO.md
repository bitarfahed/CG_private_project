# Interactive Graphics Lab TODO

## 1. Documentation

- [x] Create initial PRD.
- [x] Create development plan.
- [x] Create phase-based TODO checklist.

## 2. Architecture

- [x] Define the main application responsibilities.
- [x] Decide how geometry, materials, lighting, animation, post-processing, and GUI code will be separated.
- [x] Identify the minimal data structures needed for scene state and user-controlled parameters.

## 3. Procedural Geometry

- [x] Add procedural generation for the planned primitive shapes.
- [x] Ensure generated geometry includes the attributes needed for lighting and materials.
- [x] Provide simple controls for switching between primitives.

## 4. Procedural Materials

- [x] Add the initial procedural material set.
- [x] Expose material selection through the GUI.
- [x] Verify that each material is visually distinct.

## 5. Lighting

- [x] Add controls for point-light color, position, and intensity.
- [x] Add Phong shading support.
- [x] Add multiple colored point lights in the default scene.

## 6. Renderer Integration

- [x] Connect the scene state to the GPU/OpenGL render loop.
- [x] Render selected geometry with the selected material and lighting configuration.
- [x] Establish useful default camera and scene settings.

## 7. Animation

- [x] Add object animation.
- [x] Add light animation.
- [x] Add animated material time updates.

## 8. Post Processing

- [x] Add selectable post-processing effects.
- [x] Keep effect parameters simple and code-driven.
- [x] Confirm that effects can be enabled and disabled interactively.

## 9. GUI

- [x] Build controls for geometry selection.
- [x] Build controls for material selection.
- [x] Build controls for lighting, animation, and post-processing.
- [x] Keep the interface compact and suitable for live experimentation.

## 10. Basic Tests

- [x] Add tests for procedural geometry output where practical.
- [x] Add tests for deterministic helper logic.
- [x] Keep tests focused on stable non-visual behavior.

## 11. Polish

- [x] Improve default scene appearance.
- [x] Clean up naming, organization, and user-facing labels.
- [x] Verify the application remains responsive during interaction.

## 12. Final Documentation

- [x] Document how to run the completed application.
- [x] Summarize implemented graphics topics.
- [x] Note known limitations and possible future improvements.
