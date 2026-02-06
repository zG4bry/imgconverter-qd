import pytest
from PIL import Image
from unittest.mock import Mock


@pytest.fixture
def mock_img():
    return Mock(spec=Image.Image)


@pytest.fixture()
def mock_open_image(mocker):
    """Fixture to mock open_image function"""
    return mocker.patch("src.processor.open_image")


@pytest.fixture()
def mock_convert_image(mocker):
    """Fixture to mock convert_image function"""
    return mocker.patch("src.processor.convert_image")


@pytest.fixture()
def mock_getattr(mocker):
    """Fixture to mock getattr function"""
    return mocker.patch("src.processor.getattr")
