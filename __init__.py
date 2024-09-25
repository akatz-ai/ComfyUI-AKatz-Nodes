"""
@author: akatz
@title: Akatz Custom Nodes
@nickname: Akatz Custom Nodes
@description: Custom node pack for nodes I use in my workflows. 
Includes Dilation mask nodes for animating subject masks, audio processing nodes, image processing nodes, utility nodes, etc.
"""

from .src.ak_animated_dilation_mask import AK_AnimatedDilationMaskLinear
from .src.ak_ipadapter_custom_weights import AK_IPAdapterCustomWeights
from .src.ak_normalize_image_color import AK_NormalizeImageColor
from .src.ak_audioreactive_dilation_mask import AK_AudioreactiveDilationMask
from .src.ak_audioreactive_dynamic_dilation_mask import AK_AudioreactiveDynamicDilationMask
from .src.ak_convert_audio_to_salt_audio import AK_ConvertAudioToSaltAudio
from .src.ak_convert_salt_audio_to_audio import AK_ConvertSaltAudioToAudio
from .src.ak_rescale_float_list import AK_RescaleFloatList
from .src.ak_list_to_numpy_float_array import AK_ListToNumpyFloatArray
from .src.ak_lag_chop import AK_LagChop
from .src.ak_binary_amplitude_gate import AK_BinaryAmplitudeGate
from .src.ak_adjust_list_size import AK_AdjustListSize
from .src.ak_video_speed_adjust import AK_VideoSpeedAdjust
from .src.ak_convert_list_to_float_list import AK_ConvertListToFloatList
from .src.ak_shrink_num_sequence import AK_ShrinkNumSequence
from .src.ak_dilate_mask_linear_infinite import AK_DilateMaskLinearInfinite
from .src.ak_audio_framesync_schedule import AK_AudioFramesyncSchedule
from .src.ak_audioreactive_dilate_mask_infinite import AK_AudioreactiveDilateMaskInfinite
from .src.ak_keyframe_scheduler import AK_KeyframeScheduler
from .src.ak_scheduled_binary_comparison import AK_ScheduledBinaryComparison
from .src.ak_brightness_to_float_list import AK_BrightnessToFloatList
from .src.ak_float_list_to_dilate_mask_schedule import AK_FloatListToDilateMaskSchedule
from .src.ak_fade_between_batches import AK_FadeBetweenBatches
from .src.ak_split_image_batch import AK_SplitImageBatch
from .src.ak_convert_flex_feature_to_float_list import AK_FlexFeatureToFloatList
from .src.ak_convert_float_list_to_flex_feature import AK_FloatListToFlexFeature

NAME_POSTFIX = " | Akatz"

NODE_CONFIG = {
  "AK_AnimatedDilationMaskLinear": {"class": AK_AnimatedDilationMaskLinear, "name": "Dilate Mask Linear"},
  "AK_IPAdapterCustomWeights": {"class": AK_IPAdapterCustomWeights, "name": "IPAdapter Custom Weights"},
  "AK_NormalizeMaskImage": {"class": AK_NormalizeImageColor, "name": "Normalize Image Color"},
  "AK_AudioreactiveDilationMask": {"class": AK_AudioreactiveDilationMask, "name": "Audioreactive Dilate Mask"},
  "AK_AudioreactiveDynamicDilationMask": {"class": AK_AudioreactiveDynamicDilationMask, "name": "Audioreactive Dynamic Dilate Mask"},
  "AK_ConvertAudioToSaltAudio": {"class": AK_ConvertAudioToSaltAudio, "name": "Convert Audio To Salt Audio"},
  "AK_ConvertSaltAudioToAudio": {"class": AK_ConvertSaltAudioToAudio, "name": "Convert Salt Audio To Audio"},
  "AK_RescaleFloatList": {"class": AK_RescaleFloatList, "name": "Rescale Float List"},
  "AK_ListToNumpyFloatArray": {"class": AK_ListToNumpyFloatArray, "name": "List To Numpy Float Array"},
  "AK_LagChop": {"class": AK_LagChop, "name": "Lag Chop"},
  "AK_BinaryAmplitudeGate": {"class": AK_BinaryAmplitudeGate, "name": "Binary Amplitude Gate"},
  "AK_AdjustListSize": {"class": AK_AdjustListSize, "name": "Adjust List Size"},
  "AK_VideoSpeedAdjust": {"class": AK_VideoSpeedAdjust, "name": "Video Speed Adjust"},
  "AK_ConvertListToFloatList": {"class": AK_ConvertListToFloatList, "name": "Convert List To Float List"},
  "AK_ShrinkNumSequence": {"class": AK_ShrinkNumSequence, "name": "Shrink Num Sequence"},
  "AK_DilateMaskLinearInfinite": {"class": AK_DilateMaskLinearInfinite, "name": "Dilate Mask Linear Infinite"},
  "AK_AudioFramesyncSchedule": {"class": AK_AudioFramesyncSchedule, "name": "Schedule Audio Framesync"},
  "AK_AudioreactiveDilateMaskInfinite": {"class": AK_AudioreactiveDilateMaskInfinite, "name": "Audioreactive Dilate Mask Infinite"},
  "AK_KeyframeScheduler": {"class": AK_KeyframeScheduler, "name": "Keyframe Scheduler"},
  "AK_ScheduledBinaryComparison": {"class": AK_ScheduledBinaryComparison, "name": "Scheduled Binary Comparison"},
  "AK_BrightnessToFloatList": {"class": AK_BrightnessToFloatList, "name": "Brightness To Float List"},
  "AK_FloatListToDilateMaskSchedule": {"class": AK_FloatListToDilateMaskSchedule, "name": "Float List To Dilate Mask Schedule"},
  "AK_FadeBetweenBatches": {"class": AK_FadeBetweenBatches, "name": "Fade Between Batches"},
  "AK_SplitImageBatch": {"class": AK_SplitImageBatch, "name": "Split Image Batch"},
  "AK_FlexFeatureToFloatList": {"class": AK_FlexFeatureToFloatList, "name": "Flex Feature To Float List"},
  "AK_FloatListToFlexFeature": {"class": AK_FloatListToFlexFeature, "name": "Float List To Flex Feature"},
}

def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__) + NAME_POSTFIX

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]

ascii_art = """
💜 AKATZ NODES 💜
"""
print(ascii_art)