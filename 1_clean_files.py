import os
import sys
from PIL import Image
import argparse


def is_valid_jpeg(filepath):
    """Check if file is a JPEG and has at least 4 million pixels."""
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
    """Find files to delete and ask for confirmation."""
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
            # Get file size for reporting
            if not big_enough:
                files_to_delete.append((filepath, size_mb, megapixel))
            # remove files larger than 15MB, which will cause issue when calling the bedrock API
            if size_mb > 15:
                files_to_delete.append((filepath, size_mb, megapixel))

    # Show files to be deleted
    if not files_to_delete:
        print("No files to delete.")
        return

    print(f"\nFound {len(files_to_delete)} files to delete:")
    for filepath, size_mb, megapixel in files_to_delete:
        print(f"  - {filepath} ({size_mb:.2f} MB) - {megapixel:.2f} MP)")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean directory by removing non-JPEG files and JPEGs smaller than 4 million pixels."
    )
    parser.add_argument("directory", help="Directory to clean")

    args = parser.parse_args()
    clean_directory(args.directory)
