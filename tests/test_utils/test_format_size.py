import pytest
from src.utils import format_size

@pytest.mark.parametrize(
    "size_bytes, expected_output",
    [
        # Basic tests
        (None, None),
        (0, "0.00 B"),
        (1, "1.00 B"),
        (999, "999.00 B"),
        (1 * 1024, "1.00 KB"),
        (1024**2, "1.00 MB"),
        (1024**3, "1.00 GB"),
        (7 * (1024**3), "7.00 GB"),
        # Edge cases
        (1024**4, "1024.00 GB"),  # 1 TB
        (1024**5, "1048576.00 GB"),  # 1 PB
        (-1, "-1.00 B"),  # negative size
        (0.5, "0.50 B"),  # decimal size
    ],
)
def test_format_size(size_bytes, expected_output):
    result = format_size(size_bytes)
    assert result == expected_output
