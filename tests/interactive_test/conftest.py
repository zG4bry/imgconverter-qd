import pytest


@pytest.fixture()
def mock_get_file_size(mocker):
    """Fixture to mock get_file_size function"""
    return mocker.patch("src.interactive.get_file_size")
