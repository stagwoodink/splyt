# core.py

import os
from PIL import Image, UnidentifiedImageError
from .utils import (
    create_save_directory_if_needed,
    is_image_file,
    calculate_cell_positions,
    col_to_letter,
)
from .metadata import prepare_metadata, save_image_with_metadata
from .config import (
    VERSION,
    SUPPORTED_FORMATS,
    ERROR_CANNOT_IDENTIFY_IMAGE,
    ERROR_UNSUPPORTED_IMAGE_TYPE,
    ERROR_UNABLE_TO_SAVE_IMAGE,
)

def splyt(image_path, save_dir=None, grid_size=(3, 3), aspect_ratio=None, copy_metadata=True, add_metadata=True, cli_callbacks=None):
    """
    Split a single image into grid sections, accounting for aspect ratio if provided.
    """
    print_progress, print_completion_message = cli_callbacks if cli_callbacks else (None, None)

    # Ensure save_dir is set and exists
    save_dir = create_save_directory_if_needed(save_dir or os.path.dirname(image_path))

    try:
        img = Image.open(image_path)
    except (UnidentifiedImageError, FileNotFoundError):
        print(ERROR_CANNOT_IDENTIFY_IMAGE.format(image_path=image_path))
        return

    # Check if image format is supported
    img_format = img.format.upper()
    if img_format not in SUPPORTED_FORMATS:
        print(ERROR_UNSUPPORTED_IMAGE_TYPE.format(image_type=img_format))
        return

    width, height = img.size
    filename, ext = os.path.splitext(os.path.basename(image_path))
    original_info = prepare_metadata(img, copy_metadata, add_metadata, VERSION)

    # Use utility function to calculate cell positions
    cells = calculate_cell_positions((width, height), grid_size, aspect_ratio)

    total_splits = len(cells)
    split_count = 0

    for idx, cell in enumerate(cells):
        col = cell['col']
        row = cell['row']
        left = cell['left']
        upper = cell['upper']
        right = cell['right']
        lower = cell['lower']

        # Generate the filename for this specific grid split
        col_letter = col_to_letter(col)
        row_number = row + 1
        cropped_filename = f"{filename}_{col_letter}{row_number}{ext}"

        # Crop and save the image
        success = crop_and_save_image(img, left, upper, right, lower, cropped_filename, ext, save_dir, original_info, img_format)

        if not success:
            print(ERROR_UNABLE_TO_SAVE_IMAGE.format(image_name=cropped_filename, image_format=img_format))
        split_count += 1

        if print_progress:
            print_progress(split_count, total_splits, cropped_filename)

    if print_completion_message:
        print_completion_message(f"{filename}{ext}", total_splits, save_dir)

def crop_and_save_image(img, left, upper, right, lower, base_filename, ext, save_dir, original_info, img_format):
    """
    Crop the image and save it with metadata.
    """
    cropped_img = img.crop((left, upper, right, lower))
    cropped_filepath = os.path.join(save_dir, base_filename)

    # Ensure unique filename to avoid overwriting
    if os.path.exists(cropped_filepath):
        base_name, extension = os.path.splitext(base_filename)
        counter = 1
        while True:
            new_filename = f"{base_name}({counter}){extension}"
            new_filepath = os.path.join(save_dir, new_filename)
            if not os.path.exists(new_filepath):
                cropped_filepath = new_filepath
                break
            counter += 1
    else:
        cropped_filepath = os.path.join(save_dir, base_filename)

    try:
        save_image_with_metadata(cropped_img, cropped_filepath, original_info, img_format)
        return True
    except Exception:
        # You can log the exception if needed
        return False

def process_directory(directory_path, save_dir, grid_size, aspect_ratio=None, copy_metadata=True, add_metadata=True, cli_callbacks=None):
    """
    Process all valid images in a directory.
    """
    save_dir = create_save_directory_if_needed(save_dir)

    image_files = [f for f in os.listdir(directory_path) if is_image_file(os.path.join(directory_path, f))]
    total_images = len(image_files)

    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(directory_path, image_file)
        splyt(image_path, save_dir, grid_size, aspect_ratio, copy_metadata, add_metadata, cli_callbacks)
