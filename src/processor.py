import time
from .utils import open_image, get_file_size
from .convert import to_ansi, to_ascii, convert_image
from .interactive import interactive_mode


def process_image_file(filepath, args, requested_formats, requested_art):
    img = open_image(filepath)
    if not img:
        return
    try:
        is_animated = getattr(img, "is_animated", False)
        num_frames = getattr(img, "n_frames", 1)
        text_arts = (
            ["ASCII ART", args.ascii, lambda f, w: to_ascii(f, w, args.color)],
            ["ANSI ART", args.ansi, to_ansi],
        )
        for frame_index in range(num_frames):
            img.seek(frame_index)
            current_frame = img.convert("RGBA")
            art_displayed = False

            if args.ascii or args.ansi:
                print("\033[H\033[2J\033[3J", end="")

            for text, is_active, art_func in text_arts:
                if is_active:
                    print(f"\033[0m{text} Frame: {frame_index + 1}/{num_frames}")
                    print(art_func(current_frame, args.width))
                    art_displayed = True

            # if it is animated
            if art_displayed and is_animated:
                # get the frame duration from the GIF (default 100ms)
                duration = img.info.get("duration", 100) / 1000.0
                time.sleep(duration)
            # convert images (if requested)
            if requested_formats:
                save_requested_format(
                    img, filepath, requested_formats, args.output, frame_index
                )
        # if nothing has been specified, I will proceed with the interactive mode. Only for the first frame
        if not requested_art and not requested_formats:
            img.seek(0)
            interactive_mode(img.convert("RGBA"), filepath)
    finally:
        img.close()


def save_requested_format(img, filepath, formats, output_dir, frame_index):
    for fmt in formats:
        output_file = convert_image(img, filepath, fmt, output_dir, frame_index)
        if output_file:
            print(f"Saved: {output_file} \t{get_file_size(output_file)}")
