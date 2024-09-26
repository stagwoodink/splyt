# Splyt v1.4

Splyt is a command-line tool that allows you to effortlessly split images into grid sections of any size and aspect ratio. Whether you need to divide an image for social media posts, web design, or any other purpose, Splyt provides a simple and flexible solution with smart defaults.

## Features

- **Split Single Images or Directories**: Process a single image file or batch process all images within a directory.
- **Customizable Grid Sizes**: Define your own grid by specifying the number of columns and rows, offering complete flexibility in how images are split.
- **Custom Aspect Ratios**: Specify a custom aspect ratio for the grid cells, and Splyt will adjust the cells accordingly while ensuring the entire image is covered.
- **Smart Defaults**: If grid size or aspect ratio is not specified, Splyt intelligently applies default values to simplify usage.
- **Flexible Command-Line Parsing**: Command-line arguments can be provided in any order, and Splyt will correctly interpret them.
- **Metadata Handling**:
  - **Copy Original Metadata**: Optionally retain the original image metadata in the split images.
  - **Add Custom Metadata**: Add a custom message indicating the images were created using Splyt.
- **Intelligent Metadata Storage**: Automatically determines the appropriate way to store metadata based on the image format.
- **Prevents Overwriting**: Checks for existing files and directories to prevent accidental overwriting by adding iteration numbers when necessary.
- **Cross-Platform Support**: Works on Linux, macOS, and Windows systems.

## Example

Splyt can take any image. We will use the following as our example:

![Example Image](tests/test_images/image_9.png)

Let's split it into a 3x3 grid using a 1:1 aspect ratio.

```bash
$ splyt image_9.png 3 3 1:1
```

The output will be 9 files like this:

![a1](tests/test_images/image_9_split_example/image_9_a1.png) ![b1](tests/test_images/image_9_split_example/image_9_b1.png) ![c1](tests/test_images/image_9_split_example/image_9_c1.png) ![a2](tests/test_images/image_9_split_example/image_9_a2.png) ![b2](tests/test_images/image_9_split_example/image_9_b2.png) ![c2](tests/test_images/image_9_split_example/image_9_c2.png) ![a3](tests/test_images/image_9_split_example/image_9_a3.png) ![b3](tests/test_images/image_9_split_example/image_9_b3.png) ![c3](tests/test_images/image_9_split_example/image_9_c3.png)

