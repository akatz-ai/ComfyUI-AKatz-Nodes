import numpy as np

class AK_FloatListToFlexFeature:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"forceInput": True}),  # 'forceInput' used for custom types like FEATURE
                "original_feature": ("FEATURE", {"forceInput": True}), # The original FEATURE object to combine with the float list for the output
            },
        }

    RETURN_TYPES = ("FEATURE",)  # Define the output as a FEATURE object
    FUNCTION = "convert_float_list_to_feature"
    CATEGORY = "💜Akatz Nodes/Utils"

    DESCRIPTION = """
    AK_FloatListToFlexFeature:
    This node converts a list of float values into a FEATURE type input.
    
    - original_feature: A custom Feature object with attributes:
      - original_feature.get_value_at_frame(i): Method that returns a float value for frame `i`.
      - original_feature.frame_count: The total number of frames in the feature.
    """

    def convert_float_list_to_feature(self, float_list, original_feature):
        """
        Convert the values from a list of floats to a FEATURE object.

        Args:
        - float_list: A list of floats.
        - original_feature: The Feature object which contains frame values.

        Returns:
        - original_feature: A FEATURE object with the same frame values as the float list.
        """
        
        # Convert the float list to a numpy array
        array = np.array(float_list)
        
        # Get frame count from the number of elements in the array
        frame_count = array.shape[0]
        
        original_feature.frame_count = frame_count
        original_feature.data = array
        
        # Return the feature as a tuple (since ComfyUI expects tuples)
        return (original_feature,)

