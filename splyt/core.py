# splyt/core.py

import os
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
from .config import (
    VERSION,
    ERROR_INVALID_IMAGE,
    ERROR_UNSUPPORTED_FORMAT,
    PROGRESS_COMPLETE,
    SPLIT_DIR_SUFFIX,
)

def splyt(image_path, save_dir=None, grid_size=3, copy_metadata=True, add_metadata=True):
    """
    Split a single image into grid sections.
    """

    # Check if the file is an image
    if not is_image_file(image_path):
        raise ValueError(ERROR_INVALID_IMAGE.format(image=image_path))

    # Open the image
    try:
        img = Image.open(image_path)
    except (FileNotFoundError, UnidentifiedImageError):
        raise ValueError(ERROR_UNSUPPORTED_FORMAT.format(image=image_path))

    # Get the image filename and extension
    filename, ext = os.path.splitext(os.path.basename(image_path))

    # Handle save directory
    if save_dir is None:
        base_save_dir = f"{filename[:9]}{SPLIT_DIR_SUFFIX}"
    else:
        base_save_dir = os.path.join(save_dir, f"{filename[:9]}{SPLIT_DIR_SUFFIX}")

    # Ensure the save directory does not overwrite existing directories
    save_dir = get_lowest_available_directory(base_save_dir)
    os.makedirs(save_dir, exist_ok=True)

    # Get image dimensions
    width, height = img.size

    # Prepare metadata
    original_info = prepare_metadata(img, copy_metadata, add_metadata, VERSION)

    # Determine total number of splits and base filenames
    base_filenames = []
    if grid_size in {2, 3}:
        if width >= height:
            total_splits = grid_size
            # Horizontal split
            for i in range(grid_size):
                col_letter = col_index_to_letter(i)
                base_filename = f"{filename}_{col_letter}1"
                base_filenames.append(base_filename)
        else:
            total_splits = grid_size
            # Vertical split
            for i in range(grid_size):
                row_number = str(i + 1)
                base_filename = f"{filename}_a{row_number}"
                base_filenames.append(base_filename)
    else:
        num_cols, num_rows = get_grid_dimensions(grid_size, width, height)
        total_splits = num_cols * num_rows
        for row in range(num_rows):
            for col in range(num_cols):
                col_letter = col_index_to_letter(col)
                row_number = str(row + 1)
                base_filename = f"{filename}_{col_letter}{row_number}"
                base_filenames.append(base_filename)

    # Determine the lowest available iteration number for filenames
    iteration_num = get_lowest_available_iteration(base_filenames, save_dir)

    # Split and save images
    iteration = 0
    if grid_size in {2, 3}:
        if width >= height:
            # Horizontal split
            section_width = width // grid_size
            extra_width = width % grid_size
            for i in range(grid_size):
                left = i * section_width
                right = left + section_width + (extra_width if i == grid_size - 1 else 0)
                cropped_img = img.crop((left, 0, right, height))
                # Filename
                col_letter = col_index_to_letter(i)
                base_filename = f"{filename}_{col_letter}1"
                if iteration_num > 0:
                    cropped_filename = f"{base_filename}({iteration_num}){ext}"
                else:
                    cropped_filename = f"{base_filename}{ext}"
                # Save the image with metadata
                save_image_with_metadata(cropped_img, os.path.join(save_dir, cropped_filename), original_info, img.format)
                # Update progress
                iteration += 1
                print_progress(iteration, total_splits, cropped_filename)
        else:
            # Vertical split
            section_height = height // grid_size
            extra_height = height % grid_size
            for i in range(grid_size):
                upper = i * section_height
                lower = upper + section_height + (extra_height if i == grid_size - 1 else 0)
                cropped_img = img.crop((0, upper, width, lower))
                # Filename
                row_number = str(i + 1)
                base_filename = f"{filename}_a{row_number}"
                if iteration_num > 0:
                    cropped_filename = f"{base_filename}({iteration_num}){ext}"
                else:
                    cropped_filename = f"{base_filename}{ext}"
                # Save the image with metadata
                save_image_with_metadata(cropped_img, os.path.join(save_dir, cropped_filename), original_info, img.format)
                # Update progress
                iteration += 1
                print_progress(iteration, total_splits, cropped_filename)
    else:
        # Grid split
        num_cols, num_rows = get_grid_dimensions(grid_size, width, height)
        grid_width = width // num_cols
        grid_height = height // num_rows
        extra_width = width % num_cols
        extra_height = height % num_rows
        total_splits = num_cols * num_rows

        for row in range(num_rows):
            for col in range(num_cols):
                left = col * grid_width
                upper = row * grid_height
                right = left + grid_width + (extra_width if col == num_cols - 1 else 0)
                lower = upper + grid_height + (extra_height if row == num_rows - 1 else 0)
                cropped_img = img.crop((left, upper, right, lower))
                # Filename
                col_letter = col_index_to_letter(col)
                row_number = str(row + 1)
                base_filename = f"{filename}_{col_letter}{row_number}"
                if iteration_num > 0:
                    cropped_filename = f"{base_filename}({iteration_num}){ext}"
                else:
                    cropped_filename = f"{base_filename}{ext}"
                # Save the image with metadata
                save_image_with_metadata(cropped_img, os.path.join(save_dir, cropped_filename), original_info, img.format)
                # Update progress
                iteration += 1
                print_progress(iteration, total_splits, cropped_filename)

    # After completion, overwrite the progress line with the summary message
    final_message = f"{filename}{ext} split into {total_splits} sections and saved in '{save_dir}'"
    print_progress(total_splits, total_splits, final_message, final_message=True)


def process_directory(directory_path, save_dir, grid_size, copy_metadata, add_metadata):
    """
    Process all image files in the given directory.
    """
    # List all files in the directory
    files = os.listdir(directory_path)
    # Filter out directories and keep only image files
    image_files = [
        f for f in files
        if os.path.isfile(os.path.join(directory_path, f)) and is_image_file(os.path.join(directory_path, f))
    ]

    if not image_files:
        print(f"No image files found in directory '{directory_path}'.")
        sys.exit(1)

    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        print(f"\nProcessing '{image_file}'...")
        splyt(image_path, save_dir, grid_size, copy_metadata, add_metadata)
