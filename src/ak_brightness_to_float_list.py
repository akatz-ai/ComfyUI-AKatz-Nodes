import numpy as np
import torch

class AK_BrightnessToFloatList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"defaultInput": True}),
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "brightness_to_float_list"
    DESCRIPTION = """
    # Brightness to Float List
    - image: Input image (tensor object)
    - This node calculates the average pixel brightness for each frame and normalizes it between 0.0 (black) and 1.0 (white).
    """

    def brightness_to_float_list(self, image):
        # Convert the image batch to a numpy array if it's a tensor
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()

        # Ensure the pixel values are in the range [0, 255]
        if image.max() <= 1.0:
            image = image * 255.0

        # Calculate the average brightness for each frame
        avg_brightness = np.mean(image, axis=(1, 2, 3)) / 255.0  # Normalize to [0, 1]

        # Convert the average brightness to a list of floats
        brightness_list = avg_brightness.tolist()

        return (brightness_list,)

# Example usage
# image = inputs["0_image"]
# node = AK_BrightnessToFloatList()
# output = node.brightness_to_float_list(image)[0]
# outputs[0] = output