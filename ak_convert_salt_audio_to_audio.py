
import torch
import io
import wave
import numpy as np
from collections.abc import Mapping

class AK_ConvertSaltAudioToAudio:
    def __init__(self):
            pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
            },
        }

    CATEGORY = "💜Akatz Nodes"
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "convert_audio_bytes_to_lazy_audio_map"
    DESCRIPTION = """
    # Converts raw audio bytes (in WAV format) into a LazyAudioMap-like format.

    Parameters:
    - audio_bytes: Raw audio bytes in WAV format

    Returns:
    - lazy_audio_map: A LazyAudioMap-like object containing the waveform and sample rate
    """

    def convert_audio_bytes_to_lazy_audio_map(self, audio):
        """
        Converts raw audio bytes (in WAV format) into a LazyAudioMap-like format.
        
        Parameters:
        - audio: Raw audio bytes in WAV format
        
        Returns:
        - lazy_audio_map: A LazyAudioMap-like object containing the waveform and sample rate
        """
        # Open the audio bytes as a WAV file
        byte_io = io.BytesIO(audio)
        with wave.open(byte_io, 'rb') as wave_file:
            num_channels = wave_file.getnchannels()
            sample_rate = wave_file.getframerate()
            num_frames = wave_file.getnframes()
            
            # Read the frames as raw bytes
            audio_frames = wave_file.readframes(num_frames)
            
            # Convert the bytes to a numpy array
            audio_np = np.frombuffer(audio_frames, dtype='int16').reshape(-1, num_channels)
            
            # Normalize the audio to the range [-1, 1] and convert to a PyTorch tensor
            audio_tensor = torch.tensor(audio_np, dtype=torch.float32) / 32767.0
            
            # Reshape to (num_channels, num_samples) and add the batch dimension
            audio_tensor = audio_tensor.transpose(0, 1).unsqueeze(0)
        
        # Create a LazyAudioMap-like object
        class LazyAudioMap(Mapping):
            def __init__(self, waveform, sample_rate):
                self._dict = {
                    'waveform': waveform,
                    'sample_rate': sample_rate
                }
            
            def __getitem__(self, key):
                return self._dict[key]
            
            def __iter__(self):
                return iter(self._dict)
            
            def __len__(self):
                return len(self._dict)
        
        return (LazyAudioMap(audio_tensor, sample_rate),)