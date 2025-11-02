"""
Binary image classification module.

Uses AWS Bedrock to determine if images are suitable for stock photography platforms.
"""

import os
import argparse
from pathlib import Path
from .bedrock_client import read_prompt, process_images, get_aws_region


def process_binary_classification(image_folder, output_folder, system_prompt_file, prompt_file, region=None):
    """
    Process images for binary classification (suitable/not suitable for upload).
    
    Args:
        image_folder (str): Folder containing images to classify
        output_folder (str): Folder to save classification results
        system_prompt_file (str): Path to system prompt file
        prompt_file (str): Path to prompt file
        region (str, optional): AWS region
    """
    system_prompt = read_prompt(system_prompt_file)
    prompt = read_prompt(prompt_file)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process images and save results with _binary_response suffix
    error_file = os.path.join(os.path.dirname(output_folder), "error_log.txt")
    
    from .bedrock_client import encode_image, call_bedrock_api
    import json
    
    # Process each image in the folder
    image_list = sorted(os.listdir(image_folder))
    total_size = len(image_list)
    print(f"Total images to process: {total_size}")

    for index, image_file in enumerate(image_list):
        # Show progress in percentage
        if index % 10 == 0:
            progress_percentage = (index + 1) / total_size * 100
            print(f"Processing {index + 1}/{total_size} images ({progress_percentage:.2f}%)")

        # Check if file is an image
        if any(image_file.lower().endswith(ext) for ext in [".jpg", ".jpeg"]):
            output_file = os.path.join(
                output_folder, f"{Path(image_file).stem}_binary_response.txt"
            )
            if os.path.exists(output_file):
                print(f"Skipping {image_file}, response already exists.")
                continue
                
            image_path = os.path.join(image_folder, image_file)
            print(f"Processing {image_path}...")

            # Encode image
            image_base64 = encode_image(image_path)

            # Call Bedrock API
            try:
                response = call_bedrock_api(image_base64, system_prompt, prompt, region)
            except Exception as e:
                err_msg = f"Error processing {image_file}: {e}"
                print(err_msg)
                with open(error_file, "a") as ef:
                    ef.write(err_msg + "\n")
                continue

            # Save response
            with open(output_file, "w") as f:
                json.dump(response, f, indent=2)

            print(f"Response saved to {output_file}")


def main():
    """Main entry point for the binary classifier script."""
    # Get config directory relative to this file
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
    
    system_prompt_file = os.path.join(config_dir, "system_prompt_binary.txt")
    prompt_file = os.path.join(config_dir, "prompt_binary.txt")
    region = get_aws_region()

    parser = argparse.ArgumentParser(description="Process images with AWS Bedrock for binary classification")
    parser.add_argument("--image_folder", required=True, help="Folder containing images")
    parser.add_argument("--output_folder", required=True, help="Folder to save responses")

    args = parser.parse_args()

    process_binary_classification(
        args.image_folder,
        args.output_folder,
        system_prompt_file,
        prompt_file,
        region
    )


if __name__ == "__main__":
    main()

