import numpy as np
import copy
import cv2
import torch
import re
import math

class AK_DilateMaskLinearInfinite:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "dilation_schedule": ("STRING", {
                    "default": '(0, 30, (0, 255, 0)),',
                    "multiline": True,
                }),
                "quality_factor": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number",
                }),
                "timing_mode": (["Frame", "Percent"], { "default": "Frame" } ),
                "should_composite_subject": ("BOOLEAN", {
                    "default": False,
                }),
                "subject_mask_color": ("STRING", {
                    "default": "255, 0, 0",
                }),
                "initial_background_color": ("STRING", {
                    "default": "0, 0, 0",
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Mask"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "dilate_mask_linear_infinite"
    DESCRIPTION = """
    # Dilate Mask Linear Infinite
    - mask: Input mask or mask batch
    - dilation_schedule: Schedule for mask dilations in the format:
      (start_frame, dilation_speed, (r, g, b)),...
    - quality_factor: Quality factor for dilation (recommend between 0.25 and 0.15 for good balance between quality and speed)
    - use_percentage: Boolean to specify if the start_frame is in percentage of the total frames
    - should_composite_subject: Boolean to composite the subject mask over the final result
    - subject_mask_color: Color for the subject mask in the format "R, G, B"
    - initial_background_color: Color for the initial background in the format "R, G, B"
    """

    def parse_schedule(self, schedule_str, num_frames, timing_mode):
        pattern = r'\(\s*(\d*\.?\d*)\s*,\s*(\d+)\s*,\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\)\s*,?'
        matches = re.findall(pattern, schedule_str)
        
        if not matches:
            raise ValueError("No valid matches found in the provided schedule string.")
        
        schedule = []
        for match in matches:
            start_frame, dilation_speed, r, g, b = match
            start_frame = float(start_frame)
            if timing_mode == "Percent":
                start_frame = int(start_frame * num_frames)
            else:
                start_frame = int(start_frame)
            dilation_speed = int(dilation_speed)
            color = (int(r), int(g), int(b))
            schedule.append((start_frame, dilation_speed, color))
        
        return schedule

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

    def dilate_mask_linear_infinite(self, mask, dilation_schedule, quality_factor, timing_mode, should_composite_subject, subject_mask_color, initial_background_color):
        dup = copy.deepcopy(mask.cpu().numpy())
        num_frames, height, width = mask.shape[:3]
        schedule = self.parse_schedule(dilation_schedule, num_frames, timing_mode)
        all_dilated_masks = []

        for start_frame, dilation_speed, color in schedule:
            dilate_per_frame = dilation_speed
            dilated_masks = self.dilate_mask(dup, dilate_per_frame, start_frame, num_frames, width, height, quality_factor)
            all_dilated_masks.append((dilated_masks, color))

        initial_bg_color = tuple(map(int, initial_background_color.split(',')))
        result_images = np.zeros((num_frames, height, width, 3), dtype=np.uint8)
                    
        for index in range(num_frames):
            composite_image = np.zeros((height, width, 3), dtype=np.uint8)
            composite_image[:] = initial_bg_color  # Set initial background color
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


# mask = inputs["0_mask"]
# shape = inputs["1_string"]
# fps = inputs["2_int"]
# dilation_schedule = inputs["3_string"]
# quality_factor = inputs["4_float"]
# should_composite_subject = inputs["5_boolean"]
# subject_mask_color = inputs["6_string"]
# use_percentage = inputs["7_boolean"]
# node = AK_DilateMaskLinearInfinite()
# output = node.dilate_mask_linear_infinite(mask, dilation_schedule, quality_factor, should_composite_subject, subject_mask_color, use_percentage)

# outputs[0] = output
