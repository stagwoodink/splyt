# tests/test_splyt.py

import os
import shutil
import tempfile
from splyt.core import splyt, process_directory
from splyt.utils import VALID_GRID_SIZES, get_grid_dimensions
from PIL import Image
import pytest

# Sample images directory
TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'test_images')

@pytest.fixture(scope='module')
def test_images():
    """
    Collect all test images from the tests/test_images/ directory.
    """
    image_paths = []
    for i in range(1, 12):  # Assuming images are named image_1.png to image_11.png
        image_name = f"image_{i}.png"
        image_path = os.path.join(TEST_IMAGES_DIR, image_name)
        if os.path.exists(image_path):
            image_paths.append(image_path)
    return image_paths

def test_splyt_basic(test_images):
    for image_path in test_images:
        with tempfile.TemporaryDirectory() as tmpdir:
            save_dir = os.path.join(tmpdir, 'output')
            grid_size = 4

            # Run the splyt function
            splyt(image_path, save_dir, grid_size)

            # Find the subdirectory created by splyt
            output_dirs = [
                d for d in os.listdir(save_dir)
                if os.path.isdir(os.path.join(save_dir, d))
            ]
            assert len(output_dirs) == 1, f"No output directory found for {os.path.basename(image_path)}."
            split_dir = os.path.join(save_dir, output_dirs[0])

            # List the split images
            output_files = os.listdir(split_dir)
            expected_splits = get_expected_splits(image_path, grid_size)
            assert len(output_files) == expected_splits, f"Incorrect number of split images generated for {os.path.basename(image_path)}."

def test_splyt_all_grid_sizes(test_images):
    for image_path in test_images:
        with tempfile.TemporaryDirectory() as tmpdir:
            for grid_size in VALID_GRID_SIZES:
                save_dir = os.path.join(tmpdir, f'output_{grid_size}')
                splyt(image_path, save_dir, grid_size)

                # Find the subdirectory created by splyt
                output_dirs = [
                    d for d in os.listdir(save_dir)
                    if os.path.isdir(os.path.join(save_dir, d))
                ]
                assert len(output_dirs) == 1, f"No output directory found for grid size {grid_size} and image {os.path.basename(image_path)}."
                split_dir = os.path.join(save_dir, output_dirs[0])

                # List the split images
                output_files = os.listdir(split_dir)
                expected_splits = get_expected_splits(image_path, grid_size)
                assert len(output_files) == expected_splits, f"Grid size {grid_size}: Incorrect number of split images for {os.path.basename(image_path)}."

def get_expected_splits(image_path, grid_size):
    """
    Helper function to calculate the expected number of splits based on image dimensions and grid size.
    """
    with Image.open(image_path) as img:
        width, height = img.size
    if grid_size in {2, 3}:
        return grid_size
    else:
        num_cols, num_rows = get_grid_dimensions(grid_size, width, height)
        return num_cols * num_rows

def test_splyt_metadata(test_images):
    for image_path in test_images:
        with tempfile.TemporaryDirectory() as tmpdir:
            save_dir = os.path.join(tmpdir, 'output')
            grid_size = 2

            # Run the splyt function with metadata copying
            splyt(image_path, save_dir, grid_size, copy_metadata=True, add_metadata=True)

            # Find the subdirectory created by splyt
            output_dirs = [
                d for d in os.listdir(save_dir)
                if os.path.isdir(os.path.join(save_dir, d))
            ]
            assert len(output_dirs) == 1, f"No output directory found for {os.path.basename(image_path)}."
            split_dir = os.path.join(save_dir, output_dirs[0])

            output_files = os.listdir(split_dir)
            for file in output_files:
                file_path = os.path.join(split_dir, file)
                with Image.open(file_path) as img:
                    # Check for custom metadata
                    metadata = img.info
                    format_lower = img.format.lower()
                    if format_lower == 'png':
                        assert 'Comment' in metadata, f"Custom metadata not found in image {file}."
                        assert 'Created using Splyt' in metadata['Comment'], "Custom metadata content incorrect."
                    elif format_lower in {'jpeg', 'jpg'}:
                        exif_data = img.getexif()
                        user_comment = exif_data.get(0x9286)
                        assert user_comment, f"Custom metadata not found in image {file}."
                        assert 'Created using Splyt' in user_comment, "Custom metadata content incorrect."
                    else:
                        # For other formats, you can add appropriate checks
                        pass

def test_splyt_no_metadata(test_images):
    for image_path in test_images:
        with tempfile.TemporaryDirectory() as tmpdir:
            save_dir = os.path.join(tmpdir, 'output')
            grid_size = 2

            # Run the splyt function without metadata copying
            splyt(image_path, save_dir, grid_size, copy_metadata=False, add_metadata=False)

            # Find the subdirectory created by splyt
            output_dirs = [
                d for d in os.listdir(save_dir)
                if os.path.isdir(os.path.join(save_dir, d))
            ]
            assert len(output_dirs) == 1, f"No output directory found for {os.path.basename(image_path)}."
            split_dir = os.path.join(save_dir, output_dirs[0])

            output_files = os.listdir(split_dir)
            for file in output_files:
                file_path = os.path.join(split_dir, file)
                with Image.open(file_path) as img:
                    metadata = img.info
                    format_lower = img.format.lower()
                    if format_lower == 'png':
                        assert 'Comment' not in metadata, f"Metadata should not be present in image {file}."
                    elif format_lower in {'jpeg', 'jpg'}:
                        exif_data = img.getexif()
                        user_comment = exif_data.get(0x9286)
                        assert not user_comment, f"Metadata should not be present in image {file}."
                    else:
                        # For other formats, you can add appropriate checks
                        pass

def test_process_directory(test_images):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a directory with the test images
        images_dir = os.path.join(tmpdir, 'images')
        os.makedirs(images_dir)
        for image_path in test_images:
            shutil.copy(image_path, images_dir)

        save_dir = os.path.join(tmpdir, 'output')

        # Process the directory
        process_directory(images_dir, save_dir, grid_size=3, copy_metadata=False, add_metadata=False)

        # Check that output directories were created for each image
        output_dirs = [
            d for d in os.listdir(save_dir)
            if os.path.isdir(os.path.join(save_dir, d))
        ]
        assert len(output_dirs) == len(test_images), "Incorrect number of output directories."

        # Check contents of each output directory
        for image_file in os.listdir(images_dir):
            image_name, _ = os.path.splitext(image_file)
            split_dir_name = f"{image_name[:9]}_split"
            output_dir = os.path.join(save_dir, split_dir_name)
            assert os.path.exists(output_dir), f"Output directory {output_dir} does not exist."
            output_files = os.listdir(output_dir)
            expected_splits = get_expected_splits(os.path.join(images_dir, image_file), 3)
            assert len(output_files) == expected_splits, f"Incorrect number of split images in {output_dir}."

def test_splyt_invalid_image():
    invalid_image_path = os.path.join(TEST_IMAGES_DIR, 'invalid_image.txt')
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create an invalid image file
        with open(invalid_image_path, 'w') as f:
            f.write('This is not an image')

        # Run the splyt function and expect a ValueError due to invalid image
        with pytest.raises(ValueError, match="is not a valid image"):
            splyt(invalid_image_path, tmpdir)

