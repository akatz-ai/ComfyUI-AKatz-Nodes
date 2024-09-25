import torch

class AK_SplitImageBatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_batch": ("IMAGE",),  # The input image batch to be split
                "split_index": ("INT", {"default": 1, "min": 1}),  # The index at which to split the batch
                "split_batch_index": ("INT", {"default": 0, "min": 0, "max": 1}),  # Whether to return the first or second batch
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "split_image_batch"
    CATEGORY = "💜Akatz Nodes/Utils"
    DESCRIPTION = """
    # AK Split Image Batch
    This node splits an input image batch into two at a given index, and returns one of the partitions.
    - split_index: The index at which to split the image batch.
    - split_batch_index: 0 to return the first partition, 1 to return the second partition.
    """

    def split_image_batch(self, image_batch, split_index, split_batch_index):
        # Validate the split index to be within range
        batch_size = image_batch.shape[0]
        if split_index < 1 or split_index >= batch_size:
            raise ValueError(f"split_index must be between 1 and {batch_size - 1}.")
        
        # Split the image batch into two parts
        batch1 = image_batch[:split_index]  # First part up to split_index
        batch2 = image_batch[split_index:]  # Second part from split_index to the end
        
        # Select which batch to return based on split_batch_index (0 or 1)
        if split_batch_index == 0:
            return (batch1,)
        elif split_batch_index == 1:
            return (batch2,)
        else:
            raise ValueError("split_batch_index must be either 0 or 1.")