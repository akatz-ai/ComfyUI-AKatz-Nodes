import numpy as np
import copy
import cv2
import torch
import math

PI = math.pi

class AK_AudioreactiveDynamicDilationMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "normalized_amp": ("*", {"defaultInput": True}),
                "shape": (["circle","square"],),
                "max_radius": ("INT",{
                    "default": 25
                }),
                "min_radius": ("INT",{
                    "default": 0
                }),
                "quality_factor": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number",
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
    RETURN_TYPES = ("MASK",)
    FUNCTION = "dilate_mask_with_amplitude"
    DESCRIPTION = """
    # Dilate Mask dynamically based on Amplitude
    - masks: The mask to dilate
    - norm_amps: The normalized amplitude values
    - shape: The shape of the dilation
    - max_radius: The maximum radius of the dilation
    - min_radius: The minimum radius of the dilation
    - quality_factor: The quality factor of the dilation
    """
    
    def create_circular_kernel(self, radius):
        d = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x*x + y*y <= radius*radius
        kernel = np.zeros((d, d), dtype=np.uint8)
        kernel[mask] = 1
        return kernel

    def dilate_mask_with_amplitude(self, mask, normalized_amp, shape="circle", max_radius=25, min_radius=0, quality_factor=0.25):
        dup = copy.deepcopy(mask.cpu().numpy())
        
        # Convert normalize_amp into a float list from numpy array if it is not already a list
        if not isinstance(normalized_amp, list):
            normalized_amp = normalized_amp.tolist()

        epsilon = 1e-6
        if quality_factor < epsilon:
            shape = "square"

        for index, (mask_frame, amp) in enumerate(zip(dup, normalized_amp)):
            # Scale the amplitude to fluctuate between min_radius and max_radius
            radius = min_radius + amp * (max_radius - min_radius)

            if radius <= 0:
                continue

            s = abs(int(radius * quality_factor if shape == "circle" else radius))
            d = s * 2 + 1

            if shape == "circle":
                k = np.zeros((d, d), np.uint8)
                k = cv2.circle(k, (s, s), s, 1, -1)
            else:
                k = np.ones((d, d), np.uint8)

            iterations = int(1 / quality_factor if quality_factor >= epsilon else 1)

            if radius > 0:
                dilated_mask = cv2.dilate(mask_frame, k, iterations=iterations)
            else:
                dilated_mask = cv2.erode(mask_frame, k, iterations=iterations)

            dup[index] = dilated_mask
        
        return (torch.from_numpy(dup),)