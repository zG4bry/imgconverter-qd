import sys
import argparse
import os
import re
from PIL import Image

ALL_FORMATS = ["png", "jpg", "webp"]
DEFAULT_WIDTH = 90
ASCII_CHARS = "@&#%?=+*;:~-,. "
# ASCII_CHARS = "@#%?*+;:,. "
# ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`\'."


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


def get_file_size(filepath: str):
    if not os.path.exists(filepath):
        return None
    return format_size(os.path.getsize(filepath))


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
        print(f"Skipping: '{source_path}' is already in {target_format.upper()} format.")
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


def interactive_mode(img: Image.Image, filepath: str, output_dir: str = None):
    INTERNAL_WIDTH = 22 + len(
        os.path.basename(filepath)
    )  #  INTERACTIVE MODE for:   => 19 characters + 3 spaces
    separator = "-" * (INTERNAL_WIDTH)
    print(f"\n{separator}")
    print(f"INTERACTIVE MODE for: {os.path.basename(filepath)}")
    # Original Size: " => 16 characters
    print(f"Original Size: {get_file_size(filepath):>{INTERNAL_WIDTH-15}}")
    print(separator)

    # Dictionary to store results: {format: (path, size_string)}
    generated_files = {}

    # Convert to all available formats and store results
    print("Generating temporary previews...")

    for fmt in ALL_FORMATS:
        out_path = convert_image(img, filepath, fmt, output_dir)
        if out_path:
            size = get_file_size(out_path)
            generated_files[fmt] = (out_path, size)
        else:
            print(f"  [Error] Failed to generate {fmt.upper()}.")

    if not generated_files:
        print("\n[Error] Could not generate any output files.")
        return

    # Display the comparison table
    print("\n[Comparison] Generated File Sizes:")
    print("-" * 50)
    for fmt, (path, size) in generated_files.items():
        display_path = os.path.basename(path) if output_dir else path
        print(f"{fmt.upper():^6} | {size:>10} | {display_path}")
    print("-" * 50)

    # User input
    print("Which formats do you want to KEEP?")
    print("- Enter formats separated by spaces (e.g., ‘jpg webp’)")
    print("- Enter ‘all’ to keep them all")
    print("- Enter ‘none’ to delete all previews")
    choice = input("\n> ").lower().strip()

    # Parsing with Regex
    wanted_formats = re.split(r"[;,]\s*|\s+", choice)
    wanted_formats_normalized = format_normalizer(wanted_formats, generated_files)

    # At this point, wanted_formats_normalized contains only ‘jpg’, ‘png’, ‘webp’ as unique values.

    files_to_delete = []
    kept_formats = []

    if "all" in wanted_formats_normalized:
        print("All generated files kept.")
        return

    if "none" in wanted_formats_normalized or not choice:
        # If the user enters nothing, we assume 'none'
        files_to_delete = list(generated_files.keys())
        print("No files kept. Deleting all generated files...")
    else:
        for fmt, _ in generated_files.items():
            if fmt in wanted_formats_normalized:
                kept_formats.append(fmt)
            else:
                files_to_delete.append(fmt)

    # deletion process
    for fmt in files_to_delete:
        path_to_remove = generated_files[fmt][0]
        try:
            os.remove(path_to_remove)
        except OSError as e:
            print(f"[Warning] Could not delete {path_to_remove}: {e}")

    if kept_formats:
        print(f"Success! Kept: {", ".join(kept_formats)}")
    elif "none" in wanted_formats:
        print("No files kept. All generated previews deleted.")


def main():

    parser = argparse.ArgumentParser(
        description="Tool for converting images into various formats and/or ASCII/ANSI characters"
    )
    # Input
    parser.add_argument(
        "image_paths", type=str, nargs="+", help="path of one or more images."
    )
    # Output dir
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Destination folder for converted files.",
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

        if args.ascii:  # print ASCII Art (if requested)
            print(f"\n{" ASCII ART ":-^{args.width}}\n")
            print(to_ascii(img, args.width))
            print(f"{"-"*args.width}")
        if args.ansi:  # print ANSI Art (if requested)
            print(f"\n{" ANSI ART ":-^{args.width}}\n")
            print(to_ansi(img, args.width))
            print(f"{"-"*args.width}")

        # convert images (if requested)
        if requested_formats:
            for fmt in requested_formats:
                output_file = convert_image(img, filepath, fmt, args.output)
                if output_file:
                    print(f"Saved: {output_file} \t{get_file_size(output_file)}")
                else:
                    pass

        # if nothing has been specified, I will proceed with the interactive mode
        elif not requested_art:
            interactive_mode(img, filepath)
        else:
            print("Text Art display only (no files saved).")


if __name__ == "__main__":
    main()
