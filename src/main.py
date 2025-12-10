import sys
import argparse
import os
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
                return filename_output
            case "png":
                out_img.save(filename_output, optimize=True)
                return filename_output
            case "webp":
                out_img.save(filename_output)  # default quality 80
                return filename_output
            case _:
                print(f"{target_format.upper()} format not supported\n")
                return None
        return filename_output
    except (OSError, ValueError) as e:
        print(f"Errore: {e}")
        return None


def interactive_mode(img: Image.Image, filepath: str):
    INTERNAL_WIDTH = 22 + len(
        filepath
    )  #  INTERACTIVE MODE for:   => 19 characters + 3 spaces
    separator = "-" * (INTERNAL_WIDTH)
    print(separator)
    print(f"INTERACTIVE MODE for: {filepath}")
    # Original Size: " => 16 characters
    print(f"Original Size: {get_file_size(filepath):>{INTERNAL_WIDTH-15}}")
    print(separator)

    # Dictionary to store results: {format: (path, size_string)}
    generated_files = {}

    # Convert to all available formats and store results
    print("Generating temporary previews...")

    for fmt in ALL_FORMATS:
        out_path = convert_image(img, filepath, fmt)
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
    print("---------------------------------------")
    for fmt, (path, size) in generated_files.items():
        print(f"{fmt.upper():^6} | {size:>10} | {path}")
    print("---------------------------------------")

    # Prompt the user for action
    prompt_msg = "Keep formats (e.g., 'jpg png'), 'all', or 'none'? "
    choice = input(prompt_msg).lower().strip()

    # Normalize choices for parsing (handle 'jpeg' manually if not in ALL_FORMATS)
    wanted_formats = choice.split()

    if "all" in wanted_formats or choice == "all":
        print("All generated files kept.")
        return

    if "none" in wanted_formats or choice == "none" or not wanted_formats:
        # If the user enters nothing, we assume 'none'
        print("No files kept. Deleting all generated files...")

        for path, _ in generated_files.values():
            try:
                os.remove(path)
            except OSError as e:
                print(f"[Warning] Could not delete {path}: {e}")
        return

    # Process the user's selection and perform deletion
    kept_formats = []

    # 'jpeg' as an alias for 'jpg'
    if "jpg" in ALL_FORMATS and "jpeg" in wanted_formats:
        wanted_formats.remove("jpeg")
        if "jpg" not in wanted_formats:
            wanted_formats.append("jpg")

    for fmt, (path, size) in generated_files.items():
        if fmt in wanted_formats:
            kept_formats.append(fmt.upper())
        else:
            try:
                os.remove(path)
            except OSError as e:
                print(f"[Warning] Could not delete {path}: {e}")

    if kept_formats:
        print(f"Success! Kept: {", ".join(kept_formats)}")
    else:
        print("No files kept. All generated previews deleted.")


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
                output_file = convert_image(img, filepath, fmt)
                if output_file:
                    print(f"Saved: {output_file} \t{get_file_size(output_file)}")
                else:
                    print("Image not saved")
                    sys.exit(1)

        # if nothing has been specified, I will proceed with the interactive mode
        elif not requested_art:
            interactive_mode(img, filepath)
        else:
            print("Text Art display only (no files saved).")


if __name__ == "__main__":
    main()