Each cell is a square due to the 1:1 aspect ratio, and the entire image is covered, with any extra pixels included in edge images if necessary.

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installing Splyt](#installing-splyt)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Options](#options)
  - [Examples](#examples)
- [Contributing](#contributing)
  - [Project Structure](#project-structure)
  - [Setting Up a Development Environment](#setting-up-a-development-environment)
- [License](#license)

## Installation

### Prerequisites

- **Python 3.6 or higher**: Ensure you have Python installed on your system.
- **Pip**: Python's package installer should be available.

### Installing Splyt

1. **Clone the Repository**

   Open your terminal or command prompt and clone the repository:

   ```bash
   git clone https://github.com/stagwoodink/splyt.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd splyt
   ```

3. **Install the Package**

   Install Splyt using `pip`:

   ```bash
   pip install .
   ```

   **Note**: You may need to use `pip3` instead of `pip` on some systems.

   This command installs Splyt and its dependencies. After installation, the `splyt` command will be available globally.

## Usage

### Basic Usage

```bash
splyt <image_path|directory> [save_directory] [grid_size] [aspect_ratio] [options]
```

- `<image_path|directory>`: Path to the image file or directory containing images to be split.
- `[save_directory]`: (Optional) Directory where the split images will be saved.
- `[grid_size]`: Define the number of columns and rows to split the image into. You can specify this using integers or formats like `x:y`, `x/y`, or `x x`.
- `[aspect_ratio]`: (Optional) Define the aspect ratio for each grid cell. Use two numbers or formats like `x:y`, `x/y`, or `x x`.
- `[options]`: Additional options (e.g., `-c`, `-C`).

**Important**: Command-line arguments can be provided in any order. Splyt intelligently parses integers as grid size and aspect ratio, and paths as the target image/directory and save directory.

### Options

- **Grid Sizes**:
  - Specify grid size using numbers in any order. The first two integers encountered are used for columns (x) and rows (y).
    - Examples:
      - `3 3` splits the image into 3 columns and 3 rows.
      - `4:2` or `4/2` splits the image into 4 columns and 2 rows.
      - `5x3` splits the image into 5 columns and 3 rows.
  - **Defaults**: If no grid size is provided, columns (x) defaults to 2, and rows (y) defaults to 1, creating a 2x1 split.

- **Aspect Ratios**:
  - To specify a custom aspect ratio for the grid cells, provide two more numbers or use formats like `x:y`.
    - Examples:
      - `16:9` sets the cell aspect ratio to 16:9.
      - `1 1` sets the cell aspect ratio to 1:1 (square cells).
  - If the aspect ratio is not specified, cells will adjust to fit the image dimensions evenly based on the grid size.

- **Flexible Argument Order**:
  - You can provide arguments in any order.
    - Examples:
      - `splyt image.png 3 3 1:1 save_dir`
      - `splyt 3 3 image.png save_dir 1:1`
      - Both commands will result in the same output.

- **Flags**:
  - `-c`: Do not copy the original metadata to the split images. The custom "Created using Splyt" metadata will still be added unless `-C` is also used.
  - `-C`: Do not copy the original metadata and do not add any metadata to the split images.

### Examples

#### Split a Single Image with Custom Grid Size and Aspect Ratio

```bash
splyt image.png 3 3 1:1
```

- Splits `image.png` into 3 columns and 3 rows with square cells (aspect ratio 1:1).
- Saves the split images in a directory named `splyt/` in the same location as `image.png`.

#### Split an Image Specifying Aspect Ratio and Save Directory

```bash
splyt image.jpg 4 2 16:9 output_dir
```

- Splits `image.jpg` into 4 columns and 2 rows with a cell aspect ratio of 16:9.
- Saves the split images in `output_dir/`.

#### Provide Arguments in Any Order

```bash
splyt output_dir 4 2 image.jpg 16:9
```

- Splyt intelligently parses the inputs:
  - Grid Size: 4 columns, 2 rows.
  - Aspect Ratio: 16:9.
  - Target Image: `image.jpg`.
  - Save Directory: `output_dir/`.
- Logic
  - The first path given is always the target image.
  - The second path given (optional) is always the destination.
  - The first integer (optional) is always grid columns.
  - The second integer (optional) is always grid rows.
  - The third integer (optional) is always aspect ratio y.
  - The fourth integer (optional) is always aspect ratio x.
  - Exceptions
    - It's smart enough to recognize groupings.
    - Giving `3 16:9` will result in 3 columns 1 row and an aspect ratio of 16:9.
    - But giving `3 16 9` will result in 3 columns 16 rows and a 9:auto aspect ratio.

#### Process All Images in a Directory with Custom Aspect Ratio

```bash
splyt input_images/ 3 3 4:5
```

- Processes all image files in `input_images/`.
- Splits each image into 3 columns and 3 rows with a cell aspect ratio of 4:5.
- Saves the split images in a `splyt/` directory within `input_images/`.

#### Do Not Copy Original Metadata

```bash
splyt image.png output_dir 9 9 -c
```

- Splits `image.png` into 9 columns and 9 rows.
- Does not copy the original metadata to the split images.
- Adds the custom "Created using Splyt" metadata.

#### Do Not Add Any Metadata

```bash
splyt image.png output_dir 12 1 -C
```

- Splits `image.png` into 12 sections horizontally.
- Does not copy the original metadata or add any custom metadata.

## Contributing

Contributions are welcome! If you'd like to contribute to Splyt, please follow these guidelines.

### Project Structure

```bash
splyt/
├── splyt/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── core.py
│   ├── metadata.py
│   └── utils.py
├── tests/
│   ├── test_images/*
│   └── test_splyt.py
├── README.md
├── LICENSE
└── setup.py
```

- **`splyt/` (inner directory)**: Contains the Python package modules.
  - **`__init__.py`**: Indicates that `splyt/` is a Python package.
  - **`cli.py`**: Handles command-line argument parsing and execution control.
  - **`core.py`**: Contains the core functionality for image processing.
  - **`metadata.py`**: Handles metadata for images.
  - **`utils.py`**: Helper functions for calculations and file operations.
  - **`config.py`**: Configuration constants and variables.
- **`setup.py`**: Setup script used to build and install the package.
- **`README.md`**: This file.
- **`LICENSE`**: The project's license file.
- **`tests/`**: Contains automated tests and test images.

### Setting Up a Development Environment

1. **Clone the Repository**

   ```bash
   git clone https://github.com/stagwoodink/splyt.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd splyt
   ```

3. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venvScriptsactivate'
   ```

4. **Install Dependencies**

   Install the package in editable mode along with development dependencies:

   ```bash
   pip install -e .
   ```

5. **Run Tests**

   Run automated tests to verify that everything is working:

   ```bash
   pytest
   ```

6. **Make Your Changes**

   - Ensure code quality by following PEP 8 guidelines.
   - Add or update documentation as needed.

7. **Submit a Pull Request**

   - Push your changes to your fork of the repository.
   - Open a pull request with a clear description of your changes.

## License

Splyt is released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software in accordance with the license.

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/stagwoodink/splyt/issues).

## Acknowledgements

- **Pillow**: Splyt utilizes the [Pillow](https://python-pillow.org/) library for image processing.
- **Community Contributions**: We welcome and appreciate contributions from the community.

---

Thank you for using Splyt! We hope it simplifies your image splitting tasks.
