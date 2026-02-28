# ImgConverter-QD

`ImgConverter-QD` is a fast and versatile command-line tool for converting images into various formats, generating ASCII/ANSI art, and comparing file sizes in an interactive mode.

## Features

- 🖼️ **Image Conversion**: Convert images to **JPG**, **PNG**, and **WebP** formats.
- 🎨 **ASCII/ANSI Art**: Generate text-based art from your images with full color support.
- ⚡ **Interactive Mode**: Preview and compare file sizes for different formats before saving.
- 🎞️ **Animation Support**: Handles animated GIFs by processing each frame individually.
- 📂 **Batch Processing**: Supports multiple image paths for bulk conversion.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zG4bry/imgconverter-qd.git
   cd imgconverter-qd
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Conversion

To convert one or more images, specify the output formats you want:

```bash
python main.py path/to/image1.jpg path/to/image2.png --png --webp
```

### ASCII/ANSI Art

Generate and display ASCII or ANSI art in your terminal:

```bash
# ASCII art
python main.py path/to/image.jpg --ascii

# ANSI art (with color)
python main.py path/to/image.jpg --ansi

# Colored ASCII art
python main.py path/to/image.jpg --ascii --color

# Adjust the width of the art
python main.py path/to/image.jpg --ascii --width 120
```

### Interactive Mode

If you run the tool with an image path but without specifying any output format or art type, it will start in interactive mode:

```bash
python main.py path/to/image.jpg
```

In this mode, `ImgConverter-QD` will generate temporary previews in all supported formats (JPG, PNG, WebP) and show you a comparison of the file sizes. You can then choose which files to keep.

### Options

```bash
usage: main.py [-h] [-o OUTPUT] [--jpg] [--png] [--webp] [--ascii] [--ansi] [-w WIDTH] [-c] image_paths [image_paths ...]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Destination folder for converted files.

conversion formats:
  --jpg, --jpeg         converts the image to JPG format
  --png                 converts the image to PNG format
  --webp                converts the image to WebP format

text Art (ASCII/ANSI):
  --ascii               print ASCII Art version
  --ansi                print ANSI Color Art version
  -w WIDTH, --width WIDTH
                        output width art (default: 90)
  -c, --color           enable colored ASCII output (only with --ascii)
```
