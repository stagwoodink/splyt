import os
import sys
import time
from PIL import Image, UnidentifiedImageError, ExifTags, PngImagePlugin, JpegImagePlugin
import re

# Version number
VERSION = "1.0"

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
    pattern = re.compile(rf"({'|'.join(re.escape(bf) for bf in base_filenames)})(?:\((\d+)\))?\.\w+$")

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

def exif_data_to_bytes(exif_dict):
    """
    Convert EXIF data dictionary to bytes.
    """
    exif_bytes = Image.Exif()
    for tag, value in exif_dict.items():
        exif_bytes[tag] = value
    return exif_bytes.tobytes()

def save_image_with_metadata(image, file_path, metadata, original_format):
    """
    Save the image to the specified file path, including metadata.
    """
    # Get the format from the original image or file extension
    format_lower = original_format.lower() if original_format else ''
    if not format_lower:
        _, ext = os.path.splitext(file_path)
        format_lower = ext.lower().strip('.')

    if format_lower == 'png':
        # For PNG images
        info = PngImagePlugin.PngInfo()
        for k, v in metadata.items():
            if isinstance(v, str):
                info.add_text(k, v)
            elif isinstance(v, bytes):
                info.add_itxt(k, v.decode('utf-8', 'ignore'))
            else:
                info.add_text(k, str(v))
        image.save(file_path, pnginfo=info)
    elif format_lower in ['jpeg', 'jpg']:
        # For JPEG images
        if 'exif' in metadata:
            exif_data = metadata['exif']
            exif_bytes = exif_data_to_bytes(exif_data)
            image.save(file_path, exif=exif_bytes)
        else:
            image.save(file_path)
    else:
        # Other formats may not support metadata
        image.save(file_path)

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

def splyt(image_path, save_dir=None, grid_size=3, copy_metadata=True, add_metadata=True):
    """
    Split a single image into grid sections.
    """
    # Check if the file is an image
    if not is_image_file(image_path):
        print(f"Error: The file '{image_path}' is not a valid image.")
        return

    # Open the image
    try:
        img = Image.open(image_path)
    except (FileNotFoundError, UnidentifiedImageError):
        print(f"Error: Cannot open the image '{image_path}'. It may be corrupted or in an unsupported format.")
        return

    # Get the image filename and extension
    filename, ext = os.path.splitext(os.path.basename(image_path))

    # Handle save directory
    if save_dir is None:
        base_save_dir = f"{filename[:9]}_split"
    else:
        base_save_dir = os.path.join(save_dir, f"{filename[:9]}_split")

    # Ensure the save directory does not overwrite existing directories
    save_dir = get_lowest_available_directory(base_save_dir)
    os.makedirs(save_dir, exist_ok=True)

    # Get image dimensions
    width, height = img.size

    # Prepare metadata
    original_info = img.info.copy() if copy_metadata else {}

    # Add custom metadata
    if add_metadata:
        metadata_text = f"Created using Splyt v{VERSION}"
        format_lower = img.format.lower() if img.format else ''
        if format_lower == 'png':
            # For PNG, add to 'Comment' or as tEXt chunk
            if 'Comment' in original_info:
                original_info['Comment'] += '\n' + metadata_text
            else:
                original_info['Comment'] = metadata_text
        elif format_lower in ['jpeg', 'jpg']:
            # For JPEG, use EXIF
            exif_data = img.getexif()
            exif_dict = dict(exif_data)
            exif_dict[0x9286] = metadata_text  # UserComment tag
            original_info['exif'] = exif_dict
        else:
            # For other formats, handle appropriately if possible
            pass

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
    image_files = [f for f in files if os.path.isfile(os.path.join(directory_path, f)) and is_image_file(os.path.join(directory_path, f))]

    if not image_files:
        print(f"No image files found in directory '{directory_path}'.")
        sys.exit(1)

    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        print(f"\nProcessing '{image_file}'...")
        splyt(image_path, save_dir, grid_size, copy_metadata, add_metadata)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: splyt <image_path|directory> [save_directory] [grid_size] [-c] [-C]")
        sys.exit(1)

    image_path, save_dir, grid_size, copy_metadata, add_metadata = parse_arguments(sys.argv[1:])
    if grid_size not in VALID_GRID_SIZES:
        print(f"Invalid grid size '{grid_size}'. Valid options are {VALID_GRID_SIZES}. Defaulting to 3.")
        grid_size = 3

    if os.path.isdir(image_path):
        # Process all image files in the directory
        process_directory(image_path, save_dir, grid_size, copy_metadata, add_metadata)
    else:
        # Process a single image file
        splyt(image_path, save_dir, grid_size, copy_metadata, add_metadata)
