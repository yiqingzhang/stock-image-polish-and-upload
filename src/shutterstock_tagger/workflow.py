"""
Workflow orchestration module.

Manages the complete pipeline from raw images to upload-ready batches.
"""

import os
import argparse


RAW_EXPORT_PATH = "1_raw_export"
LABEL_FOLDER = "2_binary_output"


def get_state_completed(state_file):
    """
    Check the current workflow state.
    
    Args:
        state_file (str): Path to the state file
        
    Returns:
        int: Current state number
    """
    assert os.path.exists(state_file), f"State file {state_file} does not exist."

    with open(state_file, "r") as f:
        content = f.read().strip()
        return int(content)


def update_state_completed(state_file, state):
    """
    Update the workflow state.
    
    Args:
        state_file (str): Path to the state file
        state (int): New state number
    """
    with open(state_file, "w") as f:
        f.write(str(state))
    print(f"State updated to {state} in {state_file}.")


def step_0_convert_images(base_folder):
    """
    Step 0: Convert HEIC/HEIF images to JPEG format.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    assert os.path.exists(raw_input_path), f"Raw input path {raw_input_path} does not exist."
    print(f"Converting images in {raw_input_path}...")

    command = f"python -m shutterstock_tagger.convert_images '{raw_input_path}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to convert files in {raw_input_path}.")
        return False
    print("Step 0: Convert files done.")
    return True


def step_1_clean_files(base_folder):
    """
    Step 1: Clean files by removing images that don't meet requirements.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    assert os.path.exists(raw_input_path), f"Raw input path {raw_input_path} does not exist."
    print(f"Processing images in {raw_input_path}...")

    command = f"python -m shutterstock_tagger.clean_files '{raw_input_path}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to clean files in {raw_input_path}.")
        return False
    print("Step 1: Cleaned files done.")
    return True


def step_2_get_images_binary(base_folder):
    """
    Step 2: Classify images for suitability using AWS Bedrock.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    label_folder = os.path.join(base_folder, LABEL_FOLDER)
    assert os.path.exists(raw_input_path), f"Raw input path {raw_input_path} does not exist."
    print(f"Processing images in {raw_input_path}...")

    command = f"python -m shutterstock_tagger.binary_classifier --image_folder '{raw_input_path}' --output_folder '{label_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to get images binary in {raw_input_path}.")
        return False
    print("Step 2: Get images binary done.")
    return True


def step_3_move_files(base_folder):
    """
    Step 3: Organize files based on classification results.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    label_folder = os.path.join(base_folder, LABEL_FOLDER)
    assert os.path.exists(label_folder), f"label_folder {label_folder} does not exist."
    copied_dest_folder = os.path.join(base_folder, "3_copied_dest")
    print(f"Copying images in {raw_input_path} to {copied_dest_folder}...")

    command = f"python -m shutterstock_tagger.file_organizer --source_dir '{raw_input_path}' --label_dir '{label_folder}' --results_dir '{copied_dest_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to move files from {raw_input_path} to {copied_dest_folder}.")
        return False

    print("Step 3: Move files done.")
    return True


def step_4_delete_folders(base_folder):
    """
    Step 4: Clean up temporary folders.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    command = f"python -m shutterstock_tagger.folder_cleanup --base_folder '{base_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to delete folders in {base_folder}.")
        return False
    print("Step 4: Delete folders done.")
    return True


def step_5_generate_tags(base_folder):
    """
    Step 5: Generate tags, titles, and categories using AWS Bedrock.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    copied_dest_folder = os.path.join(base_folder, "3_copied_dest/high")
    tag_output_folder = os.path.join(base_folder, "5_tag_output")
    assert os.path.exists(copied_dest_folder), f"Copied destination folder {copied_dest_folder} does not exist."
    print(f"Processing images in {copied_dest_folder}...")

    command = f"python -m shutterstock_tagger.tag_generator --image_folder '{copied_dest_folder}' --output_folder '{tag_output_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to run tag_generator on images in {copied_dest_folder}.")
        return False
    print("Step 5: Generate tags done.")
    return True


def step_6_analyze_results(base_folder):
    """
    Step 6: Analyze results and create CSV for upload.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    tag_output_folder = os.path.join(base_folder, "5_tag_output")
    assert os.path.exists(tag_output_folder), f"Tag output folder {tag_output_folder} does not exist."
    print(f"Analyzing results in {tag_output_folder}...")

    command = f"python -m shutterstock_tagger.result_analyzer --folder_path '{tag_output_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to analyze results in {tag_output_folder}.")
        return False
    print("Step 6: Analyze results done.")
    return True


def step_7_split_upload_batch(base_folder):
    """
    Step 7: Split images into upload batches of 100.
    
    Args:
        base_folder (str): Base working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    single_output_folder = os.path.join(base_folder, "3_copied_dest/high")
    batch_output_folder = os.path.join(base_folder, "7_batch_output")
    if not os.path.exists(batch_output_folder):
        os.makedirs(batch_output_folder)
    assert os.path.exists(single_output_folder), f"Tag output folder {single_output_folder} does not exist."
    print(f"Splitting upload batches in {single_output_folder}...")
    tag_file = os.path.join(base_folder, "6_image_tags.csv")
    command = f"python -m shutterstock_tagger.batch_splitter --single_output_folder '{single_output_folder}' --tag_files '{tag_file}' --batch_output_folder '{batch_output_folder}'"
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to split upload batches in {single_output_folder}.")
        return False
    print("Step 7: Split upload batches done.")
    return True


def process_images(base_folder):
    """
    Main workflow orchestrator. Executes all steps in sequence.
    
    Args:
        base_folder (str): Base working directory
    """
    state_file_path = os.path.join(base_folder, "state.txt")

    if not os.path.exists(state_file_path):
        print(f"State file {state_file_path} does not exist. Initializing state to -1.")
        update_state_completed(state_file_path, -1)

    state_completed = get_state_completed(state_file_path)
    
    # Execute each step in sequence
    if state_completed == -1:
        if step_0_convert_images(base_folder):
            update_state_completed(state_file_path, 0)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 0:
        if step_1_clean_files(base_folder):
            update_state_completed(state_file_path, 1)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 1:
        if step_2_get_images_binary(base_folder):
            update_state_completed(state_file_path, 2)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 2:
        if step_3_move_files(base_folder):
            update_state_completed(state_file_path, 3)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 3:
        if step_4_delete_folders(base_folder):
            update_state_completed(state_file_path, 4)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 4:
        if step_5_generate_tags(base_folder):
            update_state_completed(state_file_path, 5)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 5:
        if step_6_analyze_results(base_folder):
            update_state_completed(state_file_path, 6)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 6:
        if step_7_split_upload_batch(base_folder):
            update_state_completed(state_file_path, 7)

    print("All steps completed successfully.")
    print(f"Folder of images to submit: {os.path.join(base_folder, '7_batch_output')}")


def main():
    """Main entry point for the workflow script."""
    parser = argparse.ArgumentParser(description="Process images with AWS Bedrock.")
    parser.add_argument(
        "--base_folder",
        type=str,
        required=True,
        help="Path to the folder containing images.",
    )

    args = parser.parse_args()
    process_images(args.base_folder)


if __name__ == "__main__":
    main()

