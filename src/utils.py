import os
import sys
from PIL import Image
from consts import DEFAULT_WIDTH, ALL_FORMATS


def format_size(size_bytes: int):
    if size_bytes is None:
        return None
    units = ["B", "KB", "MB", "GB"]
    divisor = 1024
    size = float(size_bytes)

    for i in range(len(units) - 1):
        if size < divisor:
            return f"{size:.2f} {units[i]}"
        size /= divisor
    # if it exceeds GB, it remains in GB
    return f"{size:.2f} {units[-1]}"

def get_source_ext(source_path):
    return os.path.splitext(source_path)[1].lower().lstrip(".")

def get_file_size(filepath: str):
    if not os.path.exists(filepath):
        return None
    return format_size(os.path.getsize(filepath))


def resize_img(img: Image.Image, width: int = DEFAULT_WIDTH):
    w, h = img.size
    ratio = h / w
    new_height = int(
        (width * ratio * 0.55)
    )  # 0.55 is the correction factor for rectangular terminal fonts.
    return img.resize((width, new_height))


def format_normalizer(raw, files):
    normalized = set()
    for fmt in raw:
        if not fmt:
            continue
        normalized_fmt = "jpg" if fmt == "jpeg" else fmt
        if normalized_fmt in files:
            normalized.add(normalized_fmt)
        elif normalized_fmt in ALL_FORMATS:
            print(
                f"Note: ‘{fmt.upper()}’ was not generated (it may be the original format)."
            )
    return normalized


def open_image(image_path: str):
    try:
        with Image.open(image_path) as img:
            return img.copy()
    except FileNotFoundError:
        print(f"Error: File not found'{image_path}'")
        sys.exit(1)
    except OSError as e:
        print(f"Error: Unable to process the image {e}")
        sys.exit(1)
