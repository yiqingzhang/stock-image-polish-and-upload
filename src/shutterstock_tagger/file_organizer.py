"""
File organization module.

Moves and organizes images based on classification results.
"""

import os
import shutil
import argparse


def create_folder_if_not_exists(folder_path):
    """
    Create a folder if it does not exist.
    
    Args:
        folder_path (str): Path to the folder to create
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def move_files(source_dir, label_dir, base_dest_dir):
    """
    Move files based on binary classification results.
    
    Organizes images into folders based on:
    - Upload decision (yes/no)
    - Likelihood of acceptance (low/medium/high)
    
    Args:
        source_dir (str): Directory containing source images
        label_dir (str): Directory containing classification results
        base_dest_dir (str): Base destination directory for organized files
    """
    # Get the error log file
    error_log_file = os.path.join(os.path.dirname(source_dir), "error_log.txt")

    # Create base destination directory if it doesn't exist
    os.makedirs(base_dest_dir, exist_ok=True)

    # Create subdirectories for different classifications
    create_folder_if_not_exists(f"{base_dest_dir}/yes")
    create_folder_if_not_exists(f"{base_dest_dir}/no")
    create_folder_if_not_exists(f"{base_dest_dir}/low")
    create_folder_if_not_exists(f"{base_dest_dir}/medium")
    create_folder_if_not_exists(f"{base_dest_dir}/high")

    # Process files in source directory
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)

        # Skip if not a file
        if not os.path.isfile(source_file):
            continue

        # Get base name without extension
        base_name = os.path.splitext(filename)[0]

        # Find matching txt file in labels directory
        txt_file = os.path.join(label_dir, base_name + "_binary_response.txt")

        if not os.path.exists(txt_file):
            print(f"No results file found for {filename}")
            with open(error_log_file, "a") as error_log:
                error_log.write(f"No results file found for {filename}\n")
            continue

        # Read classification from the txt file
        with open(txt_file, "r") as f:
            lines = f.readline().strip().split("\\n")
            if len(lines) < 2:
                print(f"Insufficient classification data in {txt_file}")
                with open(error_log_file, "a") as error_log:
                    error_log.write(f"Insufficient classification data in {txt_file}\n")
                continue

            upload_decision = lines[0].strip().lower()
            likelihood = lines[1].strip().lower()

            # Copy to appropriate folders based on classification
            if "yes" in upload_decision:
                dest_dir = os.path.join(base_dest_dir, "yes")
                dest_file = os.path.join(dest_dir, filename)
                shutil.copy2(source_file, dest_file)

            elif "no" in upload_decision:
                dest_dir = os.path.join(base_dest_dir, "no")
                dest_file = os.path.join(dest_dir, filename)
                shutil.copy2(source_file, dest_file)

            if "low" in likelihood:
                dest_dir = os.path.join(base_dest_dir, "low")
                dest_file = os.path.join(dest_dir, filename)
                shutil.copy2(source_file, dest_file)
            elif "medium" in likelihood:
                dest_dir = os.path.join(base_dest_dir, "medium")
                dest_file = os.path.join(dest_dir, filename)
                shutil.copy2(source_file, dest_file)
            elif "high" in likelihood:
                dest_dir = os.path.join(base_dest_dir, "high")
                dest_file = os.path.join(dest_dir, filename)
                shutil.copy2(source_file, dest_file)


def main():
    """Main entry point for the file organizer script."""
    parser = argparse.ArgumentParser(
        description="Move files based on classification results."
    )
    parser.add_argument(
        "--source_dir", type=str, help="Source directory containing files to move."
    )
    parser.add_argument(
        "--label_dir",
        type=str,
        help="Label directory containing classification results.",
    )
    parser.add_argument(
        "--results_dir", type=str, help="Directory containing classification results."
    )
    args = parser.parse_args()
    
    print(f"Source directory: {args.source_dir}")
    print(f"Label directory: {args.label_dir}")
    print(f"Results directory: {args.results_dir}")

    move_files(args.source_dir, args.label_dir, args.results_dir)


if __name__ == "__main__":
    main()

