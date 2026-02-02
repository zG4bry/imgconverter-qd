import pytest
from src.utils import get_source_ext


@pytest.mark.parametrize(
    "source_path, expected_output",
    [
        # Basic tests
        ("/bla/blabla/boh.exe", "exe"),
        ("/bla/boh.jpg", "jpg"),
        ("/bla/boh.svg", "svg"),
        ("/boh.test", "test"),
        # Edge cases
        ("relative/path/file.jpg", "jpg"),
        ("./file.png", "png"),
        ("file", ""),  # no extension
        ("file.", ""),  # empty extension
        (".hidden", ""),  # hidden file with no extension
        ("path.with.dots/file.tar.gz", "gz"),
        ("UPPERCASE.JPG", "jpg"),  # uppercase extension
        ("MixedCase.PnG", "png"),  # mixed case extension
    ],
)
def test_get_source_ext(source_path, expected_output):
    assert get_source_ext(source_path) == expected_output
