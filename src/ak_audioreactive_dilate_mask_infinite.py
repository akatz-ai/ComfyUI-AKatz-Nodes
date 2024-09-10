import numpy as np
import copy
import cv2
import torch
import re
import math

PI = math.pi

class AK_AudioreactiveDilateMaskInfinite:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "normalized_amp": ("*", {"defaultInput": True}),
                "mask_colors": ("STRING", {
                    "default": '(255, 0, 0), (0, 255, 0), (0, 0, 255)',
                    "multiline": True,
                }),
                "threshold": ("FLOAT", {
                    "default": 0.5
                }),
                "dilation_speed": ("INT", {
                    "default": 30,
                    "min": 1,
                    "step": 1,
                    "display": "number"
                }),
                "quality_factor": ("FLOAT", {
                    "default": 0.15,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number",
                }),
                "should_composite_subject": ("BOOLEAN", {
                    "default": False,
                }),
                "subject_mask_color": ("STRING", {
                    "default": "255, 0, 0",
                }),
                "initial_background_color": ("STRING", {
                    "default": "0, 0, 0",
                }),
                "start_frame": ("INT", {
                    "default": 0,
                }),
                "end_frame": ("INT", {
                    "default": 0,
                }),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        if input_types["normalized_amp"] not in ("NORMALIZED_AMPLITUDE", "FLOAT"):
            return "normalized_amp must be an NORMALIZED_AMPLITUDE or FLOAT type"
        if input_types["mask"] != "MASK":
            return "mask must be a MASK type"
        return True

    CATEGORY = "💜Akatz Nodes/Mask"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "dilate_mask_with_amplitude"
    DESCRIPTION = """
    # Audioreactive Dilate Mask Infinite
    - mask: Input mask or mask batch
    - normalized_amp: The normalized amplitude values
    - mask_colors: Colors for the dilation masks in the format "(r, g, b), (r, g, b), ..."
    - threshold: The threshold of the dilation
    - dilation_speed: Speed of dilation in pixels per frame
    - quality_factor: Quality factor for dilation
    - should_composite_subject: Boolean to composite the subject mask over the final result
    - subject_mask_color: Color for the subject mask in the format "R, G, B"
    - initial_background_color: Color for the initial background in the format "R, G, B"
    - start_frame: Start frame for the dilation
    - end_frame: End frame for the dilation (0 for infinite)
    """

    def parse_colors(self, colors_str):
        pattern = r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*,?'
        matches = re.findall(pattern, colors_str)
        if not matches:
            return [(255, 255, 0), (255, 0, 255)]  # Default to yellow and magenta
        return [(int(r), int(g), int(b)) for r, g, b in matches]

    def dilate_mask(self, mask, dilate_per_frame, start_frame, num_frames, width, height, quality_factor):
        result_images = np.zeros((num_frames, height, width), dtype=np.uint8)
        radius = 0
        
        shape = "circle"
        epsilon = 1e-6
        if quality_factor < epsilon:
            shape = "square"

        for index in range(num_frames):
            if index < start_frame:
                continue

            frame_index = index
            frame_mask = mask[frame_index] if frame_index < mask.shape[0] else mask[-1]

            radius += dilate_per_frame

            s = abs(int(radius * quality_factor if shape == "circle" else radius))
            d = s * 2 + 1
            k = np.zeros((d, d), np.uint8)
            if shape == "circle":
                k = cv2.circle(k, (s, s), s, 1, -1)
            else:
                k += 1

            if radius > 0:
                dilated_mask = cv2.dilate(frame_mask, k, iterations=int(1 / quality_factor if shape == "circle" else 1))
            else:
                dilated_mask = cv2.erode(frame_mask, k, iterations=int(1 / quality_factor if shape == "circle" else 1))

            result_images[index] = dilated_mask

            # Check if the entire frame is covered by the mask
            if np.all(dilated_mask == 1):
                result_images[index:] = 1
                break

        return result_images

    def dilate_mask_with_amplitude(self, mask, normalized_amp, mask_colors, threshold, dilation_speed, quality_factor, should_composite_subject, subject_mask_color, initial_background_color, start_frame, end_frame):
        dup = copy.deepcopy(mask.cpu().numpy())
        num_frames, height, width = mask.shape[:3]
        colors = self.parse_colors(mask_colors)
        all_dilated_masks = []

        # Convert normalize_amp into a float list from numpy array if it is not already a list
        if not isinstance(normalized_amp, list):
            normalized_amp = normalized_amp.tolist()

        dilating = False  # Track whether we are in the dilating or decaying phase
        current_color_index = 0

        for index, amp in enumerate(normalized_amp):
            if index < start_frame:
                continue
            if end_frame > 0 and index >= end_frame:
                break
            if amp > threshold and not dilating:  # Start dilating if a beat is detected and not already dilating
                dilating = True
                start_frame = index
                color = colors[current_color_index % len(colors)]
                current_color_index += 1
                dilated_masks = self.dilate_mask(dup, dilation_speed, start_frame, num_frames, width, height, quality_factor)
                all_dilated_masks.append((dilated_masks, color))
            elif amp <= threshold:
                dilating = False

        initial_bg_color = tuple(map(int, initial_background_color.split(',')))
        result_images = np.zeros((num_frames, height, width, 3), dtype=np.uint8)
        result_images[:] = initial_bg_color  # Set initial background color

        for index in range(num_frames):
            composite_image = np.zeros((height, width, 3), dtype=np.uint8)
            composite_image[:] = initial_bg_color  # Ensure initial background color is set for each frame
            for dilated_masks, color in all_dilated_masks:
                mask_frame = dilated_masks[index]
                colored_mask = np.zeros((height, width, 3), dtype=np.uint8)
                colored_mask[mask_frame > 0] = color
                composite_image[mask_frame > 0] = color

            result_images[index] = composite_image
            
        if should_composite_subject:
            subject_color = tuple(map(int, subject_mask_color.split(',')))
            for index in range(num_frames):
                subject_mask = mask[index]
                result_images[index][subject_mask > 0] = subject_color

        result_images = result_images.astype(np.float32) / 255.0  # Normalize to [0, 1]
        result = torch.from_numpy(result_images).float()  # Ensure float type
        return (result,)