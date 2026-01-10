from consts import ASCII_CHARS
from utils import resize_img, get_source_ext
from PIL import Image
import os


def to_ascii(img: Image.Image, width: int, colored: bool):
    img = resize_img(img, width)
    if colored:
        img = img.convert("RGBA")
    else:
        img = img.convert("LA")
    pixels = img.getdata()
    ascii_str = ""
    n = len(ASCII_CHARS)
    for i, pixel in enumerate(pixels):
        if colored:
            r, g, b, a = pixel
            if a == 0:
                ascii_str += " "
            else:
                l = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
                index = int((l * (n - 1)) / 255)
                ascii_str += f"\033[38;2;{r};{g};{b}m{ASCII_CHARS[index]}"
            if (i + 1) % width == 0:
                ascii_str += "\n"
        else:
            l, a = pixel
            if a == 0:
                ascii_str += " "
            else:
                index = int((l * (n - 1)) / 255)
                ascii_str += ASCII_CHARS[index]
            if (i + 1) % width == 0:
                ascii_str += "\n"
    return ascii_str


def to_ansi(img: Image.Image, width: int):
    img = resize_img(img, width).convert("RGBA")
    pixels = img.getdata()
    ansi_str = ""
    CHARACTER = "█"
    for i, pixel in enumerate(pixels):
        r, g, b, a = pixel
        if a == 0:
            ansi_str += "\033[0m "  # print transparent pixel
        else:
            ansi_str += (
                f"\033[38;2;{r};{g};{b}m{CHARACTER}"  # add colored CHARACTER to string
            )
        if (i + 1) % width == 0:
            ansi_str += "\033[0m\n"  # color reset and new line
    ansi_str += "\033[0m"  # color reset
    return ansi_str


# Aggiungere controllo dell'estensione iniziale. Se è uguale al formato in cui deve essere convertita annullare.
def convert_image(
    img: Image.Image,
    source_path: str,
    target_format: str,
    output_dir: str = None,
    index: int = None,
):
    source_ext = get_source_ext(source_path)

    normalized_source = "jpg" if source_ext == "jpeg" else source_ext
    normalized_target = "jpg" if target_format == "jpeg" else target_format

    if normalized_source == normalized_target:
        print(
            f"Skipping: '{source_path}' is already in {target_format.upper()} format."
        )
        return None

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename_root = os.path.join(
            output_dir, os.path.splitext(os.path.basename(source_path))[0]
        )
    else:
        filename_root = os.path.splitext(source_path)[0]
    is_animated = getattr(img, "is_animated", False)
    if is_animated and index is not None:
        filename_output = f"{filename_root}_{index}.{target_format}"
    else:
        filename_output = f"{filename_root}.{target_format}"
    try:
        out_img = img.copy()

        match target_format:
            case "jpg" | "jpeg":
                # JPG doesn't support transparency
                if img.mode in ("RGBA", "P"):
                    out_img = img.convert("RGB")
                out_img.save(filename_output)  # default quality 75
            case "png":
                out_img.save(filename_output, optimize=True)
            case "webp":
                out_img.save(filename_output)  # default quality 80
            case _:
                print(f"{target_format.upper()} format not supported\n")
                return None
        return filename_output
    except (OSError, ValueError) as e:
        print(f"Errore: {e}")
        return None
