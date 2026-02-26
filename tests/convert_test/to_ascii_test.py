from PIL import Image
from src.convert import to_ascii
from tests.helpers.ascii_ansi_helpers import build_ascii_expected, rgba_to_la


def test_to_ascii_colored(image_case, mock_resize_img, img_width, mocker):
    pixels, colored, mode = image_case
    expected = build_ascii_expected(pixels, img_width, colored)

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
