import sys
import argparse
import os
from PIL import Image

DEFAULT_WIDTH = 90
ASCII_CHARS = "@&#%?=+*;:~-,. "
# ASCII_CHARS = "@#%?*+;:,. "
# ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`\'."


def open_image(image_path: str):
    try:
        with Image.open(image_path) as img:
            return img.copy()
    except FileNotFoundError:
        print(f"Error: File non found'{image_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def resize_for_terminal(img: Image.Image, width: int = DEFAULT_WIDTH):
    w, h = img.size
    ratio = h / w
    new_height = int(
        (width * ratio * 0.55)
    )  # 0.55 is the correction factor for rectangular terminal fonts.
    return img.resize((width, new_height))


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
        ansi_str += f"\033[38;2;{r};{g};{b}m{CHARACTER}"
        if (i + 1) % width == 0:
            ansi_str += "\033[0m\n"  # Resetta colore e vai a capo
    ansi_str += "\033[0m"  # Reset finale
    return ansi_str


def convert_image(img: Image.Image, source_path: str, target_format: str):
    filename_root = os.path.splitext(source_path)[0]
    filename_output = f"{filename_root}.{target_format}"
    try:
        out_img = img.copy()
        match target_format:
            case "jpg" | "jpeg":
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


def main():

    parser = argparse.ArgumentParser(
        description="Tool for converting images into various formats and/or ASCII/ANSI characters"
    )
    parser.add_argument(
        "image_paths", type=str, nargs="+", help="path of one or more images"
    )
    # Output formats
    conv_group = parser.add_argument_group("conversion formats")
    conv_group.add_argument(
        "--jpg", "--jpeg", action="store_true", help="converts the image to JPG format"
    )
    conv_group.add_argument(
        "--png", action="store_true", help="converts the image to PNG format"
    )
    conv_group.add_argument(
        "--webp", action="store_true", help="converts the image to WebP format"
    )
    # Text art
    art_group = parser.add_argument_group("text Art (ASCII/ANSI)")
    art_group.add_argument(
        "--ascii", action="store_true", help="print ASCII Art version"
    )
    art_group.add_argument(
        "--ansi", action="store_true", help="print ANSI Color Art version"
    )
    art_group.add_argument(
        "-w",
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"output width art (default: {DEFAULT_WIDTH})",
    )

    args = parser.parse_args()

    requested_formats = []
    if args.jpg:
        requested_formats.append("jpg")
    if args.png:
        requested_formats.append("png")
    if args.webp:
        requested_formats.append("webp")

    requested_art = args.ascii or args.ansi

    for filepath in args.image_paths:
        img = open_image(filepath)
        if not img:
            continue

        if args.ascii:  # print ASCII Art
            print(
                f"\n{"="*int((args.width-11)/2)} ASCII ART {"="*int((args.width-11)/2)}\n"
            )
            print(to_ascii(img, args.width))
            print(f"{"="*args.width}")
        if args.ansi:  # print ANSI Art
            print(
                f"\n{"="*int((args.width-10)/2)} ANSI ART {"="*int((args.width-10)/2)}\n"
            )
            print(to_ansi(img, args.width))
            print(f"{"="*args.width}")

        # converto immagini (se richiesto)
        if requested_formats:
            for fmt in requested_formats:
                output_file = convert_image(img, filepath, fmt)
                if output_file:
                    print(f"Saved: {output_file}")  # Implementare calcolo memoria

        # se non è stato esplicitato nulla procedo con la modalità interattiva
        elif not requested_art:
            ...  # implementare conversione interattiva con calcolo memoria e scelta immagini convertite
        else:
            print("Text Art display only (no files saved).")


if __name__ == "__main__":
    main()
