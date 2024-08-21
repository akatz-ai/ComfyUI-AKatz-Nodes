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
                "normalized_amp": ("NORMALIZED_AMPLITUDE",),
                "shape": (["circle","square"],),
                "max_radius": ("INT",{
                    "default": 25
                }),
                "min_radius": ("INT",{
                    "default": 0
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes"
    RETURN_TYPES = ("MASK",)
    FUNCTION = "dilate_mask_with_amplitude"
    DESCRIPTION = """
    # Dilate Mask dynamically based on Amplitude
    - masks: The mask to dilate
    - norm_amps: The normalized amplitude values
    - shape: The shape of the dilation
    - max_radius: The maximum radius of the dilation
    - min_radius: The minimum radius of the dilation
    """
    
    def create_circular_kernel(self, radius):
        d = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x*x + y*y <= radius*radius
        kernel = np.zeros((d, d), dtype=np.uint8)
        kernel[mask] = 1
        return kernel

    def dilate_mask_with_amplitude(self, mask, normalized_amp, shape="circle", max_radius=25, min_radius=0):
        dup = copy.deepcopy(mask.cpu().numpy())

        # Pre-compute circular kernels if shape is "circle"
        if shape == "circle":
            circular_kernels = [self.create_circular_kernel(r) for r in range(max_radius+1)]

        for index, (mask, amp) in enumerate(zip(dup, normalized_amp)):
            # Scale the amplitude to fluctuate between min_radius and max_radius
            current_radius = min_radius + amp * (max_radius - min_radius)

            if current_radius <= 0:
                continue

            if shape == "circle":
                k = circular_kernels[int(current_radius)]
            else:
                d = 2 * int(current_radius) + 1
                k = np.ones((d, d), np.uint8)

            dup[index] = cv2.dilate(mask, k, iterations=1)
        
        return (torch.from_numpy(dup),)