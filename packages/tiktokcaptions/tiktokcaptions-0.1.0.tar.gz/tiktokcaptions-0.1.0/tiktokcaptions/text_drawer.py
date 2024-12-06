from moviepy.editor import TextClip, ImageClip, VideoClip, CompositeVideoClip
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import numpy as np
import tempfile

text_cache = {}
shadow_cache = {}

class Character:
    def __init__(self, text, color=None):
        self.text = text
        self.color = color

    def set_color(self, color):
        self.color = color

class Word:
    def __init__(self, text):
        self.text = text
        self.color = None
        self.background = None
        self.background_padding = (8, 4)  # (horizontal, vertical) padding
        self.background_radius = 6  # rounded corner radius

    def set_background(self, color):
        self.background = color
        return self

class TextClipEx(TextClip):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs["txt"]

def moviepy_to_pillow(clip) -> Image:
    temp_file = tempfile.NamedTemporaryFile(suffix=".png").name
    clip.save_frame(temp_file)
    image = Image.open(temp_file)
    return image

def get_text_size(text, fontsize, font, stroke_width):
    text_clip = create_text(text, fontsize=fontsize, color="white", font=font, stroke_width=stroke_width)
    return text_clip.size

def get_text_size_ex(text, font, fontsize, stroke_width):
    text_clip = create_text_ex(text, font_size=fontsize, color="white", font=font, stroke_width=stroke_width)
    return text_clip.size

def blur_text_clip(text_clip, blur_radius: int) -> VideoClip:
    # Convert TextClip to a PIL image
    pil_img = moviepy_to_pillow(text_clip)

    # Create a new black background image
    pil_img_padded = Image.new("RGBA", (pil_img.width + blur_radius * 3, pil_img.height + blur_radius * 3), (0, 0, 0, 0))

    # Paste the original image with offset
    offset = int(blur_radius * 0.6)
    pil_img_padded.paste(pil_img, (blur_radius+offset, blur_radius+offset), pil_img)

    # Create a blurred version of the text
    pil_img_padded = pil_img_padded.filter(
        ImageFilter.GaussianBlur(radius=blur_radius)
    )

    # Convert back to ImageClip
    return ImageClip(np.array(pil_img_padded), transparent=True)

def create_text(
    text: str,
    fontsize: int,
    color: str,
    font: str,
    bg_color: str = 'transparent',
    blur_radius: int = 0,
    opacity: float = 1.0,
    stroke_color: str | None = None,
    stroke_width: int = 1,
    kerning: float = 0.0,
) -> VideoClip:
    global text_cache

    arg_hash = hash((text, fontsize, color, font, bg_color, blur_radius, opacity, stroke_color, stroke_width, kerning))

    if arg_hash in text_cache:
        return text_cache[arg_hash].copy()

    text_clip = TextClipEx(txt=text, fontsize=fontsize, color=color, bg_color=bg_color, font=font, stroke_color=stroke_color, stroke_width=stroke_width, kerning=kerning)

    text_clip = text_clip.set_opacity(opacity)

    if blur_radius:
        text_clip = blur_text_clip(text_clip, blur_radius)

    text_cache[arg_hash] = text_clip.copy()

    return text_clip

def create_text_chars(
    text: list[Word] | list[Character],
    fontsize,
    color,
    font,
    bg_color = 'transparent',
    blur_radius: int = 0,
    opacity = 1,
    stroke_color = None,
    stroke_width = 1,
    add_space_between_words = True,
) -> list[VideoClip]:
    # Create a clip for each character
    clips = []
    for i, item in enumerate(text):
        if isinstance(item, Word):
            chars = item.characters
            if add_space_between_words and i < len(text) - 1:
                chars.append(Character(" ", item.color))
        else:
            chars = [item]

        for char in chars:
            clip = create_text(char.text, fontsize, char.color or color, font, bg_color, blur_radius, opacity, stroke_color, stroke_width)
            clips.append(clip)

    return clips

