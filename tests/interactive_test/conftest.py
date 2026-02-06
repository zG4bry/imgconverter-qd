import pytest
from PIL import Image
from unittest.mock import Mock


@pytest.fixture
def mock_img():
    return Mock(spec=Image.Image)


@pytest.fixture
def mock_generated_files_ok():
    return {
        "jpg": ("/tmp/img.jpg",),
        "png": ("/tmp/img.png",),
        "webp": ("/tmp/img.webp",),
    }


@pytest.fixture()
def mock_get_file_size(mocker):
    """Fixture to mock get_file_size function"""
    return mocker.patch("src.interactive.get_file_size")


@pytest.fixture()
def mock_convert_image(mocker):
    """Fixture to mock convert_image function"""
    return mocker.patch("src.interactive.convert_image")


@pytest.fixture()
def mock_show_header(mocker):
    """Fixture to mock show_header function"""
    return mocker.patch("src.interactive.show_header")


@pytest.fixture()
def mock_parse_user_choice(mocker):
    """Fixture to mock parse_user_choice function"""
    return mocker.patch("src.interactive.parse_user_choice")


@pytest.fixture()
def mock_os_remove(mocker):
    """Fixture to mock os.remove function"""
    return mocker.patch("src.interactive.os.remove")


@pytest.fixture
def mock_show_and_create_previews(mocker):
    """Fixture to mock show_and_create_previews function"""
    return mocker.patch("src.interactive.show_and_create_previews")


@pytest.fixture
def mock_input(mocker):
    """Fixture to mock input function"""
    return mocker.patch("src.interactive.input")
