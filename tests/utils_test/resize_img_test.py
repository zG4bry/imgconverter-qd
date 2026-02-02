import pytest
from PIL import Image
from src.utils import resize_img
from src.consts import DEFAULT_WIDTH, CORRECTION_FACTOR


@pytest.mark.parametrize(
    "w, h",
    [
        (100, 200),
        (200, 100),
        (500, 500),
        (10, 20),
    ],
)
def test_resize_img_default_width(w, h):
    """Test resize_img with default width"""
    img = Image.new("RGB", (w, h))

    resized = resize_img(img)
    expected_width = DEFAULT_WIDTH
    expected_height = int(DEFAULT_WIDTH * (h / w) * CORRECTION_FACTOR)  # 82

    assert resized.size == (expected_width, expected_height)


@pytest.mark.parametrize(
    "w, h, custom_width",
    [
        (100, 200, 50),
        (200, 100, 150),
        (500, 500, 75),
        (10, 20, 25),
    ],
)
def test_resize_img_custom_width(w, h, custom_width):
    """Test resize_img with custom width"""
    img = Image.new("RGB", (w, h))

    resized = resize_img(img, custom_width)
    expected_height = int(custom_width * (h / w) * CORRECTION_FACTOR)

    assert resized.size == (custom_width, expected_height)
