from PIL import Image
from src.convert import to_ansi
from tests.helpers.ascii_ansi_helpers import build_ansi_expected


def test_to_ansi_colored(image_case, mock_resize_img, img_width, mocker):
    pixels, _, _ = image_case
    expected = build_ansi_expected(pixels, img_width)

    mock_converted_img = mocker.Mock(spec=Image.Image)
    mock_converted_img.getdata.return_value = pixels

    mock_resized_img = mocker.Mock(spec=Image.Image)
    mock_resized_img.convert.return_value = mock_converted_img
    mock_resize_img.return_value = mock_resized_img

    mock_input_img = mocker.Mock(spec=Image.Image)

    result = to_ansi(mock_input_img, width=img_width)

    assert result == expected
    mock_resized_img.convert.assert_called_once_with("RGBA")
