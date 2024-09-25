# config.py

# Version number
VERSION = "1.0"

# Supported grid sizes
VALID_GRID_SIZES = {2, 3, 4, 6, 8, 9, 12}

# Metadata related strings
CREATED_WITH_METADATA = "Created using Splyt v{version}"
COMMENT_KEY_PNG = "Comment"
USER_COMMENT_TAG_JPEG = 0x9286  # UserComment EXIF tag

# Error messages
ERROR_INVALID_IMAGE = "Error: The file '{image}' is not a valid image."
ERROR_UNSUPPORTED_FORMAT = "Error: Cannot open the image '{image}'. It may be corrupted or in an unsupported format."
ERROR_NO_IMAGE_FILES = "No image files found in directory '{directory}'."

# Progress messages
PROGRESS_COMPLETE = "{filename}{ext} split into {total_splits} sections and saved in '{save_dir}'"

# Directories and filenames
SPLIT_DIR_SUFFIX = "_split"
