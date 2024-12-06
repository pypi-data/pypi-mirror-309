# TikTok Captions

Add TikTok-style captions to your videos automatically using OpenAI's Whisper for transcription.

## Installation

```bash
pip install tiktokcaptions
```

## Usage

```python
from tiktokcaptions import add_captions_to_videofile

# whisper transcription (dict)
transcription = ...

# Basic usage
add_captions_to_videofile("input.mp4", transcription=transcription, output_file="with_captions.mp4")

# With custom options
add_captions_to_videofile(
    "input.mp4",
    transcription=transcription,
    output_file="with_captions.mp4",

    # Font settings
    font="Montserrat-ExtraBold.ttf",  # or path to custom font
    font_size=70,
    font_color="white",

    # Stroke settings
    stroke_width=2,
    stroke_color="black",

    # Word highlighting
    highlight_current_word=True,
    highlight_color="#FF4500",
    highlight_padding=(10, 8),  # (x, y) padding
    highlight_radius=10,

    # Layout
    line_count=2,
    padding=50,
    position="center",  # "top", "bottom", or "center"
    margin=0,

    # Shadow effects
    shadow_strength=1.0,
    shadow_blur=0.3,

    # Other
    verbose=False
)
```

## Features
- Automatic speech recognition using Whisper
- Customizable caption styling
- Support for multiple video formats
- Easy to use API

## Requirements
- Python 3.7+
- FFmpeg installed on your system

## License
MIT License - see LICENSE file for details.