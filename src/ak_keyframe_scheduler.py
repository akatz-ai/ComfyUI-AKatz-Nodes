from ..modules.easing import easing_functions, KeyframeScheduler

# Credit to https://github.com/get-salt-AI/SaltAI_AudioViz/tree/main for the keyframe scheduler code

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
      
WILDCARD = AnyType("*")

class AK_KeyframeScheduler:
    @classmethod
    def INPUT_TYPES(cls):
        easing_funcs = list(easing_functions.keys())
        easing_funcs.insert(0, "None")
        return {
            "required": {
                "keyframe_schedule": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "easing_mode": (easing_funcs, )
            },
            "optional": {
                "end_frame": ("INT", {"min": 0}),
                "ndigits": ("INT", {"min": 1, "max": 12, "default": 5}),
                "a": (WILDCARD, {}),
                "b": (WILDCARD, {})
            }
        }

    RETURN_TYPES = ("LIST", )
    RETURN_NAMES = ("schedule_list", )

    FUNCTION = "keyframe_schedule"
    CATEGORY = f"💜Akatz Nodes/Utils"

    def keyframe_schedule(self, keyframe_schedule, easing_mode, end_frame=0, ndigits=2, a=None, b=None):
        if a and not isinstance(a, (int, float, bool, list)):
            raise ValueError("`a` is not a valid int, float, boolean, or schedule_list")
        if b and not isinstance(b, (int, float, bool, list)):
            raise ValueError("`b` is not a valid int, float, or boolean, or schedule_list")
        
        custom_vars = {}
        if a:
            custom_vars['a'] = a
        if b:
            custom_vars['b'] = b
        
        scheduler = KeyframeScheduler(end_frame=end_frame, custom_vars=custom_vars)
        schedule = scheduler.generate_schedule(keyframe_schedule, easing_mode=easing_mode, ndigits=ndigits)
        return (schedule, )