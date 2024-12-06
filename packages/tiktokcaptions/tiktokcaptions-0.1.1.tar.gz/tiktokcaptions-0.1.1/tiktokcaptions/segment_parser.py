from typing import Callable

def is_sentence_boundary(current_word: str, next_word: str | None = None) -> bool:
    # Check if current word ends with period
    current = current_word.strip()
    if current.endswith("."):
        return True

    # If we have a next word and it starts with capital letter (after stripping space)
    if next_word and next_word.strip() and next_word.strip()[0].isupper():
        return True

    return False

def parse(
    segments: list[dict],
    fit_function: Callable,
    allow_partial_sentences: bool = False,
):
    captions = []
    caption = {
        "start": None,
        "end": 0,
        "words": [],
        "text": "",
    }

    # Merge words that are not separated by spaces
    for s, segment in enumerate(segments):
        for w, word in enumerate(segment["words"]):
            if w > 0 and word["word"][0] != " ":
                segments[s]["words"][w-1]["word"] += word["word"]
                segments[s]["words"][w-1]["end"] = word["end"]
                del segments[s]["words"][w]

    # Parse segments into captions that fit on the video
    for segment in segments:
        for i, word in enumerate(segment["words"]):
            current_word = word["word"]
            next_word = segment["words"][i + 1]["word"] if i + 1 < len(segment["words"]) else None

            # If we don't have a caption started yet
            if caption["start"] is None:
                caption["start"] = word["start"]

            # Check if adding this word would fit
            test_text = caption["text"] + current_word
            caption_fits = fit_function(test_text)

            if caption_fits:
                # Add the word to current caption
                caption["words"].append(word)
                caption["end"] = word["end"]
                caption["text"] = test_text

                # Check if this is a sentence boundary
                if is_sentence_boundary(current_word, next_word):
                    # Save current caption
                    captions.append(caption)
                    # Start new caption
                    caption = {
                        "start": None,
                        "end": 0,
                        "words": [],
                        "text": "",
                    }
            else:
                # If caption doesn't fit, save current and start new
                if caption["words"]:
                    captions.append(caption)
                caption = {
                    "start": word["start"],
                    "end": word["end"],
                    "words": [word],
                    "text": current_word,
                }

    # Add the final caption if it has content
    if caption["words"]:
        captions.append(caption)

    return captions
