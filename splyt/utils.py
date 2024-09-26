# utils.py

import os
from PIL import Image, UnidentifiedImageError
from .config import SUPPORTED_FORMATS

def is_image_file(filepath):
    """
    Check if the given file path points to a valid image of a supported format.
    """
    try:
        with Image.open(filepath) as img:
            return img.format.upper() in SUPPORTED_FORMATS
    except (FileNotFoundError, UnidentifiedImageError):
        return False

def get_lowest_available_directory(base_dir):
    """
    Determine the lowest available directory to avoid overwriting directories.
    """
    iteration = 1
    new_dir = f"{base_dir}/{iteration}"
    while os.path.exists(new_dir):
        iteration += 1
        new_dir = f"{base_dir}/{iteration}"
    return new_dir

def create_save_directory_if_needed(save_dir):
    """
    Ensure the save directory exists.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir

def col_to_letter(col):
    """
    Convert a column number to a letter representation (a-z, aa, ab, etc.).
    """
    result = []
    col += 1  # Adjusting to 1-based indexing
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        result.append(chr(65 + remainder))  # Using uppercase letters
    return ''.join(reversed(result)).lower()

def calculate_cell_positions(image_size, grid_size, aspect_ratio=None):
    """
    Calculate cell positions based on image size, grid size, and aspect ratio.
    Returns a list of cells, each cell is a dict with keys:
    - 'col': column index
    - 'row': row index
    - 'left': left pixel coordinate
    - 'upper': upper pixel coordinate
    - 'right': right pixel coordinate
    - 'lower': lower pixel coordinate
    """
    width, height = image_size
    num_cols, num_rows = grid_size

    cells = []

    if aspect_ratio is None:
        # Evenly split the image
        col_width = width / num_cols
        row_height = height / num_rows
        for col in range(num_cols):
            for row in range(num_rows):
                left = int(col * col_width)
                upper = int(row * row_height)
                right = int((col + 1) * col_width) if col < num_cols - 1 else width
                lower = int((row + 1) * row_height) if row < num_rows - 1 else height
                cells.append({
                    'col': col,
                    'row': row,
                    'left': left,
                    'upper': upper,
                    'right': right,
                    'lower': lower
                })
    else:
        aspect_x, aspect_y = aspect_ratio

        # Compute scaling factor
        scale_x = width / (aspect_x * num_cols)
        scale_y = height / (aspect_y * num_rows)
        scaling_factor = min(scale_x, scale_y)

        cell_width = aspect_x * scaling_factor
        cell_height = aspect_y * scaling_factor

        total_width = cell_width * num_cols
        total_height = cell_height * num_rows

        # Adjust for any remaining pixels to cover the entire image
        extra_width = width - total_width
        extra_height = height - total_height

        cols = num_cols + (1 if extra_width > 0 else 0)
        rows = num_rows + (1 if extra_height > 0 else 0)

        for col in range(cols):
            for row in range(rows):
                left = int(col * cell_width)
                upper = int(row * cell_height)
                right = int((col + 1) * cell_width)
                lower = int((row + 1) * cell_height)

                if col == cols - 1:
                    right = width
                if row == rows - 1:
                    lower = height

                cells.append({
                    'col': col,
                    'row': row,
                    'left': left,
                    'upper': upper,
                    'right': right,
                    'lower': lower
                })

    return cells
