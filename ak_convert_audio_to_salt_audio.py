
import torch
import io
import wave
import numpy as np
from collections.abc import Mapping

class AK_ConvertAudioToSaltAudio:
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
    FUNCTION = "convert_tensor_to_audio_bytes"
    DESCRIPTION = """
    # Converts a PyTorch tensor representing audio data into raw audio bytes in WAV format.

    Parameters:
    - audio: LazyAudioMap-like object containing the waveform and sample rate

    Returns:
    - audio_bytes: Raw audio bytes in WAV format
    """

    def convert_tensor_to_audio_bytes(self, audio, num_channels=2):
        """
        Converts a PyTorch tensor representing audio data into raw audio bytes in WAV format.
        
        Parameters:
        - audio: PyTorch tensor with shape (1, num_channels, num_samples) or (num_channels, num_samples)
        - num_channels: Number of audio channels (default: 2)
        
        Returns:
        - audio_bytes: Raw audio bytes in WAV format
        """
        audio_tensor = audio['waveform']
        sample_rate = audio['sample_rate']
        # Ensure the tensor is in the correct shape (num_channels, num_samples)
        if audio_tensor.dim() == 3:
            audio_tensor = audio_tensor.squeeze(0)
        
        # Convert tensor to numpy array with shape (num_samples, num_channels)
        audio_np = audio_tensor.transpose(0, 1).numpy()

        # Create a byte buffer to write the WAV file into
        byte_io = io.BytesIO()
        
        # Write the WAV file
        with wave.open(byte_io, 'wb') as wave_file:
            wave_file.setnchannels(num_channels)
            wave_file.setsampwidth(2)  # 2 bytes per sample (16-bit PCM)
            wave_file.setframerate(sample_rate)
            
            # Convert the numpy array to 16-bit PCM format
            audio_int16 = (audio_np * 32767.0).astype('int16')
            wave_file.writeframes(audio_int16.tobytes())
        
        # Get the byte content
        audio_bytes = byte_io.getvalue()
        
        return (audio_bytes,)