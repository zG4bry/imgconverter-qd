import os
import pytest
from src.processor import process_image_file
from unittest.mock import Mock, call


def test_process_image_file_no_img(mock_open_image):
    filename = os.path.basename("show_header_test.py")
    args = "test"
    requested_formats = "test_format"
    requested_art = "test_art"
    mock_open_image.return_value = None

    assert process_image_file(filename, args, requested_formats, requested_art) == None


def test_process_image_file_ascii_animated(
    mock_open_image,
    mock_to_ascii,
    mock_save_requested_format,
    mock_time_sleep,
):
    args = Mock()
    args.ascii = True
    args.ansi = False
    args.width = 80
    args.color = True
    args.output = "out"

    requested_formats = ["png"]
    requested_art = True
    filepath = "test.gif"

    img = Mock()
    img.is_animated = True
    img.n_frames = 2
    img.info = {"duration": 200}

    frame = Mock()
    img.convert.return_value = frame

    mock_open_image.return_value = img
    mock_to_ascii.return_value = "ASCII_RESULT"

    process_image_file(filepath, args, requested_formats, requested_art)

    mock_open_image.assert_called_once_with(filepath)

    img.seek.assert_has_calls([call(0), call(1)])

    assert img.convert.call_count == 2

    mock_to_ascii.assert_has_calls(
        [
            call(frame, args.width, args.color),
            call(frame, args.width, args.color),
        ]
    )

    mock_save_requested_format.assert_has_calls(
        [
            call(img, filepath, requested_formats, args.output, 0),
            call(img, filepath, requested_formats, args.output, 1),
        ]
    )

    assert mock_time_sleep.call_count == 2
    mock_time_sleep.assert_called_with(0.2)

    img.close.assert_called_once()

def test_process_image_file_no_ascii_no_formats(
    mock_open_image,
    mock_to_ascii,
    mock_save_requested_format,
    mock_time_sleep,
    mock_interactive_mode
):
    args = Mock()
    args.ascii = False
    args.ansi = False
    args.width = 80
    args.color = True
    args.output = "out"

    requested_formats = []
    requested_art = False
    filepath = "test.gif"

    img = Mock()
    img.is_animated = True
    img.n_frames = 2
    img.info = {"duration": 200}

    frame = Mock()
    img.convert.return_value = frame

    mock_open_image.return_value = img
    mock_to_ascii.return_value = "ASCII_RESULT"

    mock_interactive_mode.return_value = "test_file_size"

    process_image_file(filepath, args, requested_formats, requested_art)

    assert mock_open_image.call_count == 1
    assert mock_interactive_mode.call_count == 1
    assert mock_save_requested_format.call_count == 0
    assert mock_time_sleep.call_count == 0

    img.close.assert_called_once()
