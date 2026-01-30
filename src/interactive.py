import os
import re
from .utils import get_file_size, format_normalizer
from .consts import ALL_FORMATS
from .convert import convert_image
from PIL import Image


def show_header(filepath: str):
    INTERNAL_WIDTH = 22 + len(
        os.path.basename(filepath)
    )  #  INTERACTIVE MODE for:   => 19 characters + 3 spaces
    separator = "-" * (INTERNAL_WIDTH)
    print(f"\n{separator}")
    print(f"INTERACTIVE MODE for: {os.path.basename(filepath)}")
    # Original Size: " => 16 characters
    print(f"Original Size: {get_file_size(filepath):>{INTERNAL_WIDTH-15}}")
    print(separator)


def show_and_create_previews(img: Image.Image, filepath: str, output_dir: str = None):
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
        return []

    # Display the comparison table
    print("\n[Comparison] Generated File Sizes:")
    print("-" * 50)
    for fmt, (path, size) in generated_files.items():
        display_path = os.path.basename(path) if output_dir else path
        print(f"{fmt.upper():^6} | {size:>10} | {display_path}")
    print("-" * 50)

    return generated_files


def parse_user_choice():
    print("Which formats do you want to KEEP?")
    print("- Enter formats separated by spaces (e.g., ‘jpg webp’)")
    print("- Enter ‘all’ to keep them all")
    print("- Enter ‘none’ to delete all previews")
    choice = input("\n> ").lower().strip()
    return choice


def interactive_mode(img: Image.Image, filepath: str, output_dir: str = None):
    show_header(filepath)

    generated_files = show_and_create_previews(img, filepath, output_dir)

    choice = parse_user_choice()

    # Parsing with Regex
    wanted_formats = re.split(r"[;,]\s*|\s+", choice)
    wanted_formats_normalized = format_normalizer(wanted_formats, generated_files)

    # At this point, wanted_formats_normalized contains only ‘jpg’, ‘png’, ‘webp’ as unique values.
    files_to_delete = []
    kept_formats = []

    if "all" in wanted_formats:
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
