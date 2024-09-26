# metadata.py

from PIL import Image, ExifTags
from .config import CREATED_WITH_METADATA, VERSION, COMMENT_KEY_PNG, USER_COMMENT_TAG_JPEG

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
            # For PNG, add to 'Comment'
            comments = original_info.get(COMMENT_KEY_PNG, '')
            if comments:
                original_info[COMMENT_KEY_PNG] = comments + '\n' + metadata_text
            else:
                original_info[COMMENT_KEY_PNG] = metadata_text
        elif format_lower in ['jpeg', 'jpg']:
            # For JPEG, use EXIF
            exif_data = img.getexif()
            exif_data[USER_COMMENT_TAG_JPEG] = metadata_text
            original_info['exif'] = exif_data
        # Other formats may not support metadata

    # Ensure EXIF data is included if copy_metadata is True
    if copy_metadata and img.format.lower() in ['jpeg', 'jpg']:
        exif_data = img.getexif()
        if exif_data:
            original_info['exif'] = exif_data

    return original_info

def save_image_with_metadata(image, file_path, metadata, image_format):
    """
    Save the image to the specified file path, including metadata.
    """
    format_lower = image_format.lower() if image_format else ''
    try:
        if format_lower == 'png':
            from PIL import PngImagePlugin
            info = PngImagePlugin.PngInfo()
            for k, v in metadata.items():
                if isinstance(v, str):
                    info.add_text(k, v)
                elif isinstance(v, bytes):
                    info.add_text(k, v.decode('utf-8', 'ignore'))
            image.save(file_path, pnginfo=info)
        elif format_lower in ['jpeg', 'jpg']:
            exif_data = metadata.get('exif')
            if exif_data:
                exif_bytes = exif_data.tobytes()
                image.save(file_path, exif=exif_bytes)
            else:
                image.save(file_path)
        else:
            # For other formats, save without metadata
            image.save(file_path)
    except Exception:
        # If saving with metadata fails, save without it
        image.save(file_path)
