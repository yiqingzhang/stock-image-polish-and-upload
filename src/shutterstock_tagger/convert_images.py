"""
Image format conversion module.

Converts HEIC/HEIF images to JPEG format with sRGB color profile
and removes unsupported formats like PNG.
"""

import os
import io
from PIL import Image, ImageCms
import pillow_heif
import argparse
from tqdm import tqdm

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()


def convert_to_jpeg(input_path, output_path):
    """
    Convert an image to high-quality JPEG with sRGB color profile.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path where the JPEG output will be saved
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if needed (for PNG with transparency, HEIC, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply sRGB color profile
            try:
                srgb_profile = ImageCms.createProfile('sRGB')
                if img.info.get('icc_profile'):
                    # Convert from current profile to sRGB
                    input_profile = ImageCms.ImageCmsProfile(io.BytesIO(img.info['icc_profile']))
                    img = ImageCms.profileToProfile(img, input_profile, srgb_profile)
                # If no profile exists, just ensure RGB mode (sRGB is assumed)
            except Exception as e:
                print(f"Warning: Could not apply sRGB profile to {input_path}: {e}")
            
            # Save as high-quality JPEG
            img.save(output_path, 'jpeg', quality=95, optimize=True)
            return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False


def is_convertible_format(filepath):
    """
    Check if file is in a format we can convert to JPEG.
    
    Args:
        filepath (str): Path to the file to check
        
    Returns:
        bool: True if file can be converted to JPEG
    """
    ext = os.path.splitext(filepath)[1].lower()
    return ext in ['.heic', '.heif']


def is_deletable_format(filepath):
    """
    Check if file is in a format that should be deleted.
    
    Args:
        filepath (str): Path to the file to check
        
    Returns:
        bool: True if file should be deleted
    """
    ext = os.path.splitext(filepath)[1].lower()
    return ext in ['.png']


def convert_directory(directory):
    """
    Convert HEIC images to JPEG, and remove invalid files.
    
    Args:
        directory (str): Directory path containing images to process
    """
    files_to_convert = []
    files_to_delete = []

    print(f"Scanning directory: {directory}")

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip directories and non-image files
            if os.path.isdir(filepath):
                continue

            # Check if it's a convertible format (HEIC)
            if is_convertible_format(filepath):
                files_to_convert.append(filepath)
                continue
            # Check if it's a deletable format (PNG)
            if is_deletable_format(filepath):
                files_to_delete.append(filepath)
                continue

    # Show files to be converted
    if files_to_convert:
        print(f"\nFound {len(files_to_convert)} files to convert to JPEG:")

    # Show files to be deleted
    if files_to_delete:
        print(f"\nFound {len(files_to_delete)} files to delete:")
        for filepath in files_to_delete:
            print(f"  - {filepath}")

    if not files_to_convert and not files_to_delete:
        print("No files to convert or delete.")
        return

    # Ask for confirmation
    if files_to_convert or files_to_delete:
        confirmation = input("\nDo you want to proceed with these operations? (yes/no): ")
        
        if confirmation.lower() in ["yes", "y"]:
            # Convert files
            converted_count = 0

            print(f"\nConverting {len(files_to_convert)} files to JPEG...")
            for filepath in tqdm(files_to_convert):
                # Generate output filename (replace extension with .jpeg)
                base_name = os.path.splitext(filepath)[0]
                output_path = base_name + ".jpeg"
                
                if convert_to_jpeg(filepath, output_path):
                    # Remove original file after successful conversion
                    try:
                        os.remove(filepath)
                        converted_count += 1
                    except Exception as e:
                        print(f"Error removing original {filepath}: {e}")
                else:
                    print(f"Failed to convert: {filepath}")

            # Delete invalid files
            deleted_count = 0
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")

            print(f"\nOperation completed:")
            print(f"  - Converted {converted_count} files to JPEG")
            print(f"  - Deleted {deleted_count} invalid files")
        else:
            print("Operation cancelled. No files were modified.")

    # Normalize .JPEG extensions to .jpeg
    for root, _, files in os.walk(directory):
        for filename in files:
            filename_parts = filename.split('.')
            if len(filename_parts) < 2:
                print(f"Skipping file with no extension: {filename}")
                continue
            filename_without_ext = '.'.join(filename_parts[:-1])
            filename_ext = filename_parts[-1]

            if filename_ext.lower() in ['jpeg', 'jpg']:
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, filename_without_ext + '.jpeg')
                if old_path != new_path:
                    try:
                        os.rename(old_path, new_path)
                    except Exception as e:
                        print(f"Error renaming {old_path}: {e}")
            else:
                print(f"Unsupported extension: {filename}")


def main():
    """Main entry point for the convert_images script."""
    parser = argparse.ArgumentParser(
        description="Convert PNG/HEIC images to high-quality JPEG and clean invalid files."
    )
    parser.add_argument("directory", help="Directory to process")

    args = parser.parse_args()
    convert_directory(args.directory)


if __name__ == "__main__":
    main()

