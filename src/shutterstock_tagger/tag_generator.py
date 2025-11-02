"""
Tag generation module.

Uses AWS Bedrock to generate titles, keywords, and categories for stock photography.
"""

import os
import argparse
from .bedrock_client import read_prompt, process_images, get_aws_region


def main():
    """Main entry point for the tag generator script."""
    # Get config directory relative to this file
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
    
    system_prompt_file = os.path.join(config_dir, "system_prompt.txt")
    prompt_file = os.path.join(config_dir, "prompt.txt")
    region = get_aws_region()

    parser = argparse.ArgumentParser(description="Generate tags for images using AWS Bedrock")
    parser.add_argument("--image_folder", required=True, help="Folder containing images")
    parser.add_argument("--output_folder", required=True, help="Folder to save responses")

    args = parser.parse_args()

    system_prompt = read_prompt(system_prompt_file)
    prompt = read_prompt(prompt_file)

    process_images(args.image_folder, args.output_folder, system_prompt, prompt, region)


if __name__ == "__main__":
    main()

