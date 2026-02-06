import os
from src.processor import save_requested_format

def test_save_requested_format_no_output(mock_convert_image,mock_img, capsys):
    mock_convert_image.return_value = None
    img = mock_img
    filename = os.path.basename("show_header_test.py")
    formats = ["test_formats_1","test_formats_2"]
    output_dir = "test_output_dir"
    frame_index = 2

    save_requested_format(img, filename, formats, output_dir, frame_index)

    captured = capsys.readouterr().out

    assert captured == ""
    assert mock_convert_image.call_count == len(formats)


def test_save_requested_format_success(mock_convert_image,mock_img, capsys):
    mock_convert_image.return_value = "test_output_file"
    img = mock_img
    filename = os.path.basename("show_header_test.py")
    formats = ["test_formats_1","test_formats_2"]
    output_dir = "test_output__dir"
    frame_index = 2

    save_requested_format(img, filename, formats, output_dir, frame_index)

    captured = capsys.readouterr().out

    assert f"Saved:" in captured
    assert mock_convert_image.call_count == len(formats)