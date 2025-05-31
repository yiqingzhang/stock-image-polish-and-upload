import os
import shutil


def delete_folder(folder_path):
    """Delete a folder if it exists."""
    if os.path.exists(folder_path):
        # confirm deletion
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
    # get the error log file
    error_log_file = os.path.join(os.path.dirname(base_dest_dir), "error_log.txt")

    delete_folder(f"{base_dest_dir}/yes")
    delete_folder(f"{base_dest_dir}/no")
    delete_folder(f"{base_dest_dir}/low")
    delete_folder(f"{base_dest_dir}/medium")


def delete_folders(base_folder):
    copied_dir = os.path.join(base_folder, "3_copied_dest")
    delete_sub_folders(copied_dir)
    print(f"Deleted subfolders in {copied_dir}")

    delete_folder(os.path.join(base_folder, "1_raw_export"))
    print(f"Deleted folder: {os.path.join(base_folder, '1_raw_export')}")


if __name__ == "__main__":
    import argparse
    import os

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

    base_folder = args.base_folder

    delete_folders(base_folder)
