import numpy as np

class AK_ConvertListToFloatList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_list": ("*",),  # Assuming ComfyUI can provide a list, NumPy array, or other types of lists
            },
        }
        
    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)  # Output as a Python list of floats
    FUNCTION = "convert_to_float_array_node"
    DESCRIPTION = """
    # AK Convert to Float Array
    Convert any input list type (NumPy array, Python integer list, Python float list) into a Python float array.
    - input_list: The input list or array to be converted to a Python float array.
    """

    def convert_to_float_array_node(self, **kwargs) -> tuple:
        """
        Convert any input list type to a Python float array.

        Args:
        - input_list: The input list or array to be converted.

        Returns:
        - tuple: A tuple containing the converted Python float array.
        """
        
        input_list = kwargs["input_list"]
        
        # Convert input to a NumPy array for uniform processing
        if isinstance(input_list, np.ndarray):
            # If it's already a NumPy array, just convert dtype
            float_array = input_list.astype(np.float64)
        else:
            # If it's not a NumPy array, first convert to NumPy array then change dtype
            float_array = np.array(input_list, dtype=np.float64)

        # Convert the NumPy array to a Python list of floats
        float_list = float_array.tolist()

        return (float_list,)  # Return as a tuple

