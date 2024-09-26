# cli.py

import sys
import os
import re
import time
from splyt.core import splyt, process_directory
from splyt.config import (
    USAGE_MESSAGE,
    ERROR_NO_TARGET_IMAGE,
    COLOR_GREEN,
    COLOR_WHITE,
    COLOR_BLUE,
    COLOR_RESET,
    PROCESSING_IMAGE,
    COMPLETION_MESSAGE,
    ETA_FORMAT
)
from splyt.utils import get_lowest_available_directory

def parse_arguments():
    args = sys.argv[1:]

    if len(args) < 1:
        print(USAGE_MESSAGE)
        sys.exit(1)

    # Initialize variables
    grid_x = grid_y = aspect_x = aspect_y = None
    target = save_dir = None
    copy_metadata = True
    add_metadata = True
    paths = []
    integers = []
    size_patterns = re.compile(r'^(\d+)[xX:/](\d+)$')

    # Handle options
    options = []
    for arg in args:
        if arg.startswith('-'):
            options.extend(arg[1:])
    if 'c' in options:
        copy_metadata = False
    if 'C' in options:
        copy_metadata = False
        add_metadata = False

    for arg in args:
        if arg.startswith('-'):
            continue

        # Try to parse 'NxM' patterns for grid size or aspect ratio
        match = size_patterns.match(arg)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            integers.extend([num1, num2])
            continue

        # Try to parse integers
        try:
            num = int(arg)
            integers.append(num)
            continue
        except ValueError:
            # Not an integer; treat as path
            paths.append(arg)
            continue

    # Assign integers to grid and aspect ratio
    if integers:
        grid_x = integers[0] if len(integers) > 0 else None
        grid_y = integers[1] if len(integers) > 1 else None
        aspect_x = integers[2] if len(integers) > 2 else None
        aspect_y = integers[3] if len(integers) > 3 else None

    # Default grid size if not provided
    if grid_x is None:
        grid_x = 2
    if grid_y is None:
        grid_y = 1
    grid_size = (grid_x, grid_y)

    # Set aspect ratio if provided
    aspect_ratio = (aspect_x, aspect_y) if aspect_x is not None and aspect_y is not None else None

    # Assign paths
    if paths:
        target = paths[0]
        if len(paths) > 1:
            save_dir = paths[1]
    else:
        print(USAGE_MESSAGE)
        print(ERROR_NO_TARGET_IMAGE)
        sys.exit(1)

    # Convert paths to absolute paths
    target = os.path.abspath(target)
    if save_dir is not None:
        save_dir = os.path.abspath(save_dir)
    else:
        # Default save directory
        target_dir = os.path.dirname(target) if os.path.isfile(target) else target
        save_dir = get_lowest_available_directory(os.path.join(target_dir, "splyt"))
        save_dir = os.path.abspath(save_dir)

    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    return grid_size, aspect_ratio, target, save_dir, copy_metadata, add_metadata

def main():
    grid_size, aspect_ratio, target, save_dir, copy_metadata, add_metadata = parse_arguments()

    start_time = time.time()

    if os.path.isdir(target):
        total_images = len([f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))])
    else:
        total_images = 1

    processed_images = 0

    def print_progress(iteration, total, filename):
        nonlocal start_time, processed_images

        processed_images += 1
        elapsed_time = time.time() - start_time
        avg_time_per_image = elapsed_time / processed_images if processed_images else 0
        remaining_images = total - iteration
        eta_seconds = int(avg_time_per_image * remaining_images)
        eta_minutes, eta_seconds = divmod(eta_seconds, 60)
        eta_formatted = ETA_FORMAT.format(minutes=eta_minutes, seconds=eta_seconds)

        progress_message = (
            f"{COLOR_GREEN}{PROCESSING_IMAGE.format(iteration=iteration, total=total, filename='')}{COLOR_RESET}"
            f"{COLOR_WHITE}{filename}{COLOR_RESET} "
            f"{COLOR_BLUE}{eta_formatted}{COLOR_RESET}"
        )

        print(f"\r{progress_message}", end='', flush=True)

    def print_completion_message(filename, total_splits, save_dir):
        aspect_info = f" in [{aspect_ratio[0]}:{aspect_ratio[1]}]" if aspect_ratio else ""
        total_images_str = f"{COLOR_GREEN}{total_splits}{COLOR_RESET}"
        eta_formatted = ETA_FORMAT.format(minutes=0, seconds=0)
        completion_message = COMPLETION_MESSAGE.format(
            total_images=total_images_str,
            aspect_info=aspect_info,
            save_dir=save_dir,
            eta=f"{COLOR_BLUE}{eta_formatted}{COLOR_RESET}"
        )
        print(f"\r{' ' * 80}", end='\r')  # Clear the line
        print(completion_message)

    if os.path.isdir(target):
        process_directory(
            target,
            save_dir,
            grid_size,
            aspect_ratio=aspect_ratio,
            copy_metadata=copy_metadata,
            add_metadata=add_metadata,
            cli_callbacks=(print_progress, print_completion_message)
        )
    else:
        splyt(
            target,
            save_dir,
            grid_size,
            aspect_ratio=aspect_ratio,
            copy_metadata=copy_metadata,
            add_metadata=add_metadata,
            cli_callbacks=(print_progress, print_completion_message)
        )

if __name__ == "__main__":
    main()
