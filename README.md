# AKatz Nodes

### AK Dilate Mask Linear

Dilates a mask in a linear animated fashion given a mask batch.
- mask: MASK, input a mask batch
- shape: "circle" or "square", "circle" is the most accurate and should be used for final renders. "square" is fast to calculate and should be used for testing the workflow.
- dilate_per_frame: INT, how much the mask should be dilated per frame.
- delay: INT, number of frames to wait before starting dilation.

### AK Normalize Mask Color

Normalize the color of the mask to a specified color.
- image: The input image tensor.
- threshold: The threshold value for determining black pixels.
- r: Red channel value (0-255) for the non-black pixels.
- g: Green channel value (0-255) for the non-black pixels.
- b: Blue channel value (0-255) for the non-black pixels.

### AK IPAdapter Custom Weights

Used to provide custom timings for crossfading multiple images using just two IPAdapters.
Text input should be a string of weights in the form: "(weight, start_frame, duration, interpolation_function),..."
E.g. "(1.0, 0, 24, linear), (0.5, 24, 12, ease_in), (0.0, 48, 24, ease_out), ..."
A default timing of "ease_in_out" is used if no interpolation function is specified.
- weights: The weights and timings to be applied to the images
- default_timing: The default easing function to be used for transitions
- frames: The number of frames in the output
- image: The image batch to be crossfaded by the weights