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

NODE_CONFIG = {
  "AK_AnimatedDilationMaskLinear": {"class": AK_AnimatedDilationMaskLinear, "name": "AK Dilate Mask Linear"},
  "AK_IPAdapterCustomWeights": {"class": AK_IPAdapterCustomWeights, "name": "AK IPAdapter Custom Weights"},
  "AK_NormalizeMaskImage": {"class": AK_NormalizeMaskColor, "name": "AK Normalize Mask Color"},
  "AK_AudioreactiveDilationMask": {"class": AK_AudioreactiveDilationMask, "name": "AK Audioreactive Dilate Mask"},
  "AK_AudioreactiveDynamicDilationMask": {"class": AK_AudioreactiveDynamicDilationMask, "name": "AK Audioreactive Dynamic Dilate Mask"},
  "AK_ConvertAudioToSaltAudio": {"class": AK_ConvertAudioToSaltAudio, "name": "AK Convert Audio To Salt Audio"},
  "AK_ConvertSaltAudioToAudio": {"class": AK_ConvertSaltAudioToAudio, "name": "AK Convert Salt Audio To Audio"}
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