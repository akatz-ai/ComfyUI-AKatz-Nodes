import torch
import numpy as np

class AK_MakeDepthmapSeamless:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "depthmap_batch": ("IMAGE",),  # Batch of images (depth maps)
            },
        }

    RETURN_TYPES = ("IMAGE",)  # Output is a batch of images (seamless depth maps)
    CATEGORY = "💜Akatz Nodes/Utils"
    FUNCTION = "make_depthmap_seamless"
    DESCRIPTION = """
    # AK Make Depthmap Seamless
    Adjusts depth maps in the batch to become seamless by fitting and removing a plane using least-squares.
    - depthmap_batch: The input depth maps to be adjusted to become seamless.
    """

    def make_depthmap_seamless(self, depthmap_batch):
        """
        Adjusts depth maps in the batch to become seamless by fitting and removing a plane using least-squares.

        Args:
            depthmap_batch (torch.Tensor): Batch of depth maps, shape [B, H, W, C]

        Returns:
            torch.Tensor: The batch of adjusted depth maps with seamless edges, shape [B, H, W, C]
        """
        # Convert PyTorch tensor to NumPy array for processing
        depthmap_np = depthmap_batch.cpu().numpy()  # [B, H, W, C]

        # Handle single image input
        if depthmap_np.ndim == 3:
            depthmap_np = np.expand_dims(depthmap_np, axis=0)  # Shape [1, H, W, C]

        # Compute the average depth map across all frames
        avg_depthmap_np = np.mean(depthmap_np, axis=0)  # Shape [H, W, C]

        # If it's 3 channels, average them into one channel
        if avg_depthmap_np.shape[-1] == 3:
            avg_depthmap_gray_np = np.mean(avg_depthmap_np, axis=-1)  # Shape [H, W]
        else:
            avg_depthmap_gray_np = avg_depthmap_np.squeeze(-1)  # Shape [H, W]

        # Fit plane to the average depth map
        plane = self.fit_plane_least_squares(avg_depthmap_gray_np)

        # Process each image in the batch using the same plane correction
        for i in range(depthmap_np.shape[0]):
            single_depthmap_np = depthmap_np[i]

            # If it's 3 channels, average them into one channel
            if single_depthmap_np.shape[-1] == 3:
                single_depthmap_gray_np = np.mean(single_depthmap_np, axis=-1)  # Shape [H, W]
            else:
                single_depthmap_gray_np = single_depthmap_np.squeeze(-1)  # Shape [H, W]

            # Subtract the plane from the depth map
            depthmap_seamless_np = single_depthmap_gray_np - plane

            # Normalize across the entire batch for consistency
            depthmap_seamless_np = (depthmap_seamless_np - depthmap_seamless_np.min()) / (
                    (depthmap_seamless_np.max() - depthmap_seamless_np.min()) or 1)

            # Ensure it's 3-channel again before inserting back into batch
            depthmap_seamless_np = np.stack([depthmap_seamless_np] * 3, axis=-1)  # Shape [H, W, 3]

            # Replace in batch
            depthmap_np[i] = depthmap_seamless_np

        # Convert back to PyTorch tensor
        depthmap_seamless = torch.from_numpy(depthmap_np).to(depthmap_batch.device).type_as(depthmap_batch)

        return (depthmap_seamless,)

    def fit_plane_least_squares(self, D):
        """
        Fits a plane to the depth map D using least squares.

        Args:
            D (numpy.ndarray): The input depth map as a 2D NumPy array.

        Returns:
            numpy.ndarray: The plane fitted to the depth map.
        """
        H, W = D.shape
        x = np.arange(W)
        y = np.arange(H)
        X, Y = np.meshgrid(x, y)
        Z = D

        # Flatten the arrays for linear regression
        X_flat = X.flatten()
        Y_flat = Y.flatten()
        Z_flat = Z.flatten()

        # Design matrix for plane fitting
        A = np.c_[X_flat, Y_flat, np.ones_like(X_flat)]

        # Perform least squares fitting
        C, _, _, _ = np.linalg.lstsq(A, Z_flat, rcond=None)

        # Construct the plane from coefficients
        plane = (C[0] * X + C[1] * Y + C[2])

        return plane
