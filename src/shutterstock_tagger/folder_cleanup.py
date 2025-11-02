"""
Folder cleanup module.

Handles deletion of temporary folders and files after processing.
"""

import os
import shutil
import argparse


def delete_folder(folder_path):
    """
    Delete a folder if it exists, with user confirmation.
    
    Args:
        folder_path (str): Path to the folder to delete
    """
    if os.path.exists(folder_path):
        # Confirm deletion
        confirm = input(
            f"Are you sure you want to delete the folder: {folder_path}? (yes/no): "
        )
        if confirm.lower() != "yes":
            print("Deletion cancelled.")
            return

        try:
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder {folder_path}: {e}")
    else:
        print(f"Folder does not exist: {folder_path}")


def delete_sub_folders(base_dest_dir):
    """
    Delete temporary subfolders in the destination directory.
    
    Args:
        base_dest_dir (str): Base destination directory
    """
    delete_folder(f"{base_dest_dir}/yes")
    delete_folder(f"{base_dest_dir}/no")
    delete_folder(f"{base_dest_dir}/low")
    delete_folder(f"{base_dest_dir}/medium")


def delete_folders(base_folder):
    """
    Delete temporary folders after processing is complete.
    
    Args:
        base_folder (str): Base folder containing all processing directories
    """
    copied_dir = os.path.join(base_folder, "3_copied_dest")
    delete_sub_folders(copied_dir)
    print(f"Deleted subfolders in {copied_dir}")

    delete_folder(os.path.join(base_folder, "1_raw_export"))
    print(f"Deleted folder: {os.path.join(base_folder, '1_raw_export')}")


def main():
    """Main entry point for the folder cleanup script."""
    parser = argparse.ArgumentParser(
        description="Delete subfolders in the base destination directory."
    )
    parser.add_argument(
        "--base_folder",
        type=str,
        required=True,
        help="Base folder path where subfolders will be deleted.",
    )

    args = parser.parse_args()
    delete_folders(args.base_folder)


if __name__ == "__main__":
    main()

