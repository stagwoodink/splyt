# splyt/cli.py

import sys
import os
from .utils import parse_arguments, VALID_GRID_SIZES
from .core import splyt, process_directory

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print_usage()
        sys.exit(0)

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

def print_usage():
    print('''Usage: splyt <image_path|directory> [save_directory] [grid_size] [-c] [-C]
Options:
  -c       Do not copy the original metadata to the split images.
  -C       Do not copy the original metadata and do not add custom metadata.
  -h, --help  Show this help message and exit.

Valid grid sizes: 2, 3, 4, 6, 8, 9, 12 (default: 3)
''')
