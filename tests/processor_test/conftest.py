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
def mock_time_sleep(mocker):
    """Fixture to mock time.sleep function"""
    return mocker.patch("src.processor.time.sleep")


@pytest.fixture()
def mock_save_requested_format(mocker):
    """Fixture to mock save_requested_format function"""
    return mocker.patch("src.processor.save_requested_format")


@pytest.fixture()
def mock_to_ascii(mocker):
    """Fixture to mock to_ascii function"""
    return mocker.patch("src.processor.to_ascii")


@pytest.fixture()
def mock_interactive_mode(mocker):
    """Fixture to mock mock_interactive_mode function"""
    return mocker.patch("src.processor.interactive_mode")
