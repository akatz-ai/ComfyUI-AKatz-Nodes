import torch

class AK_ScheduledBinaryComparison:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "comparison_schedule": ("LIST",),
            },
            "optional": {
                "epsilon_schedule": ("LIST", {}),
                "use_epsilon": ("BOOLEAN", {"default": True})
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)

    FUNCTION = "binary_threshold"
    CATEGORY = f"💜Akatz Nodes/Image"

    def binary_threshold(self, images, comparison_schedule, epsilon_schedule=[0.1], use_epsilon=True):
        batch_size = images.shape[0]

        if len(comparison_schedule) < batch_size:
            last_val = comparison_schedule[-1]
            comparison_schedule.extend([last_val] * (batch_size - len(comparison_schedule)))
        comparison_schedule = comparison_schedule[:batch_size]

        thresholds_tensor = torch.tensor(comparison_schedule, dtype=images.dtype).view(batch_size, 1, 1, 1)
        
        if use_epsilon:
            if epsilon_schedule is None:
                epsilon_schedule = [0.1] * batch_size
            if len(epsilon_schedule) < batch_size:
                last_eps = epsilon_schedule[-1]
                epsilon_schedule.extend([last_eps] * (batch_size - len(epsilon_schedule)))
            epsilon_schedule = epsilon_schedule[:batch_size]
            epsilon_tensor = torch.tensor(epsilon_schedule, dtype=images.dtype).view(batch_size, 1, 1, 1)
            
            condition_met = ((images == thresholds_tensor) |
                             (torch.abs(images - thresholds_tensor) <= epsilon_tensor))
        else:
            condition_met = images >= thresholds_tensor

        thresholded_images = torch.where(condition_met, torch.tensor(1.0, dtype=images.dtype), torch.tensor(0.0, dtype=images.dtype))

        return (thresholded_images, )