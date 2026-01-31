import pytest
from PIL import Image
from src.convert import to_ascii
from tests.helpers.ascii_helpers import build_expected, rgba_to_la


@pytest.fixture
def mock_resize_img(mocker):
    """Fixture to mock resize_img function"""
    return mocker.patch("src.convert.resize_img")


@pytest.fixture
def img_width():
    return 2


global_pixels = pytest.mark.parametrize(
    "pixels, colored, mode",
    [
        (
            [
                (255, 0, 0, 0),  # Transparent
                (255, 0, 0, 255),  # Red
                (0, 0, 255, 255),  # Blue
                (0, 255, 0, 255),  # Green
            ],
            True,
            "RGBA",
        ),
        (
            [
                (255, 0, 0, 255),  # Red
                (0, 0, 255, 255),  # Blue
                (0, 255, 0, 255),  # Green
                (0, 10, 3, 0),  # Transparent
            ],
            False,
            "LA",
        ),
        (  # Non-transparent pixels
            [
                (255, 0, 0, 255),
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 255, 0, 255),
            ],
            True,
            "RGBA",
        ),
        (
            [
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 255, 0, 255),
                (0, 10, 3, 255),
            ],
            False,
            "LA",
        ),
    ],
)


@global_pixels
def test_to_ascii_colored(pixels, colored, mode, mock_resize_img, img_width, mocker):

    expected = build_expected(pixels, img_width, colored)

    mock_converted_img = mocker.Mock(spec=Image.Image)
    if mode == "LA":
        mock_pixels = rgba_to_la(pixels)
    else:
        mock_pixels = pixels
    mock_converted_img.getdata.return_value = mock_pixels

    mock_resized_img = mocker.Mock(spec=Image.Image)
    mock_resized_img.convert.return_value = mock_converted_img
    mock_resize_img.return_value = mock_resized_img

    mock_input_img = mocker.Mock(spec=Image.Image)

    result = to_ascii(mock_input_img, width=img_width, colored=colored)

    assert result == expected
    mock_resized_img.convert.assert_called_once_with(mode)
