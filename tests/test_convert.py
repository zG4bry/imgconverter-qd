import pytest
import os
from PIL import Image
from utils import open_image, get_source_ext
from src.convert import convert_image

""" @pytest.mark.parametrize("source_path,target_format,output_dir", 
                         [("tests/images/200x200.jpeg","webp","tests"),
                          ("tests/images/200x200.jpeg","jpeg","tests"),
                          ("tests/images/200x200.jpg","jpeg","tests"),
                          ("tests/images/550x368.webp","jpeg",None)
                          ],
                         )"""


@pytest.mark.parametrize(
    "source_path,target_format,output_dir",
    [
        ("tests/images/200x200.jpeg", "webp", "tests"),
        ("tests/images/200x200.jpeg", "jpeg", "tests"),
        ("tests/images/550x368.webp", "jpeg", None),
    ],
)
def test_convert_image(source_path, target_format, output_dir):
    if get_source_ext(source_path) == target_format:
        try:
            img = open_image(source_path)
            output = convert_image(
                img, source_path, target_format, output_dir, index=None
            )
            assert output == None
            return
        except:
            assert False

    try:
        img = open_image(source_path)
    except:
        assert False

    output = convert_image(img, source_path, target_format, output_dir, index=None)
    assert os.path.isfile(output)
    os.remove(output)
