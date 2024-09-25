# splyt/metadata.py

import os
from PIL import Image, PngImagePlugin, JpegImagePlugin

def prepare_metadata(img, copy_metadata, add_metadata, version):
    """
    Prepare the metadata dictionary for saving images.
    """
    original_info = img.info.copy() if copy_metadata else {}

    # Add custom metadata
    if add_metadata:
        metadata_text = f"Created using Splyt v{version}"
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

    return original_info

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
