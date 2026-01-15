import pytest
from src.utils import format_size


@pytest.mark.parametrize("size_bytes, expected_output",
                          [(0, "0.00 B"),
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
