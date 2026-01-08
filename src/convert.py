from consts import ASCII_CHARS
from utils import resize_for_terminal
from PIL import Image
import os


def to_ascii(img: Image.Image, width: int):
    img = resize_for_terminal(img, width).convert("LA")
    pixels = img.getdata()
    ascii_str = ""
    n = len(ASCII_CHARS)
    for i, pixel in enumerate(pixels):
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
    img = resize_for_terminal(img, width).convert("RGB")
    pixels = img.getdata()
    ansi_str = ""
    CHARACTER = "█"
    for i, pixel in enumerate(pixels):
        r, g, b = pixel
        ansi_str += (
            f"\033[38;2;{r};{g};{b}m{CHARACTER}"  # add colored CHARACTER to string
        )
        if (i + 1) % width == 0:
            ansi_str += "\033[0m\n"  # color reset and new line
    ansi_str += "\033[0m"  # color reset
    return ansi_str


# Aggiungere controllo dell'estensione iniziale. Se è uguale al formato in cui deve essere convertita annullare.
def convert_image(
    img: Image.Image, source_path: str, target_format: str, output_dir: str = None
):
    source_ext = os.path.splitext(source_path)[1].lower().lstrip(".")

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
