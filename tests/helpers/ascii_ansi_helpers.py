from src.consts import ASCII_CHARS, CHARACTER

# ASCII HELPERS

def ascii_for_luminance(l: int) -> str:
    n = len(ASCII_CHARS)
    index = int((l * (n - 1)) / 255)
    return ASCII_CHARS[index]


def pixel_to_ascii(pixel, colored=True):
    # pixel is (r,g,b,a)
    r, g, b, a = pixel
    if a == 0:
        return " "
    l = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    char = ascii_for_luminance(l)
    if colored:
        return f"\033[38;2;{r};{g};{b}m{char}"
    else:
        return char


def build_ascii_expected(pixels, width, colored=True):
    out = ""
    for i, pixel in enumerate(pixels):
        out += pixel_to_ascii(pixel, colored=colored)
        if (i + 1) % width == 0:
            out += "\n"
    return out


def rgba_to_la(pixels):
    """Converte una lista di pixel RGBA in LA (luminance, alpha)"""
    return [(int(0.2126 * r + 0.7152 * g + 0.0722 * b), a) for r, g, b, a in pixels]

# ANSI HELPERS

def pixel_to_ansi(pixel):
    # pixel is (r,g,b,a)
    r, g, b, a = pixel
    if a == 0:
        return "\033[0m "
    else:
        return f"\033[38;2;{r};{g};{b}m{CHARACTER}"


def build_ansi_expected(pixels, width):
    out = ""
    for i, pixel in enumerate(pixels):
        out += pixel_to_ansi(pixel)
        if (i + 1) % width == 0:
            out += "\033[0m\n"
    out += "\033[0m"
    return out
