# Splyt v0.1

Splyt is a command-line tool that allows you to effortlessly split images into even grid sections. Whether you need to divide an image for social media posts, web design, or any other purpose, Splyt provides a simple and flexible solution.

## Features

- **Split Single Images or Directories**: Process a single image file or batch process all images within a directory.
- **Customizable Grid Sizes**: Supports various grid sizes including 2, 3, 4, 6, 8, 9, and 12 sections.
- **Metadata Handling**:
  - **Copy Original Metadata**: Optionally retain the original image metadata in the split images.
  - **Add Custom Metadata**: Add a custom message indicating the images were created using Splyt.
- **Intelligent Metadata Storage**: Automatically determines the appropriate way to store metadata based on the image format.
- **Prevents Overwriting**: Checks for existing files and directories to prevent accidental overwriting by adding iteration numbers when necessary.
- **Cross-Platform Support**: Works on Linux, macOS, and Windows systems.

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
splyt <image_path|directory> [save_directory] [grid_size] [-c] [-C]
```

- `<image_path|directory>`: Path to the image file or directory containing images to be split.
- `[save_directory]`: (Optional) Directory where the split images will be saved.
- `[grid_size]`: (Optional) Number of sections to split the image into. Valid options are `2`, `3`, `4`, `6`, `8`, `9`, `12`. Defaults to `3` if not specified.
- `-c`: Do not copy the original metadata to the split images.
- `-C`: Do not copy the original metadata and do not add the custom "Created using Splyt" metadata.

### Options

- **Grid Sizes**:
  - `2`, `3`: Splits the image into 2 or 3 sections either horizontally or vertically, depending on the image orientation.
  - `4`, `6`, `8`, `9`, `12`: Splits the image into a grid layout.

- **Flags**:
  - `-c`: Prevents copying of the original metadata. The custom "Created using Splyt" metadata will still be added unless `-C` is also used.
  - `-C`: Does not copy the original metadata and does not add any metadata to the split images.

### Examples

#### Split a Single Image into 3 Sections

```bash
splyt image.png
```

- Splits `image.png` into 3 sections.
- Saves the split images in a directory named `image_split/`.

#### Specify a Save Directory and Grid Size

```bash
splyt image.jpg output_dir 6
```

- Splits `image.jpg` into 6 sections.
- Saves the split images in `output_dir/image_split/`.

#### Process All Images in a Directory

```bash
splyt input_images/ output_dir 4
```

- Processes all image files in `input_images/`.
- Splits each image into 4 sections.
- Saves the split images in subdirectories within `output_dir/`.

#### Do Not Copy Original Metadata

```bash
splyt image.png output_dir 9 -c
```

- Splits `image.png` into 9 sections.
- Does not copy the original metadata to the split images.
- Adds the custom "Created using Splyt" metadata.

#### Do Not Add Any Metadata

```bash
splyt image.png output_dir 12 -C
```

- Splits `image.png` into 12 sections.
- Does not copy the original metadata or add any custom metadata.

## Contributing

Contributions are welcome! If you'd like to contribute to Splyt, please follow these guidelines.

### Project Structure

```
splyt/
├── splyt/
│   ├── __init__.py
│   ├── core.py
│   ├── metadata.py
│   └── utils.py
├── setup.py
├── README.md
├── LICENSE
└── tests/
    └── test_splyt.py
```

- **`splyt/` (inner directory)**: Contains the Python package modules.
  - **`__init__.py`**: Indicates that `splyt/` is a Python package.
  - **`core.py`**: The main script containing the core functionality.
  - **`metadata.py`**: Handles metadata for images.
  - **`utils.py`**: Helper functions for splitting, naming, and file operations.
- **`setup.py`**: Setup script used to build and install the package.
- **`README.md`**: This file.
- **`LICENSE`**: The project's license file.
- **`tests/`**: Contains the automated tests.

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
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
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
