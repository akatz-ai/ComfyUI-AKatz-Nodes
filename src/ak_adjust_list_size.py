class AK_AdjustListSize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),  # Assuming ComfyUI has a type for lists of floats
                "batch_size": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 10000,
                    "step": 1,
                    "round": 1,
                    "display": "number"
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)  # Assuming ComfyUI returns a list
    RETURN_NAMES = ("output_list",)
    FUNCTION = "adjust_list_size_node"
    DESCRIPTION = """
    # AK Adjust List Size
    Adjust the size of a list of floats to match the specified batch size.
    - float_list: The input list of float values.
    - batch_size: The desired batch size for the output list.
    """

    def adjust_list_size_node(self, float_list: list, batch_size: int) -> tuple:
        """
        Adjust the size of a list of floats to match the specified batch size.

        Args:
        - float_list (list of float): The input list of float values.
        - batch_size (int): The desired batch size for the output list.

        Returns:
        - tuple: A tuple containing the adjusted list, either padded or trimmed to match the batch size.
        """
        current_length = len(float_list)
        
        # If the current length is less than the batch size, pad the list with the last value
        if current_length < batch_size:
            padding_value = float_list[-1] if float_list else 0.0  # Use last value or 0 if the list is empty
            float_list.extend([padding_value] * (batch_size - current_length))
        # If the current length is greater than the batch size, trim the list from the end
        elif current_length > batch_size:
            float_list = float_list[:batch_size]

        return (float_list,)  # Return as a tuple
