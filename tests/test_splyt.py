# tests/test_splyt.py

import os
import tempfile
import pytest
from splyt.core import splyt

TEST_IMAGES_DIR = 'tests/test_images'

def test_splyt_invalid_image():
    invalid_image_path = os.path.join(TEST_IMAGES_DIR, 'invalid_image.txt')
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create an invalid image file
        with open(invalid_image_path, 'w') as f:
            f.write('This is not an image')

        # Run the splyt function and expect a ValueError due to invalid image
        with pytest.raises(ValueError, match="is not a valid image"):
            splyt(invalid_image_path, tmpdir, grid_size=3)
