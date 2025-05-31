#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import pandas as pd
from pathlib import Path


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Split files into batches of 100 based on filenames in a CSV file"
    )
    parser.add_argument(
        "--single_output_folder", help="Folder containing all the images"
    )
    parser.add_argument(
        "--tag_files",
        help="CSV file with filenames referring to files in single_output_folder",
    )
    parser.add_argument(
        "--batch_output_folder", help="Destination folder for batched outputs"
    )
    return parser


def main():
    # Parse command line arguments
    parser = create_parser()
    args = parser.parse_args()

    # Get paths from arguments
    input_folder = Path(args.single_output_folder)
    csv_file = Path(args.tag_files)
    output_folder = Path(args.batch_output_folder)

    # Check if paths are valid
    if not input_folder.exists() or not input_folder.is_dir():
        print(
            f"Error: Input folder '{input_folder}' does not exist or is not a directory"
        )
        sys.exit(1)

    if not csv_file.exists() or not csv_file.is_file():
        print(f"Error: CSV file '{csv_file}' does not exist or is not a file")
        sys.exit(1)

    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Read CSV file using pandas
    try:
        df = pd.read_csv(csv_file)
        print(f"Read CSV with {len(df)} rows and columns: {', '.join(df.columns)}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Get the filename column (assuming it's the first column)
    filename_col = df.columns[0]

    # Create batches of 100 files
    batch_size = 100
    total_files = len(df)
    total_batches = (total_files + batch_size - 1) // batch_size  # Ceiling division

    print(f"Found {total_files} files to process. Will create {total_batches} batches.")

    for batch_num in range(1, total_batches + 1):
        # Create batch folder
        batch_folder = output_folder / f"batch_{batch_num}"
        batch_folder.mkdir(exist_ok=True)

        # Get rows for this batch
        start_idx = (batch_num - 1) * batch_size
        end_idx = min(batch_num * batch_size, total_files)
        batch_df = df.iloc[start_idx:end_idx].copy()

        print(
            f"Processing batch {batch_num}/{total_batches} with {len(batch_df)} files..."
        )

        # Create CSV file for this batch
        csv_output_path = output_folder / f"batch_{batch_num}_tags.csv"
        batch_df.to_csv(csv_output_path, index=False)
        print(f"Created CSV file {csv_output_path}")

        # Copy files to batch folder
        for filename in batch_df[filename_col]:
            source_file = input_folder / filename
            if source_file.exists():
                try:
                    shutil.copy2(source_file, batch_folder)
                except Exception as e:
                    print(f"Error copying {filename}: {e}")
            else:
                print(f"Warning: File {filename} not found in input folder")

        print(f"Completed batch {batch_num}")

    print(f"All batches created successfully in {output_folder}")


if __name__ == "__main__":
    main()
