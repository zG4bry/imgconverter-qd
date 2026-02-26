from src.arg_parser import parse_args
from src.processor import process_image_file
from src.consts import ALL_FORMATS


def main():
    parser, args = parse_args()
    if args.color and not args.ascii:
        parser.error("--color/-c can only be used together with --ascii")
    requested_formats = [f for f in ALL_FORMATS if getattr(args, f)]

    requested_art = args.ascii or args.ansi

    for filepath in args.image_paths:
        process_image_file(filepath, args, requested_formats, requested_art)

    if requested_art and not requested_formats:
        print("Text Art display only (no files saved).")


if __name__ == "__main__":  # pragma: no cover
    main()
