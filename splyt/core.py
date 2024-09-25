# splyt/core.py

import os
import sys
from PIL import Image, UnidentifiedImageError
from .utils import (
    is_image_file,
    col_index_to_letter,
    print_progress,
    get_lowest_available_iteration,
    get_lowest_available_directory,
    get_grid_dimensions,
)
from .metadata import prepare_metadata, save_image_with_metadata

# Version number
VERSION = "1.0"

def splyt(image_path, save_dir=None, grid_size=3, copy_metadata=True, add_metadata=True):
    """
    Split a single image into grid sections.

    Parameters:
        image_path (str): Path to the image file.
        save_dir (str, optional): Directory where split images will be saved. Defaults to the image's directory.
        grid_size (int, optional): Number of sections to split the image into. Defaults to 3.
        copy_metadata (bool, optional): Whether to copy original metadata. Defaults to True.
        add_metadata (bool, optional): Whether to add custom metadata. Defaults to True.
    """
    # Validate that the image_path is a valid image file
    if not is_image_file(image_path):
        raise ValueError(f"The file '{image_path}' is not a valid image.")

    # If save_dir is not provided, set it to the same directory as the image
    if not save_dir:
        save_dir = os.path.dirname(image_path) or '.'

    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Get the image filename and extension
    filename, ext = os.path.splitext(os.path.basename(image_path))

    # Prepare the split directory
    split_dir_name = f"{filename[:9]}_split"
    split_dir = os.path.join(save_dir, split_dir_name)

    # Handle naming conflicts
    split_dir = get_lowest_available_directory(split_dir)

    # Create the directory for split images
    os.makedirs(split_dir, exist_ok=True)

    # Open the image
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # Prepare metadata
            metadata = prepare_metadata(img.info if hasattr(img, 'info') else {}, copy_metadata, add_metadata, VERSION)

            # Determine grid dimensions
            if grid_size in {2, 3}:
                # For grid sizes 2 and 3, decide between horizontal and vertical split
                if width >= height:
                    # Horizontal split
                    cols, rows = grid_size, 1
                else:
                    # Vertical split
                    cols, rows = 1, grid_size
            else:
                # For other grid sizes, determine cols and rows
                cols, rows = get_grid_dimensions(grid_size, width, height)

            tile_width = width // cols
            tile_height = height // rows
            extra_width = width % cols
            extra_height = height % rows

            total_tiles = cols * rows
            tile_number = 0

            # Determine the lowest available iteration number for filenames
            base_filenames = []
            for row in range(rows):
                for col in range(cols):
                    col_letter = col_index_to_letter(col)
                    row_number = str(row + 1)
                    base_filename = f"{filename}_{col_letter}{row_number}"
                    base_filenames.append(base_filename)
            iteration_num = get_lowest_available_iteration(base_filenames, split_dir)

            # Split and save images
            for row in range(rows):
                for col in range(cols):
                    left = col * tile_width
                    upper = row * tile_height
                    right = left + tile_width + (extra_width if col == cols - 1 else 0)
                    lower = upper + tile_height + (extra_height if row == rows - 1 else 0)
                    box = (left, upper, right, lower)
                    tile = img.crop(box)

                    # Filename
                    col_letter = col_index_to_letter(col)
                    row_number = str(row + 1)
                    base_filename = f"{filename}_{col_letter}{row_number}"
                    if iteration_num > 0:
                        tile_filename = f"{base_filename}({iteration_num}){ext}"
                    else:
                        tile_filename = f"{base_filename}{ext}"
                    tile_path = os.path.join(split_dir, tile_filename)

                    # Save the image with metadata
                    save_image_with_metadata(tile, tile_path, metadata, img.format)

                    # Update progress
                    tile_number += 1
                    print_progress(tile_number, total_tiles, filename + ext, split_dir)
    except (UnidentifiedImageError, FileNotFoundError):
        raise ValueError(f"The file '{image_path}' cannot be opened. It may be corrupted or in an unsupported format.")

    # After completion, overwrite the progress line with the summary message
    final_message = f"{tile_number}/{total_tiles} {filename}{ext} split into {total_tiles} sections and saved in '{split_dir}'"
    print_progress(total_tiles, total_tiles, final_message, final_message=True)

def process_directory(directory_path, save_dir, grid_size, copy_metadata, add_metadata):
    """
    Process all image files in the given directory.

    Parameters:
        directory_path (str): Path to the directory containing images.
        save_dir (str): Directory where split images will be saved.
        grid_size (int): Number of sections to split each image into.
        copy_metadata (bool): Whether to copy original metadata.
        add_metadata (bool): Whether to add custom metadata.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"The directory '{directory_path}' does not exist.")

    image_files = [
        f for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f)) and is_image_file(os.path.join(directory_path, f))
    ]

    if not image_files:
        print(f"No valid image files found in '{directory_path}'.")
        return

    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        print(f"\nProcessing '{image_file}'...")
        splyt(image_path, save_dir, grid_size, copy_metadata, add_metadata)
