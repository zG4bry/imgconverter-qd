import os
from src.processor import process_image_file


def test_process_image_file_no_img(mock_img, mock_open_image):
    filename = os.path.basename("show_header_test.py")
    args = "test"
    requested_formats = "test_format"
    requested_art = "test_art"
    mock_open_image.return_value = None

    assert process_image_file(filename, args, requested_formats, requested_art) == None
