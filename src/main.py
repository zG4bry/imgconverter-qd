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


def convert_image_format(img: Image, source_path: str, format: str):
    try:
        filename_root = os.path.splitext(source_path)[0]
        filename_output = f"{filename_root}.{format}"

        match format:
            case "jpg" | "jpeg":
                ...
            case "png":
                ...
            case "webp":
                ...
     
    except Exception as e:
        ...

def main():
    if len(sys.argv) < 2:
        print("Errore: Specifica il percorso dell'immagine.")
        sys.exit(1)
    image_path = sys.argv[1]
    img = open_image(image_path)
    if img:
        ...


if __name__ == "__main__":
    main()
