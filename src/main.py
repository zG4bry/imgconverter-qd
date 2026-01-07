from arg_parser import args
from utils import get_file_size, open_image
from convert import to_ansi, to_ascii, convert_image
from interactive import interactive_mode


def main():

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
