import pytest
from PIL import Image
from unittest.mock import Mock

@pytest.fixture
def mock_img():
    return Mock(spec=Image.Image)

@pytest.fixture 
def mock_generated_files():
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
