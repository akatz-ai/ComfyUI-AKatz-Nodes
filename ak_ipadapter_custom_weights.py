import math
import torch
import ast
import re

class AK_IPAdapterCustomWeights:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE", {"defaultInput": True}),
            "weights": ("STRING", {"default": '(1.0),', "multiline": True }),
            "default_easing": (["linear", "ease_in_out", "ease_in", "ease_out"], { "default": "ease_in_out" } ),
            "timing_mode": (["Frame", "Percent"], { "default": "Frame" } ),
            "frames": ("INT", {"default": 0, "min": 0, "step": 1 }),
            },
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "IMAGE", "IMAGE")
    RETURN_NAMES = ("weights", "weights_invert", "image_1", "image_2")
    FUNCTION = "weights_by_timings"
    CATEGORY = "💜Akatz Nodes/Scheduling"
    DESCRIPTION = """
      Used to provide custom timings for crossfading multiple images using just two IPAdapters.
      Text input should be a string of weights in the format:
      (<weights (float or float tuple)>, <frame_index (int or float)>, <transition_frames (int or float, optional)>, <easing_function (string, optional)>),...
      E.g. Frame: "((0.0, 0.0), 0), (1.0, 5, 20, linear), (0.5, 25, 10, ease_in), ((0.0, 0.0), 48, 24, ease_out)"
      Percentage: "((0.0, 0.0), 0), (1.0, 0.1, 0.1, linear), (0.5, 0.25, 0.1, ease_in), ((0.0, 0.0), 0.5, 0.25, ease_out)"
      A default timing of "ease_in_out" is used if no interpolation function is specified.
      - weights: The weights and timings to be applied to the images
      - default_easing: The default easing function to be used for transitions
      - timing_mode: The timing mode to be used for transitions (Frame or Percent)
      - frames: The number of frames in the output
      - image: The image batch to be crossfaded by the weights
    """

    def parse_weights_string(self, weights_str, default_easing="ease_in_out", timing_mode="Frame", frames=0):
        # Regular expression to capture the desired format, including optional commas and whitespace
        pattern = r'\(\s*(\d*\.?\d+|\(\s*\d*\.?\d+\s*,\s*\d*\.?\d+\s*\))\s*,\s*(\d*\.?\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?(?:,\s*(\w+)\s*)?\)\s*,?'

        # Find all matches in the input string
        matches = re.findall(pattern, weights_str)
        
        if not matches:
            raise ValueError("No valid matches found in the provided weights string.")
        
        weights_list = []
        
        for match in matches:
            weight_str, start_frame_str, duration_str, timing = match

            try:
                # Parse the weight as either a float or a tuple of two floats
                weight = ast.literal_eval(weight_str.strip())
            except (SyntaxError, ValueError):
                raise ValueError(f"Invalid weight format: {weight_str}")
            
            if isinstance(weight, float):
                weight = [weight, 1.0 - weight]  # Convert single float to list with weights and weights_invert
            elif isinstance(weight, list) or isinstance(weight, tuple):
                if len(weight) != 2 or not all(isinstance(w, (int, float)) for w in weight):
                    raise ValueError(f"Invalid weight tuple format: {weight_str}")
            else:
                raise ValueError(f"Invalid weight type: {weight_str}")
            
            try:
                # Parse the start_frame and duration as floats
                start_frame = float(start_frame_str.strip())
                duration = float(duration_str.strip()) if duration_str else 0.0
            except ValueError:
                raise ValueError(f"Invalid number format for start_frame or duration: {start_frame_str}, {duration_str}")
            
            # Handle timing mode
            if timing_mode == "Percent":
                start_frame = max(int(start_frame * frames) - 1, 0)  # Offset by 1 due to 0-based index
                duration = int(duration * frames)

            start_frame = int(start_frame)
            duration = int(duration)
            
            # Use default timing if none is provided
            timing = timing if timing else default_easing
            
            weights_list.append((weight, start_frame, duration, timing))
        
        return weights_list

    def interpolate_weights(self, weights_list, frames):
        # Initialize weights based on the first tuple
        initial_weight = weights_list[0][0][0] if weights_list[0][1] == 0 else 1.0
        initial_weight_invert = weights_list[0][0][1] if weights_list[0][1] == 0 else 0.0
        weights = [initial_weight] * frames
        weights_invert = [initial_weight_invert] * frames
        
        for weight_pair, start_frame, duration, timing in weights_list:
            if start_frame >= frames:
                continue

            if duration == 0:
                duration = frames - start_frame
            
            end_frame = min(start_frame + duration, frames)
            start_value = weights[start_frame - 1] if start_frame > 0 else initial_weight
            start_value_invert = weights_invert[start_frame - 1] if start_frame > 0 else initial_weight_invert
            delta = weight_pair[0] - start_value
            delta_invert = weight_pair[1] - start_value_invert
            
            for i in range(start_frame, end_frame):
                t = (i - start_frame) / duration if duration > 0 else 1.0
                if timing == "linear":
                    weights[i] = start_value + delta * t
                    weights_invert[i] = start_value_invert + delta_invert * t
                elif timing == "ease_in":
                    weights[i] = start_value + delta * math.sin(t * math.pi / 2)
                    weights_invert[i] = start_value_invert + delta_invert * math.sin(t * math.pi / 2)
                elif timing == "ease_out":
                    weights[i] = start_value + delta * (1 - math.cos(t * math.pi / 2))
                    weights_invert[i] = start_value_invert + delta_invert * (1 - math.cos(t * math.pi / 2))
                elif timing == "ease_in_out":
                    weights[i] = start_value + delta * (1 - math.cos(t * math.pi)) / 2
                    weights_invert[i] = start_value_invert + delta_invert * (1 - math.cos(t * math.pi)) / 2
                else:
                    weights[i] = weight_pair[0]
                    weights_invert[i] = weight_pair[1]
            
            # Fill the remaining frames after the transition with the final weight values
            for i in range(end_frame, frames):
                weights[i] = weight_pair[0]
                weights_invert[i] = weight_pair[1]
        
        return weights, weights_invert

    def weights_by_timings(self, weights='', frames=0, image=None, default_easing="linear", timing_mode="Frame"):
        # Parse the weights string
        weights_list = self.parse_weights_string(weights, default_easing, timing_mode, frames)

        # Interpolate weights based on parsed weights_list
        weights, weights_invert = self.interpolate_weights(weights_list, frames)
        
        if len(weights) == 0:
            weights = [0.0]
            weights_invert = [0.0]

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

        return (weights, weights_invert, image_1, image_2)
