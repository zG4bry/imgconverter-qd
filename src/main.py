from arg_parser import parse_args
from utils import get_file_size, open_image
from convert import to_ansi, to_ascii, convert_image
from interactive import interactive_mode
from consts import ALL_FORMATS
import time

def main():
    parser, args = parse_args()
    if args.color and not args.ascii:
        parser.error("--color/-c can only be used together with --ascii")
    requested_formats = [f for f in ALL_FORMATS if getattr(args, f)]

    requested_art = args.ascii or args.ansi

    for filepath in args.image_paths:
        img = open_image(filepath)
        if not img:
            continue
        is_animated = getattr(img, "is_animated", False)
        num_frames = getattr(img, "n_frames", 1)
        for frame_index in range(num_frames):
            img.seek(frame_index)
            current_frame = img.convert("RGBA")
            art_displayed = False
            if args.ascii:  # print ASCII Art (if requested)
                # clear terminal
                print("\033[H\033[J", end="")
                print(f"ASCII ART Frame: {frame_index + 1}/{num_frames}")
                print(to_ascii(current_frame, args.width, args.color))
                print(f"{"-"*args.width}")
                art_displayed = True
            if args.ansi:  # print ANSI Art (if requested)
                print("\033[H\033[J", end="")
                print(f"ASCII ART Frame: {frame_index + 1}/{num_frames}")
                print(to_ansi(current_frame, args.width))
                print(f"{"-"*args.width}")
                art_displayed = True
            # if it is animated
            if art_displayed and is_animated:
                # get the frame duration from the GIF (default 100ms)
                duration = img.info.get("duration", 100) / 1000.0
                time.sleep(duration)
            # convert images (if requested)

            # CAMBIARE NOME PER OGNI FRAME CONVERTITO!!!!
            if requested_formats:
                for fmt in requested_formats:
                    output_file = convert_image(img, filepath, fmt, args.output)
                    if output_file:
                        print(f"Saved: {output_file} \t{get_file_size(output_file)}")

        # if nothing has been specified, I will proceed with the interactive mode. Only for the first frame
        if not requested_art and not requested_formats:
            img.seek(0)
            interactive_mode(img.convert("RGBA"), filepath)
        else:
            print("Text Art display only (no files saved).")


if __name__ == "__main__":
    main()
