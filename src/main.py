import sys, argparse, os
from PIL import Image

DEFAULT_WIDTH = 50


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


def convert_image(img: Image.Image, source_path: str, target_format: str):
    filename_root = os.path.splitext(source_path)[0]
    filename_output = f"{filename_root}.{target_format}"
    try:
        out_img = img.copy()
        match target_format:
            case "jpg" | "jpeg":
                if img.mode in ("RGBA", "P"):
                    out_img = img.convert("RGB")
                out_img.save(filename_output, quality=90)
            case "png":
                out_img.save(filename_output, optimize=True)
            case "webp":
                out_img.save(filename_output)
            case _:
                print(f"{target_format.upper} format not supported\n")
                return None
        return filename_output
    except (OSError, ValueError) as e:
        print(f"Errore: {e}")


def main():

    parser = argparse.ArgumentParser(
        description="Tool for converting images into various formats and/or ASCII/ANSI characters"
    )
    parser.add_argument(
        "image_paths", type=str, nargs="+", help="Path of one or more images"
    )
    # Output formats
    parser.add_argument(
        "--jpg", "--jpeg", action="store_true", help="Converts the image to JPG format"
    )
    parser.add_argument(
        "--png", action="store_true", help="Converts the image to PNG format"
    )
    parser.add_argument(
        "--webp", action="store_true", help="Converts the image to WebP format"
    )
    # Text art
    parser.add_argument("--ascii", action="store_true", help="Print ASCII Art version")
    parser.add_argument(
        "--ansi", action="store_true", help="Print ANSI Color Art version"
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"Output width art (default: {DEFAULT_WIDTH})",
    )
    args = parser.parse_args()

    requested_formats = []
    if args.jpg:
        requested_formats.append("jpg")
    if args.png:
        requested_formats.append("png")
    if args.webp:
        requested_formats.append("webp")

    for filepath in args.image_paths:
        img = open_image(filepath)
        if not img:
            continue

        if requested_formats:
            for fmt in requested_formats:
                output_file = convert_image(img, filepath, fmt)
                if output_file:
                    print(f"Saved: {output_file}")  # Implementare calcolo memoria


if __name__ == "__main__":
    main()
