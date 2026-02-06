import pytest
from PIL import Image
from src.convert import convert_image
import os


@pytest.mark.parametrize(
    "img_mode, source_path, target_format, output_dir, index, should_skip, expected_filename",
    [
        # Conversioni supportate
        ("RGB", "test.png", "jpg", None, None, False, "test.jpg"),
        ("RGB", "test.png", "jpeg", None, None, False, "test.jpeg"),
        ("RGB", "test.jpg", "png", None, None, False, "test.png"),
        ("RGB", "test.jpg", "webp", None, None, False, "test.webp"),
        # RGBA a JPG (deve convertire in RGB)
        ("RGBA", "test.png", "jpg", None, None, False, "test.jpg"),
        ("RGBA", "test.png", "jpeg", None, None, False, "test.jpeg"),
        # Palette a JPG (deve convertire in RGB)
        ("P", "test.png", "jpg", None, None, False, "test.jpg"),
        ("P", "test.png", "jpeg", None, None, False, "test.jpeg"),
        # Skip quando formato sorgente = target
        ("RGB", "test.jpg", "jpg", None, None, True, None),
        ("RGB", "test.png", "png", None, None, True, None),
        ("RGB", "test.webp", "webp", None, None, True, None),
        ("RGB", "test.jpeg", "jpeg", None, None, True, None),
        # JPEG e JPG sono equivalenti
        ("RGB", "test.jpeg", "jpg", None, None, True, None),
        ("RGB", "test.jpg", "jpeg", None, None, True, None),
        # Con output_dir
        ("RGB", "test.png", "jpg", "output", None, False, "output/test.jpg"),
    ],
)
def test_convert_image_modes(
    tmp_path,
    img_mode,
    source_path,
    target_format,
    output_dir,
    index,
    should_skip,
    expected_filename,
):
    img = Image.new(img_mode, (100, 100), color="red")

    full_output_dir = tmp_path / output_dir if output_dir else tmp_path
    if output_dir:
        full_output_dir.mkdir(parents=True, exist_ok=True)

    if output_dir:
        result = convert_image(
            img, str(tmp_path / source_path), target_format, str(full_output_dir), index
        )
    else:
        result = convert_image(
            img, str(tmp_path / source_path), target_format, None, index
        )

    if should_skip:
        assert result is None
    else:
        assert result is not None
        if output_dir:
            assert result.startswith(str(full_output_dir))
        else:
            assert result.startswith(str(tmp_path))
        assert os.path.exists(result)
        assert os.path.basename(result) == os.path.basename(expected_filename)


def test_convert_image_format_not_supported(tmp_path, capsys):
    img = Image.new("RGB", (100, 100), color="red")
    source_path = str(tmp_path / "test.png")

    result = convert_image(img, source_path, "gif", None, None)

    assert result is None
    captured = capsys.readouterr()
    assert "GIF format not supported" in captured.out


def test_convert_image_os_error(tmp_path, capsys, mocker):
    img = Image.new("RGB", (100, 100), color="red")
    source_path = str(tmp_path / "test.png")

    mocker.patch.object(img, "copy", side_effect=OSError("Test error"))

    result = convert_image(img, source_path, "jpg", None, None)

    assert result is None
    captured = capsys.readouterr()
    assert "Error:" in captured.out


def test_convert_image_value_error(tmp_path, capsys, mocker):
    img = Image.new("RGB", (100, 100), color="red")
    source_path = str(tmp_path / "test.png")

    mocker.patch.object(img, "copy", side_effect=ValueError("Test error"))

    result = convert_image(img, source_path, "jpg", None, None)

    assert result is None
    captured = capsys.readouterr()
    assert "Error:" in captured.out


@pytest.mark.parametrize(
    "is_animated, index, expected_suffix",
    [
        (True, 5, "_5"),  # Entrambe condizioni vere: filename include index
        (True, None, ""),  # is_animated=True ma index=None: filename senza index
        (False, 5, ""),  # is_animated=False: filename senza index anche con index!=None
        (False, None, ""),  # Entrambe condizioni false: filename senza index
    ],
)
def test_convert_image_animated_with_index(
    tmp_path, mocker, is_animated, index, expected_suffix
):
    """Test specifico per il caso is_animated + index.

    Verifica che il filename includa l'index solo quando is_animated=True E index is not None.
    """
    img = Image.new("RGB", (100, 100), color="red")

    # Mock dell'attributo is_animated
    mocker.patch.object(img, "is_animated", is_animated, create=True)

    source_path = str(tmp_path / "test.gif")
    target_format = "png"

    result = convert_image(img, source_path, target_format, None, index)

    assert result is not None
    expected_filename = f"test{expected_suffix}.png"
    assert os.path.basename(result) == expected_filename
    assert os.path.exists(result)
