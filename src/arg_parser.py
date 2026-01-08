from consts import DEFAULT_WIDTH
import argparse


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
art_group.add_argument("--ascii", action="store_true", help="print ASCII Art version")
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
