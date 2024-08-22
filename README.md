# AKatz Nodes

### AK Dilate Mask Linear

Dilates a mask in a linear animated fashion given a mask batch.
- mask: MASK, input a mask batch
- shape: "circle" or "square", "circle" is the most accurate and should be used for final renders. "square" is fast to calculate and should be used for testing the workflow.
- dilate_per_frame: INT, how much the mask should be dilated per frame.
- delay: INT, number of frames to wait before starting dilation.

### AK Audioreactive Dynamic Dilation Mask

[Node guide available here](https://cyber-damselfly-b6c.notion.site/AK-Audioreactive-Dynamic-Dilation-Mask-Node-815e086d428f46e0ad1da8b73f3fa38f))

Dynamically dilates a mask based on audio amplitude, ideal for audio-reactive visualizations.

mask: Input mask to be dilated.
normalized_amp: Normalized amplitude (0-1) controlling the dilation.
shape: "circle" or "square" to define the dilation shape.
max_radius: Maximum radius for dilation (upper limit).
min_radius: Minimum radius for dilation (lower limit).

### AK Normalize Mask Color

Normalize the color of the mask to a specified color.
- image: The input image tensor.
- threshold: The threshold value for determining black pixels.
- r: Red channel value (0-255) for the non-black pixels.
- g: Green channel value (0-255) for the non-black pixels.
- b: Blue channel value (0-255) for the non-black pixels.

### AK IPAdapter Custom Weights

[Node guide available here](https://cyber-damselfly-b6c.notion.site/AK-Custom-Weights-Node-1ee37dfbe1e54921acf587231968e94e)

Used to provide custom timings for crossfading multiple images using just two IPAdapters.
Text input should be a string of weights in the form: "(weight, start_frame, duration, interpolation_function),..."
E.g. "(1.0, 0, 24, linear), (0.5, 24, 12, ease_in), (0.0, 48, 24, ease_out), ..."
A default timing of "ease_in_out" is used if no interpolation function is specified.
- weights: The weights and timings to be applied to the images
- default_timing: The default easing function to be used for transitions
- frames: The number of frames in the output
- image: The image batch to be crossfaded by the weights
