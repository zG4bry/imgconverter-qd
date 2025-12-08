import sys
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore: Specifica il percorso dell'immagine.")
        sys.exit(1)
    image_path = sys.argv[1]
    img = open_image(image_path)
    if img:
        ...