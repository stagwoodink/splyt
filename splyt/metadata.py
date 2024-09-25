# splyt/metadata.py

from PIL import PngImagePlugin, JpegImagePlugin

def prepare_metadata(img_info, copy_metadata, add_metadata, version):
    """
    Prepare the metadata dictionary for saving images.

    Parameters:
        img_info (dict): The original image info or metadata.
        copy_metadata (bool): Whether to copy the original metadata.
        add_metadata (bool): Whether to add custom metadata.
        version (str): The version of the splyt tool to add as metadata.

    Returns:
        dict: Prepared metadata dictionary for the image.
    """
    # Start with a copy of the original info if copy_metadata is True, otherwise an empty dict
    original_info = img_info.copy() if copy_metadata else {}

    # Add custom metadata if required
    if add_metadata:
        metadata_text = f"Created using Splyt v{version}"
        if 'Comment' in original_info:
            original_info['Comment'] += '\n' + metadata_text
        else:
            original_info['Comment'] = metadata_text

    return original_info

def save_image_with_metadata(image, file_path, metadata, original_format):
    """
    Save the image to the specified file path, including metadata.

    Parameters:
        image (PIL.Image): The image object to save.
        file_path (str): The path to save the image to.
        metadata (dict): Metadata to include with the image.
        original_format (str): The format of the original image (e.g., 'png', 'jpeg').
    """
    format_lower = original_format.lower()

    if format_lower == 'png':
        # For PNG images
        info = PngImagePlugin.PngInfo()
        for key, value in metadata.items():
            if isinstance(value, str):
                info.add_text(key, value)
            elif isinstance(value, bytes):
                info.add_itxt(key, value.decode('utf-8', 'ignore'))
            else:
                info.add_text(key, str(value))
        image.save(file_path, pnginfo=info)

    elif format_lower in ['jpeg', 'jpg']:
        # For JPEG images
        exif_data = image.getexif()
        if 'exif' in metadata:
            exif_dict = metadata['exif']
            for key, val in exif_dict.items():
                exif_data[key] = val
            exif_bytes = exif_data.tobytes()
            image.save(file_path, exif=exif_bytes)
        else:
            image.save(file_path)

    else:
        # For other formats, save without specific metadata handling
        image.save(file_path)
