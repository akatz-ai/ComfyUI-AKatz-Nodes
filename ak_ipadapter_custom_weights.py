import math
import torch

class AK_IPAdapterCustomWeights:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "weights": ("STRING", {"default": '(1.0),', "multiline": True }),
            "default_timing": (["linear", "ease_in_out", "ease_in", "ease_out"], { "default": "ease_in_out" } ),
            "frames": ("INT", {"default": 0, "min": 0, "max": 9999, "step": 1 }),
            }, "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "IMAGE", "IMAGE")
    RETURN_NAMES = ("weights", "weights_invert", "image_1", "image_2")
    FUNCTION = "weights_by_timings"
    CATEGORY = "💜Akatz Nodes"
    DESCRIPTION = """
      Used to provide custom timings for crossfading multiple images using just two IPAdapters.
      Text input should be a string of weights in the form: "(weight, start_frame, duration, interpolation_function),..."
      E.g. "(1.0, 0, 24, linear), (0.5, 24, 12, ease_in), (0.0, 48, 24, ease_out)"
      A default timing of "ease_in_out" is used if no interpolation function is specified.
      - weights: The weights and timings to be applied to the images
      - default_timing: The default easing function to be used for transitions
      - frames: The number of frames in the output
      - image: The image batch to be crossfaded by the weights
    """

    def parse_weights_string(self, weights_str, default_timing="ease_in_out"):
        # Convert the string to a list of tuples
        weights_list = []
        for weight_str in weights_str.split("),"):
            weight_str = weight_str.replace("(", "").replace(")", "").strip()
            if weight_str:
                parts = weight_str.split(",")
                weight = float(parts[0])
                start_frame = int(parts[1].strip()) if len(parts) > 1 else 0
                duration = int(parts[2].strip()) if len(parts) > 2 else 0
                timing = parts[3].strip() if len(parts) > 3 else default_timing
                weights_list.append((weight, start_frame, duration, timing))
        return weights_list

    def interpolate_weights(self, weights_list, frames):
        # Initialize weights based on the first tuple
        initial_weight = weights_list[0][0] if weights_list[0][1] == 0 else 1.0
        weights = [initial_weight] * frames
        
        for weight, start_frame, duration, timing in weights_list:
            if start_frame >= frames:
                continue

            if duration == 0:
                duration = frames - start_frame
            
            end_frame = min(start_frame + duration, frames)
            start_value = weights[start_frame - 1] if start_frame > 0 else initial_weight
            delta = weight - start_value
            
            for i in range(start_frame, end_frame):
                t = (i - start_frame) / duration if duration > 0 else 1.0
                if timing == "linear":
                    weights[i] = start_value + delta * t
                elif timing == "ease_in":
                    weights[i] = start_value + delta * math.sin(t * math.pi / 2)
                elif timing == "ease_out":
                    weights[i] = start_value + delta * (1 - math.cos(t * math.pi / 2))
                elif timing == "ease_in_out":
                    weights[i] = start_value + delta * (1 - math.cos(t * math.pi)) / 2
                else:
                    weights[i] = weight
            
            # Fill the remaining frames after the transition with the final weight value
            for i in range(end_frame, frames):
                weights[i] = weight
        
        return weights

    def weights_by_timings(self, weights='', frames=0, image=None, default_timing="ease_in_out"):
        # Parse the weights string
        weights_list = self.parse_weights_string(weights, default_timing)

        # Interpolate weights based on parsed weights_list
        weights = self.interpolate_weights(weights_list, frames)
        
        if len(weights) == 0:
            weights = [0.0]

        frames = len(weights)

        # Prepare images for crossfade
        image_1 = []
        image_2 = []
        
        evens = (lambda n: n if n % 2 == 0 else n + 1)(len(image))
        odds =  (lambda n: n if n % 2 == 0 else n - 1)(len(image))

        if image is not None:
            if len(weights_list) < 1:
                image_1 = image
                image_2 = image
            else:
                change_frame_list = [weights_list[i][1] + weights_list[i][2] for i in range(len(weights_list))]
                cur_image_array = 0   # used for switching between image_1 and image_2 based on transitions
                cur_timing_index = 0  # used for incrementing through timings array
                img_idx_1 = 0 # evens
                img_idx_2 = 1 # odds

                for i in range(frames):
                    if i == change_frame_list[cur_timing_index]:
                        cur_timing_index += 1 if cur_timing_index < len(change_frame_list) - 1 else 0
                        if i != 0: # don't change images on the first frame
                            if cur_image_array == 0:
                                img_idx_1 += 2
                                cur_image_array = 1
                            else:
                                img_idx_2 += 2
                                cur_image_array = 0
                    image_1.append(image[img_idx_1 % evens])
                    image_2.append(image[img_idx_2 % odds])
                
                image_1 = torch.stack(image_1)
                image_2 = torch.stack(image_2)

        # Find the maximum value in the list
        max_weight = max(weights)

        # Invert the weights relative to the maximum value
        weights_invert = [max_weight - weight for weight in weights]
        
        return (weights, weights_invert, image_1, image_2)
