import pytest
from PIL import Image
from src.utils import open_image


def test_open_image_file_not_found(mocker):
    """Test open_image when file doesn't exist"""
    mocker.patch("PIL.Image.open", side_effect=FileNotFoundError())

    with pytest.raises(SystemExit) as exc_info:
        open_image("/nonexistent/image.jpg")
    assert exc_info.value.code == 1


def test_open_image_os_error(mocker):
    """Test open_image when there's an OS error"""
    mocker.patch("PIL.Image.open", side_effect=OSError("Corrupt image"))

    with pytest.raises(SystemExit) as exc_info:
        open_image("/corrupt/image.jpg")
    assert exc_info.value.code == 1


def test_open_image_success(mocker):
    """Test open_image successful opening"""
    mock_img = mocker.Mock(spec=Image.Image)
    mock_open = mocker.patch("PIL.Image.open", return_value=mock_img)

    result = open_image("/valid/image.jpg")
    mock_open.assert_called_once_with("/valid/image.jpg")
    assert result == mock_img
