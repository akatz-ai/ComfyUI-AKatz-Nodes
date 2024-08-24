class AK_LagChop:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),  # Assuming ComfyUI has a type for lists of floats
                "lag_factor": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("FLOAT",)  # Assuming ComfyUI returns a list
    RETURN_NAMES = ("output_list",)
    FUNCTION = "lag_chop_node"
    DESCRIPTION = """
    # AK Lag Chop
    Apply a lag effect to a list of float values.
    - float_list: The input list of float values.
    - lag_factor: The factor by which the output lags behind the input (0 < lag_factor <= 1).
    """

    def lag_chop_node(self, float_list: list, lag_factor: float) -> tuple:
        """
        Apply a lag effect to a list of float values.

        Args:
        - float_list (list of float): The input list of float values.
        - lag_factor (float): The factor by which the output lags behind the input (0 < lag_factor <= 1).

        Returns:
        - tuple: A tuple containing the output list with lag applied to each value.
        """
        if not (0 < lag_factor <= 1):
            raise ValueError("Lag factor must be between 0 and 1, exclusive.")

        # Initialize the output list with the first value
        output_list = [float_list[0]]

        # Apply the lag effect to each subsequent value
        for i in range(1, len(float_list)):
            # Calculate the lagged value based on the previous output and the current input
            lagged_value = output_list[-1] + lag_factor * (float_list[i] - output_list[-1])
            output_list.append(lagged_value)

        return (output_list,)  # Return as a tuple
