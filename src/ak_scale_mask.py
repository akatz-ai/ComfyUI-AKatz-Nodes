import torch

class ScaleMaskNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),  # Expecting a torch.Tensor input with shape [B, H, W]
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MASK",)  # Output is a scaled torch.Tensor with the same shape as the input
    FUNCTION = "scale_mask"
    CATEGORY = "💜Akatz Nodes/Mask"

    def scale_mask(self, mask, scale_factor):
        """
        Scales the input MASK tensor by the provided scale_factor.

        Args:
        - mask (torch.Tensor): The input mask tensor of shape [B, H, W].
        - scale_factor (float): A value between 0.0 and 1.0.

        Returns:
        - tuple: A tuple containing the scaled mask tensor.
        """
        # Ensure the tensor and scale_factor are valid
        if not torch.is_tensor(mask):
            raise ValueError("Input 'mask' must be a torch.Tensor.")
        if mask.dim() not in (3, 4):
            raise ValueError("Input 'mask' must have 3 or 4 dimensions ([B, H, W] or [B, C, H, W]).")

        # Apply scaling
        scaled_mask = mask * scale_factor
        return (scaled_mask,)  # Return as a tuple


# Exporting the class for ComfyUI
NODE_CLASS_MAPPINGS = {
    "Scale Mask Node": ScaleMaskNode,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
