import os
from src.interactive import show_header


def test_show_header_outputs_expected_format(mock_get_file_size, capsys, mocker):

    filename = os.path.basename("show_header_test.py")
    internal_width = 22 + len(os.path.basename(filename))
    separator = "-" * internal_width

    mock_get_file_size.return_value = "123 KB"

    show_header(filename)
    captured = capsys.readouterr().out

    expected_output = (
        f"\n{separator}\n"
        f"INTERACTIVE MODE for: {filename}\n"
        f"Original Size: {'123 KB':>{internal_width - 15}}\n"
        f"{separator}\n"
    )

    mock_get_file_size.assert_called()
    assert captured == expected_output
