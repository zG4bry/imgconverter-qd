import pytest
from src.utils import (
    format_size,
    get_source_ext,
    format_normalizer,
    get_file_size,
    resize_img,
    open_image,
)
from src.consts import DEFAULT_WIDTH, CORRECTION_FACTOR
from PIL import Image


@pytest.mark.parametrize(
    "size_bytes, expected_output",
    [
        # Basic tests
        (None, None),
        (0, "0.00 B"),
        (1, "1.00 B"),
        (999, "999.00 B"),
        (1 * 1024, "1.00 KB"),
        (1024**2, "1.00 MB"),
        (1024**3, "1.00 GB"),
        (7 * (1024**3), "7.00 GB"),
        # Edge cases
        (1024**4, "1024.00 GB"),  # 1 TB
        (1024**5, "1048576.00 GB"),  # 1 PB
        (-1, "-1.00 B"),  # negative size
        (0.5, "0.50 B"),  # decimal size
    ],
)
def test_format_size(size_bytes, expected_output):
    result = format_size(size_bytes)
    assert result == expected_output


@pytest.mark.parametrize(
    "source_path, expected_output",
    [
        # Basic tests
        ("/bla/blabla/boh.exe", "exe"),
        ("/bla/boh.jpg", "jpg"),
        ("/bla/boh.svg", "svg"),
        ("/boh.test", "test"),
        # Edge cases
        ("relative/path/file.jpg", "jpg"),
        ("./file.png", "png"),
        ("file", ""),  # no extension
        ("file.", ""),  # empty extension
        (".hidden", ""),  # hidden file with no extension
        ("path.with.dots/file.tar.gz", "gz"),
        ("UPPERCASE.JPG", "jpg"),  # uppercase extension
        ("MixedCase.PnG", "png"),  # mixed case extension
    ],
)
def test_get_source_ext(source_path, expected_output):
    assert get_source_ext(source_path) == expected_output


@pytest.mark.parametrize(
    "raw_formats, requested_formats, expected_output",
    [
        ([], [], set()),
        ([], ["jpg"], set()),
        (["jpg", "jpeg", "png"], ["jpg", "png"], {"jpg", "png"}),
        (["jpg", "jpeg", "png", "svg"], ["jpg", "png", "svg"], {"jpg", "png", "svg"}),
        (["jpg", "jpeg", "png", "svg"], ["jpg", "svg"], {"jpg", "svg"}),
    ],
)
def test_format_normalizer(raw_formats, requested_formats, expected_output):
    assert format_normalizer(raw_formats, requested_formats) == expected_output


def test_get_file_size_file_not_exists(mocker):
    """Test get_file_size when file doesn't exist"""
    mocker.patch("os.path.exists", return_value=False)
    result = get_file_size("/nonexistent/file.jpg")
    assert result is None


def test_get_file_size_file_exists(mocker):
    """Test get_file_size when file exists"""
    mock_size = 1024
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.path.getsize", return_value=mock_size)
    result = get_file_size("/existent/file.jpg")
    assert result == "1.00 KB"


@pytest.mark.parametrize(
    "w, h",
    [(100, 200), (200, 100), (500, 500), (10, 20)],
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


def test_format_normalizer_with_duplicates():
    """Test format_normalizer with duplicate formats"""
    raw_formats = ["jpg", "jpeg", "jpg", "png", "png"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    assert result == {"jpg", "png"}


def test_format_normalizer_with_empty_strings():
    """Test format_normalizer with empty strings in raw_formats"""
    raw_formats = ["jpg", "", "png", None, "jpeg"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    assert result == {"jpg", "png"}


def test_format_normalizer_uppercase_formats():
    """Test format_normalizer with uppercase formats (case-insensitive)"""
    raw_formats = ["JPG", "JPEG", "PNG"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    # The function is case-insensitive so uppercase inputs should match
    assert result == {"jpg", "png"}  # Uppercase inputs should be normalized and matched


def test_format_normalizer_nonexistent_formats():
    """Test format_normalizer with formats not in ALL_FORMATS"""
    raw_formats = ["gif", "bmp"]
    requested_formats = ["gif", "bmp"]
    result = format_normalizer(raw_formats, requested_formats)
    # The function adds formats if they're in ALL_FORMATS and raw_formats contains them
    # Since these aren't in ALL_FORMATS but are in both lists, they get added
    assert result == {"gif", "bmp"}