def create_composite_text(text_clips: list[VideoClip], font, font_size) -> CompositeVideoClip:
    clips = []

    font = ImageFont.truetype(font, font_size)
    scale_factor = 3.012 # factor to convert Pillow to MoviePy width

    full_width = 0
    for clip in text_clips[:-1]:
        width = font.getlength(clip.text) * scale_factor
        full_width += width

    full_width += text_clips[-1].size[0]
    offset_x = 0

    for clip in text_clips:
        clip.size = (int(full_width), clip.size[1])
        clip = clip.set_position((int(offset_x), 0))
        width = font.getlength(clip.text)
        offset_x += width * scale_factor
        clips.append(clip)

    return CompositeVideoClip(clips)

def str_to_charlist(text: str) -> list[Character]:
    return [Character(char) for char in text]

def create_text_ex(text, font_size, color, font, stroke_color=None, stroke_width=0, opacity=1.0):
    # If text is a string, convert it to list of Word objects
    if isinstance(text, str):
        text = [Word(text)]

    # Create a PIL Image
    draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    font_obj = ImageFont.truetype(font, font_size)

    # First pass - calculate positions and total size without backgrounds
    current_x = font_size * 0.1  # Add small initial offset
    max_height = 0
    word_positions = []

    # Get max height first using reference characters
    bbox = draw.textbbox((0, 0), "ÁÉÍÓÚÝjpqy", font=font_obj)
    max_height = bbox[3] - bbox[1]
    max_height += font_size * 0.1  # Add small padding

    # Calculate positions without background padding influence
    for word in text:
        # Get exact text dimensions including any spacing
        bbox = draw.textbbox((current_x, 0), word.text, font=font_obj)
        word_width = bbox[2] - bbox[0]  # Calculate width relative to position

        word_positions.append({
            'x': current_x,
            'width': word_width,
            'bbox': bbox
        })

        current_x += word_width + (font_size * 0.2)  # Space between words

    total_width = current_x + (font_size * 0.1)  # Add ending offset

    # Create the actual image
    img = Image.new('RGBA', (int(total_width), int(max_height)), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Second pass - draw backgrounds and text
    for i, word in enumerate(text):
        metrics = word_positions[i]
        x = metrics['x']
        width = metrics['width']

        y = 0  # Since we calculated max_height properly, we can start at 0

        if word.background:
            # Calculate background dimensions
            padded_width = width + (word.background_padding[0] * 2)
            padded_height = max_height * 0.95

            # Center the background around the text
            bg_x = x - word.background_padding[0]
            bg_y = y + (max_height * 0.05)

            background_bbox = [
                bg_x, bg_y,
                bg_x + padded_width, bg_y + padded_height
            ]

            draw.rounded_rectangle(
                background_bbox,
                fill=word.background,
                radius=word.background_radius
            )

        # Draw text
        if stroke_width > 0 and stroke_color:
            draw.text((x, y), word.text, font=font_obj, fill=stroke_color, stroke_width=stroke_width)

        text_color = word.color if word.color else color
        draw.text((x, y), word.text, font=font_obj, fill=text_color)

    # Convert to MoviePy ImageClip
    return ImageClip(np.array(img), transparent=True).set_opacity(opacity)

def create_shadow(text: str, font_size: int, font: str, blur_radius: float, opacity: float=1.0):
    global shadow_cache

    arg_hash = hash((text, font_size, font, blur_radius, opacity))

    if arg_hash in shadow_cache:
        return shadow_cache[arg_hash].copy()

    # Create black text with stroke to make it more visible
    shadow = create_text_ex(
        text,
        font_size,
        color="black",
        font=font,
        stroke_color="black",
        stroke_width=2,  # Add stroke to make shadow more prominent
        opacity=1.0
    )

    # Apply blur effect
    shadow = blur_text_clip(shadow, int(font_size*blur_radius))

    # Apply final opacity
    shadow = shadow.set_opacity(opacity * 0.5)  # Reduce opacity to make shadow softer

    shadow_cache[arg_hash] = shadow.copy()

    return shadow
