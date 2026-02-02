import pytest


@pytest.fixture
def mock_resize_img(mocker):
    """Fixture to mock resize_img function"""
    return mocker.patch("src.convert.resize_img")


@pytest.fixture
def img_width():
    return 2


@pytest.fixture(
    params=[
        (
            [
                (255, 0, 0, 0),  # Transparent
                (255, 0, 0, 255),  # Red
                (0, 0, 255, 255),  # Blue
                (0, 255, 0, 255),  # Green
            ],
            True,
            "RGBA",
        ),
        (
            [
                (255, 0, 0, 255),  # Red
                (0, 0, 255, 255),  # Blue
                (0, 255, 0, 255),  # Green
                (0, 10, 3, 0),  # Transparent
            ],
            False,
            "LA",
        ),
        (  # Non-transparent pixels
            [
                (255, 0, 0, 255),
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 255, 0, 255),
            ],
            True,
            "RGBA",
        ),
        (
            [
                (255, 0, 0, 255),
                (0, 0, 255, 255),
                (0, 255, 0, 255),
                (0, 10, 3, 255),
            ],
            False,
            "LA",
        ),
    ],
)
def image_case(request):
    pixels, colored, mode = request.param
    return pixels, colored, mode
