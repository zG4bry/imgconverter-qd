import pytest
from src.utils import get_file_size

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