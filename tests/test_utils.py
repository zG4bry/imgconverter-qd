import pytest
from src.utils import format_size


@pytest.mark.parametrize("size_bytes, expected_output", [(0, "0.00 B"), (1, "1.00 B")])
def test_format_size(size_bytes, expected_output):
    result = format_size(size_bytes)
    assert result == expected_output
