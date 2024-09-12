import re

class AK_FloatListToDilateMaskSchedule:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "float_list": ("FLOAT", {"defaultInput": True}),
                "mask_colors": ("STRING", {
                    "default": '(255, 255, 0), (255, 0, 255)',
                    "multiline": True,
                }),
                "threshold": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "dilation_speed": ("INT", {
                    "default": 30,
                    "min": 1,
                    "step": 1,
                    "display": "number"
                }),
            },
        }

    CATEGORY = "💜Akatz Nodes/Utils"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "float_list_to_dilate_mask_schedule"
    DESCRIPTION = """
    # Float List to Dilate Mask Schedule
    - float_list: Input float list
    - mask_colors: Colors for the dilation masks in the format "(r, g, b), (r, g, b), ..."
    - threshold: The threshold of the dilation
    - dilation_speed: Speed of dilation in pixels per frame
    - This node transforms the input float list and parameters into a dilation mask schedule string.
    """

    def parse_colors(self, colors_str):
        pattern = r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*,?'
        matches = re.findall(pattern, colors_str)
        if not matches:
            return [(255, 255, 0), (255, 0, 255)]  # Default to yellow and magenta
        return [(int(r), int(g), int(b)) for r, g, b in matches]

    def float_list_to_dilate_mask_schedule(self, float_list, mask_colors, threshold, dilation_speed):
        colors = self.parse_colors(mask_colors)
        schedule = []
        current_color_index = 0
        dilating = False

        for index, value in enumerate(float_list):
            if value > threshold and not dilating:
                dilating = True
                color = colors[current_color_index % len(colors)]
                current_color_index += 1
                schedule.append(f"({index}, {dilation_speed}, ({color[0]}, {color[1]}, {color[2]})),")
            elif value <= threshold:
                dilating = False

        schedule_str = "".join(schedule)
        return (schedule_str,)

# Example usage
# float_list = inputs["0_float"]
# mask_colors = inputs["1_string"]
# threshold = inputs["2_float"]
# dilation_speed = inputs["3_int"]
# node = AK_FloatListToDilateMaskSchedule()
# output = node.float_list_to_dilate_mask_schedule(float_list, mask_colors, threshold, dilation_speed)[0]
# outputs[0] = output