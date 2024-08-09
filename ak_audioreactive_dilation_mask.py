import numpy as np
import copy
import cv2
import torch
import math

PI = math.pi

class AK_AudioreactiveDilationMask:
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
                "attack": ("FLOAT",{
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": False,
                    "display": "number"}),
                "decay": ("FLOAT",{
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": False,
                    "display": "number"}),
                "attack_function": (["linear","ease-in","ease-out","ease-in-out"],),
                "decay_function": (["linear","ease-in","ease-out","ease-in-out"],),
            },
        }

    CATEGORY = "💜Akatz Nodes"
    RETURN_TYPES = ("MASK",)
    FUNCTION = "dilate_mask_with_amplitude"
    DESCRIPTION = """
    # Dilate Mask with Amplitude
    - masks: The mask to dilate
    - norm_amps: The normalized amplitude values
    - shape: The shape of the dilation
    - max_radius: The maximum radius of the dilation
    - attack: The attack of the dilation
    - decay: The decay of the dilation
    - attack_function: The attack easing function
    - decay_function: The decay easing function
    """
    
    def create_circular_kernel(self, radius):
        d = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x*x + y*y <= radius*radius
        kernel = np.zeros((d, d), dtype=np.uint8)
        kernel[mask] = 1
        return kernel

    def ease_in_sin(self, t):
        return 1 - math.cos((t * PI) / 2)

    def ease_out_sin(self, t):
        return math.sin((t * PI) / 2)

    def ease_in_out_sin(self, t):
        return -(math.cos(PI * t) - 1) / 2

    def linear(self, t):
        return t

    def apply_easing(self, value, max_value, func):
        t = value / max_value if max_value != 0 else 1 # normalize value
        if t >= 1:
            return 1
        if func == "ease-in":
            return self.ease_in_sin(t)
        elif func == "ease-out":
            return self.ease_out_sin(t)
        elif func == "ease-in-out":
            return self.ease_in_out_sin(t)
        else:  # linear
            return self.linear(t)

    def dilate_mask_with_amplitude(self, mask, normalized_amp, shape="circle", max_radius=25, attack=1.0, decay=1.0, attack_function="linear", decay_function="linear"):
        dup = copy.deepcopy(mask.cpu().numpy())
        current_radius = 0
        radius_progress = 0

        # Pre-compute circular kernels if shape is "circle"
        if shape == "circle":
            circular_kernels = [self.create_circular_kernel(r) for r in range(max_radius+1)]

        dilating = False  # Track whether we are in the dilating or decaying phase
        
        for index, (mask, amp) in enumerate(zip(dup, normalized_amp)):
            if amp > 0 and not dilating:  # Start dilating if a beat is detected and not already dilating
                dilating = True
            
            if dilating:
                radius_progress = self.apply_easing(radius_progress + attack, 1.0, attack_function)
                if radius_progress >= 1.0:
                    dilating = False  # Start decaying after reaching max_radius
                    radius_progress = 1.0
            else:
                radius_progress = self.apply_easing(radius_progress - decay, 1.0, decay_function)
                if radius_progress <= 0.0:
                    radius_progress = 0.0
            
            current_radius = radius_progress * max_radius
            
            if current_radius <= 0:
                continue
            
            if shape == "circle":
                k = circular_kernels[int(current_radius)]
            else:
                d = 2 * int(current_radius) + 1
                k = np.ones((d, d), np.uint8)
            
            dup[index] = cv2.dilate(mask, k, iterations=1)
        
        return (torch.from_numpy(dup),)