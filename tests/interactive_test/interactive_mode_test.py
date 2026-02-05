from src.interactive import interactive_mode
from unittest.mock import call


def test_interactive_mode_all_kept(
    mock_show_header,
    mock_show_and_create_previews,
    mock_parse_user_choice,
    mock_os_remove,
    mock_img,
    mock_generated_files_ok,
    capsys,
):
    mock_show_and_create_previews.return_value = mock_generated_files_ok
    mock_parse_user_choice.return_value = "all"

    interactive_mode(mock_img, "file.png")

    output = capsys.readouterr().out
    assert "All generated files kept." in output
    mock_os_remove.assert_not_called()


def test_interactive_mode_delete_all(
    mock_show_header,
    mock_show_and_create_previews,
    mock_parse_user_choice,
    mock_os_remove,
    mock_img,
    mock_generated_files_ok,
    capsys,
):
    mock_show_and_create_previews.return_value = mock_generated_files_ok
    mock_parse_user_choice.side_effect = ["none"]

    interactive_mode(mock_img, "file.png")

    assert mock_os_remove.call_count == len(mock_generated_files_ok)
    calls = [call(value[0]) for value in mock_generated_files_ok.values()]
    mock_os_remove.assert_has_calls(
        calls,
        any_order=True,
    )
