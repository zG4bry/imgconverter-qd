import pytest
from src.utils import format_size, get_source_ext, format_normalizer

@pytest.mark.parametrize("size_bytes, expected_output",
                          [(None, None),
                           (0, "0.00 B"),
                           (1, "1.00 B"),
                           (999, "999.00 B"),
                           (1*1024, "1.00 KB"),
                           (1024**2, "1.00 MB"),
                           (1024**3, "1.00 GB"),
                           (7*(1024**3), "7.00 GB")
                           ])
def test_format_size(size_bytes, expected_output):
    result = format_size(size_bytes)
    assert result == expected_output

@pytest.mark.parametrize("source_path, expected_output",
                         [("/bla/blabla/boh.exe","exe"),
                          ("/bla/boh.jpg","jpg"),
                          ("/bla/boh.svg","svg"),
                          ("/boh.test","test")])
def test_get_source_ext(source_path, expected_output):
    assert get_source_ext(source_path) == expected_output

@pytest.mark.parametrize("raw_formats, requested_formats, expected_output",
                         [([],[],set()),
                          ([],["jpg"],set()),
                          (["jpg","jpeg","png"],["jpg","png"],{"jpg","png"}),
                          (["jpg","jpeg","png","svg"],["jpg","png","svg"],{"jpg","png","svg"}),
                          (["jpg","jpeg","png","svg"],["jpg","svg"],{"jpg","svg"})])
def test_format_normalizer(raw_formats, requested_formats, expected_output):
    assert format_normalizer(raw_formats, requested_formats) == expected_output