# test_splyt.py

import os
import pytest
from unittest.mock import patch, MagicMock
from splyt.core import splyt, process_directory
from splyt.cli import parse_arguments
from splyt.utils import is_image_file
from splyt.config import USAGE_MESSAGE, ERROR_NO_TARGET_IMAGE, SUPPORTED_FORMATS
from PIL import Image

# Test CLI arguments
def test_parse_arguments_valid(monkeypatch):
    monkeypatch.setattr('sys.argv', ['splyt', '3', '3', '1:1', 'image.png', 'output_dir'])
    grid_size, aspect_ratio, target, save_dir, copy_metadata, add_metadata = parse_arguments()
    assert grid_size == (3, 3)
    assert aspect_ratio == (1, 1)
    assert target.endswith('image.png')
    assert save_dir.endswith('output_dir')
    assert copy_metadata is True
    assert add_metadata is True

def test_parse_arguments_options(monkeypatch):
    monkeypatch.setattr('sys.argv', ['splyt', '-cC', 'image.png'])
    grid_size, aspect_ratio, target, save_dir, copy_metadata, add_metadata = parse_arguments()
    assert copy_metadata is False
    assert add_metadata is False

def test_parse_arguments_missing_target(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['splyt', '3', '3'])
    with pytest.raises(SystemExit):
        parse_arguments()
    captured = capsys.readouterr()
    assert ERROR_NO_TARGET_IMAGE in captured.out

# Test is_image_file function
def test_is_image_file_supported(tmp_path):
    img_path = tmp_path / 'test.jpg'
    img = Image.new('RGB', (10, 10))
    img.save(str(img_path))
    assert is_image_file(str(img_path)) is True

def test_is_image_file_unsupported(tmp_path):
    img_path = tmp_path / 'test.xyz'
    img_path.write_text('Not an image')
    assert is_image_file(str(img_path)) is False

def test_is_image_file_nonexistent():
    assert is_image_file('nonexistent.jpg') is False

# Testing splyt function with a sample image
def test_splyt_function(tmp_path):
    img_path = tmp_path / 'test_image.jpg'
    save_dir = tmp_path / 'output'
    img = Image.new('RGB', (100, 100))
    img.save(str(img_path))

    splyt(str(img_path), str(save_dir), grid_size=(2, 2))

    expected_files = [
        'test_image_a1.jpg', 'test_image_b1.jpg',
        'test_image_a2.jpg', 'test_image_b2.jpg'
    ]
    for filename in expected_files:
        assert (save_dir / filename).exists()

# Testing metadata copying
def test_splyt_metadata_copy(tmp_path):
    img_path = tmp_path / 'test_image.jpg'
    save_dir = tmp_path / 'output'
    img = Image.new('RGB', (100, 100))
    img_exif = img.getexif()
    img_exif[271] = 'Test Camera'  # Tag 271 is 'Make'
    img.save(str(img_path), exif=img_exif.tobytes())

    splyt(str(img_path), str(save_dir), grid_size=(1, 1), copy_metadata=True, add_metadata=False)

    output_image_path = save_dir / 'test_image_a1.jpg'
    assert output_image_path.exists()
    with Image.open(str(output_image_path)) as img_out:
        exif = img_out.getexif()
        assert exif
        assert exif[271] == 'Test Camera'

# Testing unsupported image format
def test_splyt_unsupported_format(tmp_path, capsys):
    img_path = tmp_path / 'test_image.xyz'
    img_path.write_text('Not a real image')

    splyt(str(img_path), str(tmp_path))

    captured = capsys.readouterr()
    assert 'not currently supported' in captured.out or 'Cannot identify image file' in captured.out

# Testing process_directory
def test_process_directory(tmp_path):
    img1 = Image.new('RGB', (100, 100))
    img2 = Image.new('RGB', (200, 200))
    input_dir = tmp_path / 'input'
    output_dir = tmp_path / 'output'
    input_dir.mkdir()
    img1_path = input_dir / 'img1.jpg'
    img2_path = input_dir / 'img2.png'
    img1.save(str(img1_path))
    img2.save(str(img2_path))

    process_directory(str(input_dir), str(output_dir), grid_size=(2, 2))

    assert (output_dir / 'img1_a1.jpg').exists()
    assert (output_dir / 'img2_a1.png').exists()
