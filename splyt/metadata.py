# splyt/metadata.py

from .config import CREATED_WITH_METADATA, COMMENT_KEY_PNG, USER_COMMENT_TAG_JPEG

def prepare_metadata(img, copy_metadata, add_metadata, version):
    """
    Prepare the metadata dictionary for saving images.
    """
    original_info = img.info.copy() if copy_metadata else {}

    # Add custom metadata
    if add_metadata:
        metadata_text = CREATED_WITH_METADATA.format(version=version)
        format_lower = img.format.lower()
        if format_lower == 'png':
            # For PNG, add to 'Comment' or as tEXt chunk
            if COMMENT_KEY_PNG in original_info:
                original_info[COMMENT_KEY_PNG] += '\n' + metadata_text
            else:
                original_info[COMMENT_KEY_PNG] = metadata_text
        elif format_lower in ['jpeg', 'jpg']:
            # For JPEG, use EXIF
            exif_data = img.getexif()
            exif_dict = dict(exif_data)
            exif_dict[USER_COMMENT_TAG_JPEG] = metadata_text
            original_info['exif'] = exif_dict
    return original_info

def save_image_with_metadata(image, file_path, metadata, original_format):
    """
    Save the image to the specified file path, including metadata.
    """
    format_lower = original_format.lower() if original_format else ''
    if format_lower == 'png':
        # For PNG images
        from PIL import PngImagePlugin
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
        # Other formats may not support metadata
        image.save(file_path)
