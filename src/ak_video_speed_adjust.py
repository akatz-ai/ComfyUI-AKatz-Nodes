import torch

class AK_VideoSpeedAdjust:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_batch": ("IMAGE",),
                "speed_schedule": ("FLOAT", {"forceInput": True}),
                "fps": ("INT", {"default": 30, "min": 1}),
            },
        }

    CATEGORY = "💜Akatz Nodes/Image"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "adjust_speed"
    DESCRIPTION = """
    # AK Speed Adjust
    Adjust the speed of the video dynamically based on the speed schedule.
    - image_batch: The input batch of images with shape (B, H, W, C).
    - speed_schedule: A list of floats where each value represents the speed at that frame.
    - fps: The frames per second of the original video.
    """
    
    def adjust_speed(self, image_batch: torch.Tensor, speed_schedule: list, fps: int) -> torch.Tensor:
        """
        Adjust the speed of the video based on the speed schedule.

        Args:
        - image_batch (torch.Tensor): Input image batch with shape (B, H, W, C).
        - speed_schedule (list of float): List of speed values for each frame.
        - fps (int): Frames per second of the original video.

        Returns:
        - torch.Tensor: The new image batch with speed adjustments applied.
        """
        B, H, W, C = image_batch.shape
        
        # If speed_schedule is shorter than the image batch, pad it with the last value
        if len(speed_schedule) < B:
            speed_schedule += [speed_schedule[-1]] * (B - len(speed_schedule))
        
        assert len(speed_schedule) == B, "Speed schedule length must match the number of frames in the batch."

        # Calculate time per frame in the original video
        time_per_frame = 1.0 / fps

        # Initialize progress and progress_list
        progress = 0.0
        progress_list = []
        
        # Calculate progress values for each frame in the output
        for speed_val in speed_schedule:
            progress_list.append(progress)
            progress += time_per_frame * speed_val
        
        # Map progress values to the original frame indices
        frame_indices = []
        for progress_time in progress_list:
            index = int(progress_time // time_per_frame) % B
            frame_indices.append(index)
        
        # Gather the frames from the original batch based on the calculated indices
        output_batch = image_batch[frame_indices]

        return (output_batch,)