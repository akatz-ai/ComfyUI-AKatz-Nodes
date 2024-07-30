from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch
import sys

class AK_Ascii:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "spacing": ("INT", {
                    "default": 20,
                    "min": 4,
                    "max": 100,
                    "step": 2,
                }),
                "font_size": ("INT", {
                    "default": 20,
                    "min": 4,
                    "max": 100,
                    "step": 2,
                }),
                "characters": ("STRING", {
                    "default": "\._♥♦♣MachineDelusions♣♦♥_./",
                    "description": "characters to use"
                }),
            },
        }

    CATEGORY = "💜 Akatz Nodes"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_ascii_art_effect"

    def apply_ascii_art_effect(self, image: torch.Tensor, spacing: int, font_size: int, characters):
        batch_size, height, width, channels = image.shape
        result = torch.zeros_like(image)

        for b in range(batch_size):
            img_b = image[b] * 255.0
            img_b = Image.fromarray(img_b.numpy().astype('uint8'), 'RGB')
            result_b = ascii_art_effect(img_b, spacing, font_size, characters)
            result_b = torch.tensor(np.array(result_b)) / 255.0
            result[b] = result_b

            # Update the print log
            progress = (b + 1) / batch_size * 100
            sys.stdout.write(f"\rProcessing images: {progress:.2f}%")
            sys.stdout.flush()

        # Print a new line after the progress log
        print()

        return (result,)


def ascii_art_effect(image: torch.Tensor, spacing: int, font_size: int, characters):
    chars = characters
    small_image = image.resize((image.size[0] // spacing, image.size[1] // spacing), Image.Resampling.NEAREST)

    def get_char(value):
        return chars[value * len(chars) // 256]

    ascii_image = Image.new('RGB', image.size, (0, 0, 0))
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    draw_image = ImageDraw.Draw(ascii_image)

    for i in range(small_image.height):
        for j in range(small_image.width):
            r, g, b = small_image.getpixel((j, i))
            k = (r + g + b) // 3
            draw_image.text(
                (j * spacing, i * spacing),
                get_char(k),
                font=font,
                fill=(r, g, b)
            )

    return ascii_image