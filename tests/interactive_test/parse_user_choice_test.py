import pytest
from src.interactive import parse_user_choice


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ("", ""),
        ("    ", ""),
        ("\t  JPG   WEBP \n", "jpg   webp"),
        (" JPG_1; WEBP-2 ", "jpg_1; webp-2"),
    ],
)
def test_parse_user_choice_empty_input(test_input, mock_input, expected_output):
    mock_input.return_value = test_input
    result = parse_user_choice()
    assert result == expected_output
