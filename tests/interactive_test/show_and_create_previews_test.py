import os
from src.consts import ALL_FORMATS
from src.interactive import show_and_create_previews

filename = os.path.basename("fake_test.py")
output_dir = os.path.basename("./")


def test_show_and_create_previews_full_success(
    mock_img, mock_convert_image, mock_get_file_size, capsys
):

    mock_get_file_size.return_value = "test KB"
    mock_convert_image.return_value = "mocked_ok"
    result = show_and_create_previews(mock_img, filename, output_dir)
    expected_output = {
        fmt: (mock_convert_image.return_value, mock_get_file_size.return_value)
        for fmt in ALL_FORMATS
    }
    mock_convert_image.assert_called()
    assert expected_output == result


def test_show_and_create_previews_one_fail(
    mock_img,mock_convert_image, mock_get_file_size, capsys
):

    mock_get_file_size.return_value = "test KB"
    # mocking fail on last interation
    test_s = [
        fmt if i != len(ALL_FORMATS) - 1 else None for i, fmt in enumerate(ALL_FORMATS)
    ]
    mock_convert_image.side_effect = test_s

    expected_output = {
        fmt: (test_s[i], mock_get_file_size.return_value)
        for i, fmt in enumerate(ALL_FORMATS[:-1])
    }

    result = show_and_create_previews(mock_img, filename, output_dir)

    mock_convert_image.assert_called()
    assert expected_output == result


def test_show_and_create_previews_fail(mock_img,mock_convert_image, capsys):
    mock_convert_image.return_value = None
    show_and_create_previews(mock_img, filename, output_dir)

    expected_output = []

    mock_convert_image.assert_called()
    assert expected_output == []
