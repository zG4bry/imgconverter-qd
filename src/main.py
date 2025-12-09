import sys, argparse, os
from PIL import Image


def open_image(image_path: str):
    try:
        with Image.open(image_path) as img:
            return img.copy()
    except FileNotFoundError:
        print("File non trovato\n")
        sys.exit(1)
    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)


def convert_image_format(img: Image, source_path: str, out_format: str):
    filename_root = os.path.splitext(source_path)[0]
    # filename_ext = os.path.splitext(source_path)[1].lstrip(".")
    filename_output = f"{filename_root}.{out_format}"
    print(f"Converto {source_path} in {filename_root}.{out_format}\n")
    try:
        match out_format:
            case "jpg" | "jpeg":
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(filename_output, quality=90)
                return True
            case "png":
                img.save(filename_output, optimize=True)
                return True
            case "webp":
                img.save(filename_output)
                return True
            case _:
                print("Formato non supportato\n")
                return False
    except (OSError, ValueError) as e:
        print(f"Errore: {e}")


def main():

    if len(sys.argv) < 2:
        print("Errore: Specifica il percorso dell'immagine.")
        sys.exit(1)
    image_path = sys.argv[1]
    img = open_image(image_path)
    if img:
        if not convert_image_format(
            img, image_path, "jpg"
        ):  # formato momentaneo, bisogna implementare flags con argparse
            sys.exit(1)
        else: 
            print("Immagine convertita correttamente!")


if __name__ == "__main__":
    main()
