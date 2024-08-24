"""
@author: akatz
@title: Akatz Custom Nodes
@nickname: Akatz Custom Nodes
@description: Custom node pack for nodes I use in my workflows. Includes Dilation mask nodes for animating subject masks.
"""

from .ak_animated_dilation_mask import AK_AnimatedDilationMaskLinear
from .ak_ipadapter_custom_weights import AK_IPAdapterCustomWeights
from .ak_normalize_mask_color import AK_NormalizeMaskColor
from .ak_audioreactive_dilation_mask import AK_AudioreactiveDilationMask
from .ak_audioreactive_dynamic_dilation_mask import AK_AudioreactiveDynamicDilationMask
from .ak_convert_audio_to_salt_audio import AK_ConvertAudioToSaltAudio
from .ak_convert_salt_audio_to_audio import AK_ConvertSaltAudioToAudio
from .ak_rescale_float_list import AK_RescaleFloatList
from .ak_list_to_numpy_float_array import AK_ListToNumpyFloatArray
from .ak_lag_chop import AK_LagChop
from .ak_binary_amplitude_gate import AK_BinaryAmplitudeGate
from .ak_adjust_list_size import AK_AdjustListSize
from .ak_video_speed_adjust import AK_VideoSpeedAdjust
from .ak_convert_list_to_float_list import AK_ConvertListToFloatList

NODE_CONFIG = {
  "AK_AnimatedDilationMaskLinear": {"class": AK_AnimatedDilationMaskLinear, "name": "AK Dilate Mask Linear"},
  "AK_IPAdapterCustomWeights": {"class": AK_IPAdapterCustomWeights, "name": "AK IPAdapter Custom Weights"},
  "AK_NormalizeMaskImage": {"class": AK_NormalizeMaskColor, "name": "AK Normalize Mask Color"},
  "AK_AudioreactiveDilationMask": {"class": AK_AudioreactiveDilationMask, "name": "AK Audioreactive Dilate Mask"},
  "AK_AudioreactiveDynamicDilationMask": {"class": AK_AudioreactiveDynamicDilationMask, "name": "AK Audioreactive Dynamic Dilate Mask"},
  "AK_ConvertAudioToSaltAudio": {"class": AK_ConvertAudioToSaltAudio, "name": "AK Convert Audio To Salt Audio"},
  "AK_ConvertSaltAudioToAudio": {"class": AK_ConvertSaltAudioToAudio, "name": "AK Convert Salt Audio To Audio"},
  "AK_RescaleFloatList": {"class": AK_RescaleFloatList, "name": "AK Rescale Float List"},
  "AK_ListToNumpyFloatArray": {"class": AK_ListToNumpyFloatArray, "name": "AK List To Numpy Float Array"},
  "AK_LagChop": {"class": AK_LagChop, "name": "AK Lag Chop"},
  "AK_BinaryAmplitudeGate": {"class": AK_BinaryAmplitudeGate, "name": "AK Binary Amplitude Gate"},
  "AK_AdjustListSize": {"class": AK_AdjustListSize, "name": "AK Adjust List Size"},
  "AK_VideoSpeedAdjust": {"class": AK_VideoSpeedAdjust, "name": "AK Video Speed Adjust"},
  "AK_ConvertListToFloatList": {"class": AK_ConvertListToFloatList, "name": "AK Convert List To Float List"}
}

def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]

ascii_art = """
AKATZ NODES
"""
print(ascii_art)