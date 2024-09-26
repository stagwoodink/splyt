# config.py

# Version number
VERSION = "1.4"

# Metadata related strings
CREATED_WITH_METADATA = "Created with Splyt v{version}"
COMMENT_KEY_PNG = "Comment"
USER_COMMENT_TAG_JPEG = 0x9286  # UserComment EXIF tag

# Error and progress messages
USAGE_MESSAGE = "Usage: splyt <image_path|directory> [save_directory] [grid_size] [aspect_ratio] [options]"
ERROR_INVALID_IMAGE = "Error: The file '{image}' is not a valid image."
ERROR_UNSUPPORTED_FORMAT = "Error: Cannot open the image '{image}'. It may be corrupted or in an unsupported format."
ERROR_NO_IMAGE_FILES = "No image files found in directory '{directory}'."
ERROR_UNSUPPORTED_IMAGE_TYPE = "Error: The file type '{image_type}' is not currently supported."
ERROR_NO_TARGET_IMAGE = "Error: No target image or directory provided."
ERROR_CANNOT_IDENTIFY_IMAGE = "Cannot identify image file '{image_path}'. The file may be corrupted or in an unsupported format."
ERROR_UNABLE_TO_SAVE_IMAGE = "Error: Unable to save image '{image_name}' in format '{image_format}'."

# Terminal output messages
PROCESSING_IMAGE = "Processing {iteration}/{total}: {filename}"
COMPLETION_MESSAGE = "{total_images} images created{aspect_info} and saved in {save_dir} {eta}"

# Terminal colors (ANSI escape codes)
COLOR_GREEN = '\033[92m'
COLOR_WHITE = '\033[97m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

# Supported image formats
SUPPORTED_FORMATS = ['JPEG', 'JPG', 'PNG', 'BMP', 'GIF', 'TIFF', 'TIF']

# Other constants
ETA_FORMAT = "{minutes:02d}:{seconds:02d}"
