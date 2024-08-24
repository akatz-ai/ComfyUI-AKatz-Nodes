import numpy as np
import copy
import cv2
import torch

class AK_AnimatedDilationMaskLinear:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
                "shape": (["circle", "square"],),
                "dilate_per_frame": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 9999,
                    "step": 1,
                }),
                "delay": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 99999999,
                    "step": 1,
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Mask Dilation"
    RETURN_TYPES = ("MASK",)
    FUNCTION = "dilate_mask_linear"
    DESCRIPTION = """
    # Animated Dilate Mask Linear
    - mask: Input mask or mask batch
    - shape: "circle" or "square", "circle" is most accurate to mask shape, "square" is fast to compute for testing purposes
    - step: how much should the mask be dilated per frame
    - delay: delay in frames before starting dilation
    """
    
    def dilate_mask_linear(self, mask, shape, dilate_per_frame, delay):
        
        dup = copy.deepcopy(mask.cpu().numpy())
        rads = []
        radius = 0

        for index, frame_mask in enumerate(dup):

            if index < delay:
                dup[index] = frame_mask
                continue

            radius += dilate_per_frame

            rads.append(radius)

            if index > 0 and np.all(dup[index - 1] == 1):
                s = abs(int(1000))
                d = s * 2 + 1
                k = np.zeros((d, d), np.uint8)
                k += 1
                dup[index] = cv2.dilate(frame_mask, k, iterations=1)
                continue
        
            s = abs(int(radius))
            d = s * 2 + 1
            k = np.zeros((d, d), np.uint8)
            if shape == "circle":
                k = cv2.circle(k, (s,s), s, 1, -1)
            else:
                k += 1
            
            if radius > 0:
                dup[index] = cv2.dilate(frame_mask, k, iterations=1)
            else:
                dup[index] = cv2.erode(frame_mask, k, iterations=1)
        
        result = torch.from_numpy(dup)
        return (result,)