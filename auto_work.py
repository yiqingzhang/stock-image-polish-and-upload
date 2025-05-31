import os

RAW_EXPORT_PATH = "1_raw_export"
LABEL_FOLDER = "2_binary_output"


def get_state_completed(state_file):
    """Check if the state file indicates completion."""
    assert os.path.exists(state_file), f"State file {state_file} does not exist."

    with open(state_file, "r") as f:
        content = f.read().strip()
        return int(content)


def update_state_completed(state_file, state):
    """Update the state file with the current state."""
    with open(state_file, "w") as f:
        f.write(str(state))
    print(f"State updated to {state} in {state_file}.")


def step_1_clean_files(base_folder):

    # step 1:
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    assert os.path.exists(
        raw_input_path
    ), f"Raw input path {raw_input_path} does not exist."
    print(f"Processing images in {raw_input_path}...")

    command = f"python 1_clean_files.py {raw_input_path}"
    # run the command to clean files
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to clean files in {raw_input_path}.")
        return False
    print("Step 1: Cleaned files done.")
    return True


def step_2_get_images_binary(base_folder):
    # step 2:
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    label_folder = os.path.join(base_folder, LABEL_FOLDER)
    assert os.path.exists(
        raw_input_path
    ), f"Raw input path {raw_input_path} does not exist."
    print(f"Processing images in {raw_input_path}...")

    command = f"python 2_bedrock_run_binary.py --image_folder {raw_input_path} --output_folder {label_folder}"
    # run the command to get images binary
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to get images binary in {raw_input_path}.")
        return False
    print("Step 2: Get images binary done.")
    return True


def step_3_move_files(base_folder):
    # step 3:
    raw_input_path = os.path.join(base_folder, RAW_EXPORT_PATH)
    label_folder = os.path.join(base_folder, LABEL_FOLDER)
    assert os.path.exists(label_folder), f"label_folder {label_folder} does not exist."
    copied_dest_folder = os.path.join(base_folder, "3_copied_dest")
    print(f"Copying images in {raw_input_path} to {copied_dest_folder}...")

    command = f"python 3_move_files.py --source_dir {raw_input_path} --label_dir {label_folder} --results_dir {copied_dest_folder}"
    # run the command to move files, and check if the command was successful
    # run this command, and check if the command was successful via the return code
    ret = os.system(command)
    if ret != 0:
        print(
            f"Error: Failed to move files from {raw_input_path} to {copied_dest_folder}."
        )
        return False

    print("Step 3: Move files done.")

    return True


def step_4_delete_folders(base_folder):
    # step 4:

    command = f"python 4_delete_folders.py --base_folder {base_folder}"
    # run the command to delete folders
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to delete folders in {base_folder}.")
        return False
    print("Step 4: Delete folders done.")

    return True


def step_5_generate_tags(base_folder):
    # step 5:
    copied_dest_folder = os.path.join(base_folder, "3_copied_dest/high")
    tag_output_folder = os.path.join(base_folder, "5_tag_output")
    assert os.path.exists(
        copied_dest_folder
    ), f"Copied destination folder {copied_dest_folder} does not exist."
    print(f"Processing images in {copied_dest_folder}...")

    command = f"python 5_generate_tags.py --image_folder {copied_dest_folder} --output_folder {tag_output_folder}"
    # run the command to get images binary
    ret = os.system(command)
    if ret != 0:
        print(
            f"Error: Failed to run 5_generate_tags on images in {copied_dest_folder}."
        )
        return False
    print("Step 5: 5_generate_tags run done.")

    return True


def step_6_analyze_results(base_folder):
    # step 6:
    tag_output_folder = os.path.join(base_folder, "5_tag_output")
    assert os.path.exists(
        tag_output_folder
    ), f"Tag output folder {tag_output_folder} does not exist."
    print(f"Analyzing results in {tag_output_folder}...")

    command = f"python 6_result_analysis.py --folder_path {tag_output_folder}"
    # run the command to analyze results
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to analyze results in {tag_output_folder}.")
        return False
    print("Step 6: Analyze results done.")

    return True


def step_7_split_upload_batch(base_folder):
    # step 7:
    single_output_folder = os.path.join(base_folder, "3_copied_dest/high")
    batch_output_folder = os.path.join(base_folder, "7_batch_output")
    if not os.path.exists(batch_output_folder):
        os.makedirs(batch_output_folder)
    assert os.path.exists(
        single_output_folder
    ), f"Tag output folder {single_output_folder} does not exist."
    print(f"Splitting upload batches in {single_output_folder}...")
    tag_file = os.path.join(base_folder, "6_image_tags.csv")
    command = f"python 7_split_upload_batch.py --single_output_folder {single_output_folder} --tag_files {tag_file} --batch_output_folder {batch_output_folder}"
    # run the command to split upload batches
    ret = os.system(command)
    if ret != 0:
        print(f"Error: Failed to split upload batches in {single_output_folder}.")
        return False
    print("Step 7: Split upload batches done.")

    return True


def process_images(base_folder):

    state_file_path = os.path.join(base_folder, "state.txt")

    if not os.path.exists(state_file_path):
        print(f"State file {state_file_path} does not exist. Initializing state to 0.")
        update_state_completed(state_file_path, 0)
        state_completed = 0

    state_completed = get_state_completed(state_file_path)
    if state_completed == 0:
        ret = step_1_clean_files(base_folder)
        if ret:
            update_state_completed(state_file_path, 1)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 1:
        ret = step_2_get_images_binary(base_folder)
        if ret:
            update_state_completed(state_file_path, 2)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 2:
        ret = step_3_move_files(base_folder)
        if ret:
            update_state_completed(state_file_path, 3)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 3:
        ret = step_4_delete_folders(base_folder)
        if ret:
            update_state_completed(state_file_path, 4)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 4:
        ret = step_5_generate_tags(base_folder)
        if ret:
            update_state_completed(state_file_path, 5)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 5:
        ret = step_6_analyze_results(base_folder)
        if ret:
            update_state_completed(state_file_path, 6)

    state_completed = get_state_completed(state_file_path)
    if state_completed == 6:
        ret = step_7_split_upload_batch(base_folder)
        if ret:
            update_state_completed(state_file_path, 7)

    print("All steps completed successfully.")
    print(f"Folder of images to submit: {os.path.join(base_folder, '7_batch_output')}")


if __name__ == "__main__":

    import argparse
    import os

    parser = argparse.ArgumentParser(description="Process images with AWS Bedrock.")
    parser.add_argument(
        "--base_folder",
        type=str,
        required=True,
        help="Path to the folder containing images.",
    )

    args = parser.parse_args()

    process_images(args.base_folder)
