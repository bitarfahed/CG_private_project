# Interactive Graphics Lab TODO

## 1. Documentation

- [x] Create initial PRD.
- [x] Create development plan.
- [x] Create phase-based TODO checklist.

## 2. Architecture

- [ ] Define the main application responsibilities.
- [ ] Decide how geometry, materials, lighting, animation, post-processing, and GUI code will be separated.
- [ ] Identify the minimal data structures needed for scene state and user-controlled parameters.

## 3. Procedural Geometry

- [ ] Add procedural generation for the planned primitive shapes.
- [ ] Ensure generated geometry includes the attributes needed for lighting and materials.
- [ ] Provide simple controls for switching between primitives.

## 4. Procedural Materials

- [ ] Add the initial procedural material set.
- [ ] Expose a small set of adjustable material parameters.
- [ ] Verify that each material is visually distinct.

## 5. Lighting

- [ ] Add controls for ambient, diffuse, and specular lighting behavior.
- [ ] Add Phong shading support.
- [ ] Evaluate whether multiple colored lights fit within the project timeline.

## 6. Renderer Integration

- [ ] Connect the scene state to the GPU/OpenGL render loop.
- [ ] Render selected geometry with the selected material and lighting configuration.
- [ ] Establish useful default camera and scene settings.

## 7. Animation

- [ ] Add object animation controls.
- [ ] Add light animation controls.
- [ ] Add animated material parameter controls.

## 8. Post Processing

- [ ] Add selectable post-processing effects.
- [ ] Make effect parameters simple to adjust where appropriate.
- [ ] Confirm that effects can be enabled and disabled interactively.

## 9. GUI

- [ ] Build controls for geometry selection.
- [ ] Build controls for material selection and parameters.
- [ ] Build controls for lighting, animation, and post-processing.
- [ ] Keep the interface compact and suitable for live experimentation.

## 10. Basic Tests

- [ ] Add tests for procedural geometry output where practical.
- [ ] Add tests for deterministic helper logic.
- [ ] Keep tests focused on stable non-visual behavior.

## 11. Polish

- [ ] Improve default scene appearance.
- [ ] Clean up naming, organization, and user-facing labels.
- [ ] Verify the application remains responsive during interaction.

## 12. Final Documentation

- [ ] Document how to run the completed application.
- [ ] Summarize implemented graphics topics.
- [ ] Note known limitations and possible future improvements.
