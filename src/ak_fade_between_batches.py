import torch
import torch.nn.functional as F

class AK_FadeBetweenBatches:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),  # First image batch
                "image2": ("IMAGE",),  # Second image batch
                "overlap_frames": ("INT", {"default": 10, "min": 1}),  # Number of frames to overlap/fade
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "fade_batches"
    CATEGORY = "💜Akatz Nodes/Utils"
    DESCRIPTION = """
    # AK Fade Between Batches
    This node takes two image batches and blends them together by transitioning 
    with overlapping frames. The output is a single image batch where:
    - image1 starts,
    - a number of overlap frames fade between image1 and image2,
    - image2 finishes.
    """

    def fade_batches(self, image1, image2, overlap_frames):
        # Check if image1 or image2 is None or empty
        if image1 is None or image1.numel() == 0:
            if image2 is None or image2.numel() == 0:
                raise ValueError("Both image1 and image2 are None or empty.")
            return (image2,)
        
        if image2 is None or image2.numel() == 0:
            return (image1,)

        # Ensure image2 has the same height, width, and channels as image1
        if image1.shape[1:] != image2.shape[1:]:
            # Resize image2 to match image1 dimensions (using bilinear interpolation)
            image2 = F.interpolate(image2.permute(0, 3, 1, 2), size=image1.shape[1:3], mode='bilinear', align_corners=False)
            image2 = image2.permute(0, 2, 3, 1)  # Re-permute to get back to [B, H, W, C]

        batch_size1 = image1.shape[0]
        batch_size2 = image2.shape[0]
        
        # Calculate the number of frames outside of the overlap
        non_overlap1 = batch_size1 - overlap_frames
        non_overlap2 = batch_size2 - overlap_frames
        
        if non_overlap1 < 0 or non_overlap2 < 0:
            raise ValueError("Overlap frames exceed the batch sizes of the input images.")
        
        # Create the transition frames by fading between image1 and image2
        transition_frames = []
        for i in range(overlap_frames):
            alpha_step = 1 / ((overlap_frames + 2) - 1)  # Alpha will go from 0 to 1
            alpha = alpha_step * (i + 1)
            fade_frame = (1 - alpha) * image1[non_overlap1 + i] + alpha * image2[i]
            transition_frames.append(fade_frame)
        
        # Stack the frames into a single tensor (batch)
        result_batch = torch.cat(
            (image1[:non_overlap1],  # First part from image1
             torch.stack(transition_frames),  # Transition frames
             image2[overlap_frames:]),  # Remaining frames from image2
            dim=0
        )
        return (result_batch,)

# image1 = inputs['0_image']
# image2 = inputs['1_image']
# overlap_frames = inputs['2_int']

# instance = AK_FadeBetweenBatches()
# outputs[0] = instance.fade_batches(image1, image2, overlap_frames)[0]