import numpy as np
import torch
import cv2

class AK_BlobTrack:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"defaultInput": True}),
                "cache_frames": ("INT", {
                    "default": 1, 
                    "min": 1, 
                    "max": 120, 
                    "step": 1, 
                    "display": "number"
                }),
                "diff_threshold": ("FLOAT", {
                    "default": 30.0, 
                    "min": 0.0, 
                    "max": 255.0, 
                    "step": 1.0, 
                    "display": "number"
                }),

                "min_threshold": ("INT", {"default": 50, "min": 0, "max": 255}),
                "max_threshold": ("INT", {"default": 220, "min": 1, "max": 255}),
                "threshold_step": ("INT", {"default": 10, "min": 1, "max": 50}),
                "filter_by_area": (["false", "true"], {"default": "true"}),
                "min_area": ("FLOAT", {"default": 25.0, "min": 0.0, "max": 1e6}),
                "max_area": ("FLOAT", {"default": 1e5, "min": 1.0, "max": 1e8}),
                "detect_bright_blobs": (["false", "true"], {"default": "false"}),

                "max_blobs": ("INT", {
                    "default": 10, 
                    "min": 1, 
                    "max": 100, 
                    "step": 1, 
                    "display": "number"
                }),

                "blob_outline_thickness": ("INT", {"default": 2, "min": 1, "max": 20}),
                "blob_outline_color": ("COLOR", {"default": "#ff0000"}),
                "blob_outline_alpha": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number"
                }),

                "line_thickness": ("INT", {"default": 2, "min": 1, "max": 20}),
                "line_color": ("COLOR", {"default": "#00ff00"}),
                "line_alpha": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "track_blobs"
    CATEGORY = "💜Akatz Nodes/Tracking"
    DESCRIPTION = """
    # AK Blob Track (SimpleBlobDetector)
    
    1. Uses frame differencing (with 'cache_frames') plus a threshold to isolate movement.
    2. Feeds the threshold image to OpenCV's SimpleBlobDetector.
    3. For each detected blob, draws:
       - An alpha-blended square outline in the composite.
       - A fully filled white rectangle for the blob in the mask.
    4. Also draws connecting lines between blob centers in composite.
       - If line_alpha > 0, the lines are drawn in the mask; otherwise, they are skipped.
    """

    ### COLOR PARSING UTILS ###
    def parse_hex_color(self, hex_str):
        h = hex_str.lstrip('#')
        if len(h) != 6:
            raise ValueError(f"Expected 6-digit hex color, got '{hex_str}'")
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
        return (r, g, b)

    def to_rgb_255(self, hex_str):
        r, g, b = self.parse_hex_color(hex_str)
        return (int(r*255), int(g*255), int(b*255))

    ### ALPHA DRAWING UTILS ###
    def draw_rect_alpha(self, base_img, top_left, bottom_right, color_rgb, alpha, thickness=1):
        if alpha <= 0:
            return
        if alpha >= 1.0:
            cv2.rectangle(base_img, top_left, bottom_right, color_rgb, thickness=thickness)
            return
        overlay = base_img.copy()
        cv2.rectangle(overlay, top_left, bottom_right, color_rgb, thickness=thickness)
        cv2.addWeighted(overlay, alpha, base_img, 1 - alpha, 0, dst=base_img)

    def draw_line_alpha(self, base_img, pt1, pt2, color_rgb, alpha, thickness=1):
        if alpha <= 0:
            return
        if alpha >= 1.0:
            cv2.line(base_img, pt1, pt2, color_rgb, thickness=thickness)
            return
        overlay = base_img.copy()
        cv2.line(overlay, pt1, pt2, color_rgb, thickness=thickness)
        cv2.addWeighted(overlay, alpha, base_img, 1 - alpha, 0, dst=base_img)

    ### BLOB DETECTOR SETUP ###
    def create_blob_detector(self,
                             min_threshold=50,
                             max_threshold=220,
                             threshold_step=10,
                             filter_by_area=True,
                             min_area=25.0,
                             max_area=1e5,
                             blob_color=0):
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = float(min_threshold)
        params.maxThreshold = float(max_threshold)
        params.thresholdStep = float(threshold_step)

        params.filterByColor = True
        params.blobColor = blob_color

        params.filterByArea = filter_by_area
        params.minArea = min_area
        params.maxArea = max_area

        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False

        return cv2.SimpleBlobDetector_create(params)

    def track_blobs(self,
                    image,
                    cache_frames=1,
                    diff_threshold=30.0,
                    min_threshold=50,
                    max_threshold=220,
                    threshold_step=10,
                    filter_by_area="true",
                    min_area=25.0,
                    max_area=1e5,
                    detect_bright_blobs="false",
                    max_blobs=10,
                    blob_outline_thickness=2,
                    blob_outline_color="#ff0000",
                    blob_outline_alpha=1.0,
                    line_thickness=2,
                    line_color="#00ff00",
                    line_alpha=1.0
                    ):

        # Convert input to np.uint8 [0..255]
        if isinstance(image, torch.Tensor):
            image_np = image.cpu().numpy()
        else:
            image_np = image
        if image_np.max() <= 1.0:
            image_np = (image_np * 255).astype(np.uint8)
        else:
            image_np = image_np.astype(np.uint8)

        batch_size, height, width, channels = image_np.shape
        composite_frames = np.zeros_like(image_np, dtype=np.uint8)
        mask_frames = np.zeros((batch_size, height, width), dtype=np.float32)

        # Convert booleans from input strings
        filter_area_bool = (filter_by_area.lower() == "true")
        bright_blobs_bool = (detect_bright_blobs.lower() == "true")
        blob_col_val = 255 if bright_blobs_bool else 0

        detector = self.create_blob_detector(
            min_threshold=min_threshold,
            max_threshold=max_threshold,
            threshold_step=threshold_step,
            filter_by_area=filter_area_bool,
            min_area=min_area,
            max_area=max_area,
            blob_color=blob_col_val
        )

        blob_rgb = self.to_rgb_255(blob_outline_color)
        line_rgb = self.to_rgb_255(line_color)

        def get_reference_frame(arr, i):
            start_i = max(i - cache_frames, 0)
            ref_frames = arr[start_i:i]
            if len(ref_frames) == 0:
                return arr[i]
            return np.mean(ref_frames, axis=0).astype(np.uint8)

        for i in range(batch_size):
            current_frame = image_np[i]
            ref_frame = get_reference_frame(image_np, i)
            diff_frame = cv2.absdiff(current_frame, ref_frame)

            gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, int(diff_threshold), 255, cv2.THRESH_BINARY)

            keypoints = detector.detect(thresh)
            keypoints = sorted(keypoints, key=lambda kp: kp.size, reverse=True)[:max_blobs]

            drawn_frame = current_frame.copy()
            mask_frame = np.zeros((height, width), dtype=np.uint8)
            centers = []

            for kp in keypoints:
                cx = int(round(kp.pt[0]))
                cy = int(round(kp.pt[1]))
                size_i = int(round(kp.size))
                half_w = size_i // 2
                top_left = (cx - half_w, cy - half_w)
                bottom_right = (cx + half_w, cy + half_w)

                # Draw outline on composite
                self.draw_rect_alpha(drawn_frame, top_left, bottom_right,
                                     blob_rgb, blob_outline_alpha,
                                     thickness=blob_outline_thickness)

                # Draw filled rectangle on mask
                cv2.rectangle(mask_frame, top_left, bottom_right, 255, thickness=-1)

                centers.append((cx, cy))

            # Draw lines connecting blob centers
            for idx in range(len(centers) - 1):
                pt1, pt2 = centers[idx], centers[idx+1]
                self.draw_line_alpha(drawn_frame, pt1, pt2,
                                     line_rgb, line_alpha,
                                     thickness=line_thickness)
                # Only draw lines in mask if line_alpha is non-zero
                if line_alpha > 0:
                    cv2.line(mask_frame, pt1, pt2, 255, thickness=line_thickness)

            composite_frames[i] = drawn_frame
            mask_frames[i] = mask_frame.astype(np.float32) / 255.0

        out_composite = torch.from_numpy(composite_frames.astype(np.float32)/255.0)
        out_mask = torch.from_numpy(mask_frames)
        return (out_composite, out_mask)
