import numpy as np

class AK_ListToNumpyFloatArray:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),  # Assuming ComfyUI has a type for lists of floats
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)  # Assuming ComfyUI has a type for NumPy arrays
    RETURN_NAMES = ("float_array",)
    FUNCTION = "list_to_numpy_float_array_node"
    DESCRIPTION = """
    # AK List to Numpy Float Array
    Convert a list of float values to a NumPy float array.
    - float_list: The input list of float values to be converted to a NumPy array.
    """

    def list_to_numpy_float_array_node(self, float_list: list) -> tuple:
        """
        Convert a list of float values to a NumPy float array.

        Args:
        - float_list (list of float): The input list of float values.

        Returns:
        - tuple: A tuple containing a NumPy array of float values.
        """
        # Convert the input list to a NumPy float array
        numpy_array = np.array(float_list, dtype=np.float64)
        
        return (numpy_array,)  # Return as a tuple

