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
):
    mock_show_and_create_previews.return_value = mock_generated_files_ok
    mock_parse_user_choice.side_effect = ["none", "None", "NONE", ""]

    i = 0
    for effect in mock_parse_user_choice.side_effect:
        i += 1
        interactive_mode(mock_img, "file.png")

        assert mock_os_remove.call_count == len(mock_generated_files_ok) * i
        calls = [call(value[0]) for value in mock_generated_files_ok.values()]
        mock_os_remove.assert_has_calls(
            calls,
            any_order=True,
        )


def test_interactive_mode_keep_png_only(
    mock_show_header,
    mock_show_and_create_previews,
    mock_parse_user_choice,
    mock_os_remove,
    mock_img,
    mock_generated_files_ok,
    capsys,
):
    mock_show_and_create_previews.return_value = mock_generated_files_ok
    mock_parse_user_choice.side_effect = ["png"]

    interactive_mode(mock_img, "file.png")

    mock_os_remove.assert_has_calls(
        [
            call("/tmp/img.jpg"),
            call("/tmp/img.webp"),
        ],
        any_order=True,
    )
    assert mock_os_remove.call_count == 2

    out = capsys.readouterr().out
    assert "Kept: png" in out


def test_interactive_mode_os_remove_error(
    mock_show_header,
    mock_show_and_create_previews,
    mock_parse_user_choice,
    mock_os_remove,
    mock_img,
    mock_generated_files_ok,
    capsys,
):
    mock_show_and_create_previews.return_value = mock_generated_files_ok
    mock_parse_user_choice.return_value = "none"

    mock_os_remove.side_effect = OSError("permission denied")

    interactive_mode(mock_img, "file.png")

    out = capsys.readouterr().out
    assert "Could not delete" in out
