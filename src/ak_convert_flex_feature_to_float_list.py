
class AK_FlexFeatureToFloatList:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "feature": ("FEATURE", {"forceInput": True}),  # 'forceInput' used for custom types like FEATURE
            },
        }

    RETURN_TYPES = ("FLOAT",)  # Define the output as a list of floats
    FUNCTION = "convert_feature_to_float_list"
    CATEGORY = "💜Akatz Nodes/Utils"

    DESCRIPTION = """
    AK_FlexFeatureToFloatList:
    This node converts a FEATURE type input into a list of float values, one per frame.
    
    - feature: A custom Feature object with attributes:
      - feature.get_value_at_frame(i): Method that returns a float value for frame `i`.
      - feature.frame_count: The total number of frames in the feature.
    """

    def convert_feature_to_float_list(self, feature):
        """
        Convert the values from a Feature object to a list of floats.

        Args:
        - feature: The Feature object which contains frame values.

        Returns:
        - tuple: A tuple containing a list of floats, where each float is the value
                 extracted from the feature for each frame.
        """
        # Initialize an empty list to store float values
        float_list = []

        # Iterate over each frame in the feature and extract the normalized value
        for i in range(feature.frame_count):
            value = feature.get_value_at_frame(i)
            float_list.append(value)

        # Return the list as a tuple (since ComfyUI expects tuples)
        return (float_list,)

