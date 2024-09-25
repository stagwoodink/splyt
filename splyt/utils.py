# splyt/utils.py

import os
import sys
import re
from PIL import Image, UnidentifiedImageError

# Supported grid sizes
VALID_GRID_SIZES = {2, 3, 4, 6, 8, 9, 12}

def parse_arguments(args):
    """
    Parse command line arguments to find the image path (or directory), save directory, grid size, and flags.
    Grid size can be placed anywhere in the command.
    """
    image_path = None
    save_dir = None
    grid_size = 3  # default grid size
    copy_metadata = True
    add_metadata = True

    # Flags
    flag_c = False
    flag_C = False

    for arg in args:
        if arg == '-c':
            flag_c = True
        elif arg == '-C':
            flag_C = True
        elif arg.isdigit() and int(arg) in VALID_GRID_SIZES:
            grid_size = int(arg)
        elif os.path.exists(arg):
            if image_path is None:
                image_path = arg
            else:
                save_dir = arg
        else:
            save_dir = arg

    if not image_path:
        print("Error: Image file or directory must be specified.")
        sys.exit(1)

    # Set metadata flags
    if flag_C:
        copy_metadata = False
        add_metadata = False
    elif flag_c:
        copy_metadata = False
        add_metadata = True

    return image_path, save_dir, grid_size, copy_metadata, add_metadata

def is_image_file(file_path):
    """
    Check if the file at file_path is an image.
    """
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify that it is, in fact, an image
        return True
    except (UnidentifiedImageError, IOError):
        return False

def col_index_to_letter(col_index):
    """
    Convert column index to a lowercase letter starting from 'a'.
    """
    return chr(ord('a') + col_index)

def print_progress(iteration, total, file_name='', final_message=False):
    """
    Print the progress in the format '#/# filename.ext', updating the same line.
    If final_message is True, display the completion message.
    """
    GREEN = '\033[32m'  # ANSI code for green
    RESET = '\033[0m'   # ANSI code to reset color
    if final_message:
        message = f"{GREEN}{total}/{total}{RESET} {file_name}"
        sys.stdout.write(f"\r{message}\n")
    else:
        sys.stdout.write(f"\r{GREEN}{iteration}/{total}{RESET} {file_name}")
    sys.stdout.flush()

def get_lowest_available_iteration(base_filenames, save_dir):
    """
    For all base filenames, find the lowest available iteration number not in use.
    Returns the lowest non-negative integer not used for any of the base filenames.
    """
    used_iterations = set()

    # Build a regex pattern to match filenames with optional iteration numbers
    pattern = re.compile(
        rf"({'|'.join(re.escape(bf) for bf in base_filenames)})(?:\((\d+)\))?\.\w+$"
    )

    for file in os.listdir(save_dir):
        match = pattern.match(file)
        if match:
            iteration = int(match.group(2)) if match.group(2) else 0
            used_iterations.add(iteration)

    # Find the lowest non-negative integer not in used_iterations
    iteration_num = 0
    while iteration_num in used_iterations:
        iteration_num += 1

    return iteration_num

def get_lowest_available_directory(base_dir):
    """
    Find the lowest available iteration number for the base directory.
    Returns the directory name with the iteration number appended if necessary.
    """
    if not os.path.exists(base_dir):
        return base_dir
    iteration = 1
    while True:
        new_dir = f"{base_dir}({iteration})"
        if not os.path.exists(new_dir):
            return new_dir
        iteration += 1

def get_grid_dimensions(grid_size, width, height):
    """
    Determine the number of rows and columns for grid sizes that require a grid layout.
    """
    is_long = width >= height
    if grid_size == 4:
        return 2, 2
    elif grid_size == 6:
        return (3, 2) if is_long else (2, 3)
    elif grid_size == 8:
        return (4, 2) if is_long else (2, 4)
    elif grid_size == 9:
        return 3, 3
    elif grid_size == 12:
        return (4, 3) if is_long else (3, 4)
    return 1, 1  # Should not happen for valid grid sizes
