import pytest
import os
from utils import open_image, get_source_ext
from src.convert import convert_image


@pytest.mark.parametrize(
    "source_path,target_format,output_dir",
    [
        ("tests/images/200x200.jpeg", "webp", "tests"),
        ("tests/images/200x200.jpeg", "jpeg", "tests"),
        ("tests/images/200x200.jpg", "jpeg", "tests"),
        ("tests/images/200x200.jpg", "random", "tests"),
        ("tests/images/550x368.webp", "jpeg", None),
    ],
)
def test_convert_image(source_path, target_format, output_dir, capsys):
    if get_source_ext(source_path) == target_format:
        try:
            img = open_image(source_path)
            output = convert_image(
                img, source_path, target_format, output_dir, index=None
            )
            assert output is None
            return
        except Exception:
            assert False

    try:
        img = open_image(source_path)
        output = convert_image(img, source_path, target_format, output_dir, index=None)
        if output is None:
            captured = capsys.readouterr()
            assert captured.out in [
                f"Skipping: '{source_path}' is already in {target_format.upper()} format.\n",
                f"{target_format.upper()} format not supported\n",
            ]
        else:
            assert os.path.isfile(output)
            os.remove(output)
    except Exception:
        assert False
