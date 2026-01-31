import pytest
from src.utils import format_normalizer


@pytest.mark.parametrize(
    "raw_formats, requested_formats, expected_output",
    [
        ([], [], set()),
        ([], ["jpg"], set()),
        (["jpg", "jpeg", "png"], ["jpg", "png"], {"jpg", "png"}),
        (["jpg", "jpeg", "png", "svg"], ["jpg", "png", "svg"], {"jpg", "png", "svg"}),
        (["jpg", "jpeg", "png", "svg"], ["jpg", "svg"], {"jpg", "svg"}),
    ],
)
def test_format_normalizer(raw_formats, requested_formats, expected_output):
    assert format_normalizer(raw_formats, requested_formats) == expected_output


def test_format_normalizer_with_duplicates():
    """Test format_normalizer with duplicate formats"""
    raw_formats = ["jpg", "jpeg", "jpg", "png", "png"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    assert result == {"jpg", "png"}


def test_format_normalizer_with_empty_strings():
    """Test format_normalizer with empty strings in raw_formats"""
    raw_formats = ["jpg", "", "png", None, "jpeg"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    assert result == {"jpg", "png"}


def test_format_normalizer_uppercase_formats():
    """Test format_normalizer with uppercase formats (case-insensitive)"""
    raw_formats = ["JPG", "JPEG", "PNG"]
    requested_formats = ["jpg", "png"]
    result = format_normalizer(raw_formats, requested_formats)
    # The function is case-insensitive so uppercase inputs should match
    assert result == {"jpg", "png"}  # Uppercase inputs should be normalized and matched


def test_format_normalizer_nonexistent_formats():
    """Test format_normalizer with formats not in ALL_FORMATS"""
    raw_formats = ["gif", "bmp"]
    requested_formats = ["gif", "bmp"]
    result = format_normalizer(raw_formats, requested_formats)
    # The function adds formats if they're in ALL_FORMATS and raw_formats contains them
    # Since these aren't in ALL_FORMATS but are in both lists, they get added
    assert result == {"gif", "bmp"}
