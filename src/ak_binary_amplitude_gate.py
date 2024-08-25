class AK_BinaryAmplitudeGate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),  # Assuming ComfyUI has a type for lists of floats
                "min_value": ("FLOAT", {
                    "default": 0.0,
                    "min": -1e10,
                    "max": 1e10,
                    "step": 0.001,
                    "round": 0.001,
                    "display": "number"
                }),
                "max_value": ("FLOAT", {
                    "default": 1.0,
                    "min": -1e10,
                    "max": 1e10,
                    "step": 0.001,
                    "round": 0.001,
                    "display": "number"
                }),
                "threshold": ("FLOAT", {
                    "default": 0.5,
                    "min": -1e10,
                    "max": 1e10,
                    "step": 0.001,
                    "round": 0.001,
                    "display": "number"
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Audio"
    RETURN_TYPES = ("FLOAT",)  # Assuming ComfyUI returns a list
    RETURN_NAME = "output_list"
    FUNCTION = "binary_amplitude_gate_node"
    DESCRIPTION = """
    # AK Binary Amplitude Gate
    Apply a binary amplitude gate to a list of float values.
    - float_list: The input list of float values.
    - min_value: The value to set if the float is below the threshold.
    - max_value: The value to set if the float is equal to or above the threshold.
    - threshold: The threshold to determine the gating.
    """

    def binary_amplitude_gate_node(self, float_list: list, min_value: float, max_value: float, threshold: float) -> tuple:
        """
        Apply a binary amplitude gate to a list of float values.

        Args:
        - float_list (list of float): The input list of float values.
        - min_value (float): The value to set if the float is below the threshold.
        - max_value (float): The value to set if the float is equal to or above the threshold.
        - threshold (float): The threshold to determine the gating.

        Returns:
        - tuple: A tuple containing the output list with values gated to min_value or max_value.
        """
        # Apply the binary amplitude gate to the input list
        output_list = [float(min_value) if val < threshold else float(max_value) for val in float_list]
        
        return (output_list,)  # Return as a tuple
