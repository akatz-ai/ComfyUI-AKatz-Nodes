class AK_ShrinkNumSequence:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_list": ("FLOAT", {"forceInput": True}),  # Expecting a list of floats
                "target_number": ("FLOAT", {"default": 1.0, "step": 0.01, "round": False, "display": "number"}),   # The float number to shrink
                "max_occurrences": ("INT", {"default": 2, "min": 1}),  # Maximum occurrences to keep
                "use_epsilon": ("BOOLEAN", {"default": True}),  # Boolean to use epsilon comparison
            },
        }

    RETURN_TYPES = ("FLOAT",)  # Output will be a list of floats
    FUNCTION = "shrink_num_sequence"
    CATEGORY = "💜Akatz Nodes/Utils"

    def shrink_num_sequence(self, float_list, target_number=1.0, max_occurrences=2, use_epsilon=False) -> tuple:
        """
        Shrink contiguous sequences of a specified float value in a list so that each sequence
        contains only the first max_occurrences values.

        Args:
        - float_list (list of float): The input list of float values.
        - target_number (float): The float number to shrink.
        - max_occurrences (int): Maximum number of target_number values to keep in each contiguous sequence.
        - use_epsilon (bool): Whether to use epsilon comparison for float equality.

        Returns:
        - tuple: A tuple containing the modified list with shrunk sequences of the specified float value.
        """
        # Define epsilon for comparison
        epsilon = 1e-7

        # Initialize variables to store the output and a counter for the target number values
        output_list = []
        count = 0

        # Iterate through the list
        for val in float_list:
            # Check if the current value matches the target number
            if (use_epsilon and abs(val - target_number) < epsilon) or (not use_epsilon and val == target_number):
                # If the current value matches the target number, check the count
                if count < max_occurrences:
                    output_list.append(val)
                else:
                    output_list.append(0.0)
                count += 1
            else:
                # Reset count when a non-target value is found
                output_list.append(val)
                count = 0

        return (output_list,)