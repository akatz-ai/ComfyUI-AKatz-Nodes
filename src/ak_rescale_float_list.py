import numpy as np

class AK_RescaleFloatList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),  # Assuming ComfyUI has a type for lists of floats
                "new_min": ("FLOAT", {
                    "default": 0.0,
                    "min": -1e10,
                    "max": 1e10,
                    "step": 0.001,
                    "round": 0.0001,
                    "display": "number"
                }),
                "new_max": ("FLOAT", {
                    "default": 1.0,
                    "min": -1e10,
                    "max": 1e10,
                    "step": 0.001,
                    "round": 0.0001,
                    "display": "number"
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("output_list",)
    FUNCTION = "rescale_values_node"
    DESCRIPTION = """
    # AK Rescale Float List
    Rescale a list of float values from an original range to a new range.
    - float_list: The input list of float values to be rescaled.
    - orig_min: The minimum value of the original range.
    - orig_max: The maximum value of the original range.
    - new_min: The minimum value of the new range.
    - new_max: The maximum value of the new range.
    """

    def rescale_values_node(self, float_list: list, new_min: float, new_max: float) -> tuple:
        """
        Rescale a list of float values from an original range to a new range.

        Args:
        - float_list (list of float): The input list of float values to be rescaled.
        - orig_min (float): The minimum value of the original range.
        - orig_max (float): The maximum value of the original range.
        - new_min (float): The minimum value of the new range.
        - new_max (float): The maximum value of the new range.

        Returns:
        - tuple: A tuple containing a list of float values rescaled to the new range.
        """
        # Convert the input list to a NumPy array for vectorized operations
        float_array = np.array(float_list)
        
        # get original min and max
        orig_min = float_array.min()
        orig_max = float_array.max()

        # Check if the original range is valid
        if orig_max == orig_min:
            raise ValueError("Original min and max values must be different.")

        # Calculate the scale factor
        scale = (new_max - new_min) / (orig_max - orig_min)

        # Rescale the values
        rescaled_array = new_min + (float_array - orig_min) * scale

        return (rescaled_array.tolist(),)  # Return as a tuple

