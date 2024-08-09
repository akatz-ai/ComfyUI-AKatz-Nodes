import numpy as np
import torch

class AK_NormalizeMaskColor:
    def __init__(self):
            pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("FLOAT",{
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "round": 0.1, #The value representing the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                "red": ("INT",{
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "round": 0, #The value representing the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                "green": ("INT",{
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "round": 0, #The value representing the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                "blue": ("INT",{
                    "default": 255,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "round": 0, #The value representing the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
            },
        }

    CATEGORY = "💜Akatz Nodes"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "clamp_black_and_white_video_custom_color"
    DESCRIPTION = """
    # AK Normalize Mask Color
    Normalize the color of the mask to a specified color.
    - image: The input video tensor with shape (num_frames, H, W, C).
    - threshold: The threshold value for determining black pixels.
    - r: Red channel value (0-255) for the non-black pixels.
    - g: Green channel value (0-255) for the non-black pixels.
    - b: Blue channel value (0-255) for the non-black pixels.
    """
    
    def clamp_black_and_white_video_custom_color(self, image: torch.Tensor, threshold: float, red: int, green: int, blue: int) -> torch.Tensor:
        """
        Process a video tensor to clamp pixels close to black to pure black,
        and turn all other pixels to a specified color for each frame.

        Args:
        - image (torch.Tensor): The input video tensor with shape (num_frames, H, W, C).
        - threshold (float): The threshold value for determining black pixels.
        - r (int): Red channel value (0-255) for the non-black pixels.
        - g (int): Green channel value (0-255) for the non-black pixels.
        - b (int): Blue channel value (0-255) for the non-black pixels.

        Returns:
        - torch.Tensor: The processed video tensor with pixels clamped to black or the specified color.
        """
        # Ensure the video tensor is in the correct range [0, 1]
        image = image.clamp(0, 1)

        # Convert RGB values to the range [0, 1]
        color = torch.tensor([red / 255.0, green / 255.0, blue / 255.0], dtype=image.dtype, device=image.device)

        # Transpose the tensor to have channels first, for easier processing
        image = image.permute(0, 3, 1, 2)  # Shape: (num_frames, C, H, W)

        # Calculate the brightness of each pixel (assuming the video is in RGB format)
        brightness = image.mean(dim=1)  # Shape: (num_frames, H, W)

        # Create a mask for pixels that are close to black
        black_mask = brightness < threshold  # Shape: (num_frames, H, W)

        # Initialize the output video tensor with the specified color
        output = torch.ones_like(image)
        output[:, 0, :, :] = color[0]
        output[:, 1, :, :] = color[1]
        output[:, 2, :, :] = color[2]

        # Set black pixels to pure black in the output video
        output[:, :, :, :] = torch.where(black_mask[:, None, :, :], 0.0, output)

        # Permute the output back to the original shape (num_frames, H, W, C)
        output = output.permute(0, 2, 3, 1)

        return (output,)