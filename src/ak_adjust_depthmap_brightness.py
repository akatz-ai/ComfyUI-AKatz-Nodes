import torch
import numpy as np

class AK_AdjustDepthmapBrightness:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "depthmap_batch": ("IMAGE",),  # Expecting a tensor in [B, H, W, C] shape
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust_brightness_for_loop"
    CATEGORY = "💜Akatz Nodes/Utils"
    DESCRIPTION = """
    Adjusts the brightness of each frame in a depth map video batch to match the brightness of the first frame.
    - depthmap_batch: Batch of depth maps, shape [B, H, W, C].
    """

    def adjust_brightness_for_loop(self, depthmap_batch):
        """
        Adjusts the brightness of each frame in a depth map batch to match the brightness of the first frame.

        Args:
            depthmap_batch (torch.Tensor): Batch of depth maps, shape [B, H, W, C]

        Returns:
            torch.Tensor: The batch of adjusted depth maps, shape [B, H, W, C]
        """
        # Convert to numpy for processing
        depthmap_np = depthmap_batch.cpu().numpy().copy()

        # Handle single image input by adding a batch dimension
        if depthmap_np.ndim == 3:
            depthmap_np = np.expand_dims(depthmap_np, axis=0)

        num_frames = depthmap_np.shape[0]
        first_frame_np = depthmap_np[0]

        # Calculate average brightness for the first frame
        if first_frame_np.shape[-1] == 3:
            first_frame_gray_np = np.mean(first_frame_np, axis=-1)
        else:
            first_frame_gray_np = first_frame_np.squeeze(-1)
        first_frame_avg_brightness = first_frame_gray_np.mean()

        # Process each frame
        for i in range(num_frames):
            frame_np = depthmap_np[i]
            if frame_np.shape[-1] == 3:
                frame_gray_np = np.mean(frame_np, axis=-1)
            else:
                frame_gray_np = frame_np.squeeze(-1)
            frame_avg_brightness = frame_gray_np.mean()
            brightness_diff = first_frame_avg_brightness - frame_avg_brightness

            # Adjust the frame's brightness
            frame_adjusted_np = frame_gray_np + brightness_diff
            frame_adjusted_np = np.clip(frame_adjusted_np, 0, 1)
            frame_adjusted_np = np.stack([frame_adjusted_np] * 3, axis=-1)

            depthmap_np[i] = frame_adjusted_np

        # Remove batch dimension if it was a single image
        if depthmap_np.shape[0] == 1:
            depthmap_np = depthmap_np[0]

        # Convert back to PyTorch tensor
        depthmap_adjusted = torch.from_numpy(depthmap_np).to(depthmap_batch.device).type_as(depthmap_batch)

        return (depthmap_adjusted,)
