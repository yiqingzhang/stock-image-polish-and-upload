# Shuttlestock

A comprehensive workflow automation tool for preparing and uploading images to stock photography platforms like Shutterstock.

## Overview

This project provides an automated pipeline for processing images intended for stock photography platforms. It handles everything from initial image selection and cleaning to metadata generation and batch organization for uploading.

The workflow uses AWS Bedrock to analyze images for suitability and to generate appropriate titles, tags, and categories according to Shutterstock's requirements.

## Requirements

```
boto3
pandas
Pillow
```

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Project Structure

The project consists of several Python scripts that each handle a specific step in the workflow:

1. `1_clean_files.py` - Initial processing and cleaning of image files (remove files too small/too large/video)
2. `2_bedrock_run_binary.py` - Uses AWS Bedrock to analyze images for suitability
3. `3_move_files.py` - Sorts images based on analysis results
4. `4_delete_folders.py` - Cleans up temporary files and folders (delete photos not suitable for uploads)
5. `5_generate_tags.py` - Generates tags, titles, and categories for selected images (via AWS bedrock models)
6. `6_result_analysis.py` - Analyzes the results of the tagging process
7. `7_split_upload_batch.py` - Splits images into batches for uploading (100 per batch)
8. `auto_work.py` - *Main script that orchestrates the entire workflow*

## Workflow Process

The `auto_work.py` script orchestrates a 7-step workflow:

1. **Clean Files**: Prepares and organizes raw image files for processing
2. **Binary Analysis**: Uses AWS Bedrock to analyze each image and determine if it's suitable for stock photography based on platform guidelines
3. **Move Files**: Sorts images into appropriate folders based on the analysis results
4. **Delete Folders**: Cleans up temporary directories
5. **Generate Tags**: Generates appropriate titles, tags, and categories for approved images using AI
6. **Result Analysis**: Analyzes and validates the generated metadata
7. **Split Upload Batch**: Organizes images into batches of 100 for uploading to Shutterstock

The workflow uses a state system stored in a `state.txt` file to track progress, allowing you to pause and resume the process at any point.

## How to Use

1. Create a work directory with a `1_raw_export` folder containing your original images:

```
work_dir/
└── 1_raw_export/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

2. Run the main script, pointing to your work directory:

```bash
python auto_work.py --base_folder /path/to/work_dir
```

3. The script will process all images and create a final batch folder structure ready for upload:
There is some checkpoint that require verification (enter yes) before folder deletion

```
work_dir/
└── 7_batch_output/
    ├── batch_1/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── batch_2/
    │   └── ...
    └── batch_1_tags.csv
    └── batch_2_tags.csv
```

4. Upload to shuttlestock batch by batch and using the csv files for batch upload (100 each time.)

## Prompt Templates

The project includes several prompt templates for the AI analysis:

- `prompt.txt` - Used for generating titles, tags, and categories
- `prompt_binary.txt` - Used for binary classification of images
- `system_prompt.txt` - System-level prompt for the AI
- `system_prompt_binary.txt` - System-level prompt for binary classification

## State Management

The workflow maintains its state in a `state.txt` file in the work directory. This allows the process to be resumed from where it left off if interrupted. Each step updates the state file upon successful completion.

## Output Structure

After processing, your images will be organized as follows:

- Selected images with high likelihood of acceptance: `3_copied_dest/high/`
- Generated tags: `5_tag_output/`
- Upload-ready batches: `7_batch_output/`

Each batch in the output directory (`7_batch_output/`) includes:
- Up to 100 images per batch
- A corresponding CSV file with all the metadata needed for upload