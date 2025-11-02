"""
File cleaning module.

Removes images that don't meet minimum requirements for stock photography:
- Must be JPEG format
- Must have at least 4 million pixels
- Must be under 15MB (AWS Bedrock API limit)
"""

import os
from PIL import Image
import argparse


def is_valid_jpeg(filepath):
    """
    Check if file is a JPEG and has at least 4 million pixels.
    
    Args:
        filepath (str): Path to the file to check
        
    Returns:
        tuple: (is_valid, megapixels) - Boolean validity and megapixel count
    """
    # Check extension first
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in [".jpg", ".jpeg"]:
        return False, 0

    try:
        # Open the image and get dimensions
        with Image.open(filepath) as img:
            width, height = img.size
            pixel_count = width * height
            # Check if image has at least 4 million pixels
            return pixel_count >= 4_000_000, pixel_count / 1_000_000
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, 0


def clean_directory(directory):
    """
    Find files to delete and ask for confirmation.
    
    Removes files that are:
    - Not JPEG format
    - Smaller than 4 million pixels
    - Larger than 15MB (AWS Bedrock API limit)
    
    Args:
        directory (str): Directory path to clean
    """
    files_to_delete = []

    print(f"Scanning directory: {directory}")

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip directories and non-image files
            if os.path.isdir(filepath):
                continue

            # Check if it's a valid JPEG with sufficient size
            big_enough, megapixel = is_valid_jpeg(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            # Remove files that don't meet minimum pixel requirements
            if not big_enough:
                files_to_delete.append((filepath, size_mb, megapixel))
            # Remove files larger than 15MB, which will cause issues with Bedrock API
            elif size_mb > 15:
                files_to_delete.append((filepath, size_mb, megapixel))

    # Show files to be deleted
    if not files_to_delete:
        print("No files to delete.")
        return

    print(f"\nFound {len(files_to_delete)} files to delete:")
    for filepath, size_mb, megapixel in files_to_delete:
        print(f"  - {filepath} ({size_mb:.2f} MB, {megapixel:.2f} MP)")

    # Ask for confirmation
    confirmation = input("\nDo you want to delete these files? (yes/no): ")

    if confirmation.lower() in ["yes", "y"]:
        # Delete files
        for filepath, _, _ in files_to_delete:
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
        print(f"\nSuccessfully deleted {len(files_to_delete)} files.")
    else:
        print("Operation cancelled. No files were deleted.")


def main():
    """Main entry point for the clean_files script."""
    parser = argparse.ArgumentParser(
        description="Clean directory by removing non-JPEG files and JPEGs smaller than 4 million pixels."
    )
    parser.add_argument("directory", help="Directory to clean")

    args = parser.parse_args()
    clean_directory(args.directory)


if __name__ == "__main__":
    main()

