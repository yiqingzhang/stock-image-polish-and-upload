# Workflow Guide

This guide provides detailed information about each step in the Shutterstock Image Tagger workflow.

## Table of Contents

- [Overview](#overview)
- [Detailed Step-by-Step Guide](#detailed-step-by-step-guide)
- [State Management](#state-management)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Overview

The Shutterstock Image Tagger workflow consists of 8 automated steps that transform raw images into upload-ready batches with AI-generated metadata.

```
Raw Images → Convert → Clean → Classify → Organize → Tag → Analyze → Batch → Upload
```

## Detailed Step-by-Step Guide

### Step 0: Convert Images

**Module**: `convert_images.py`

**Purpose**: Convert HEIC/HEIF images to JPEG format with sRGB color profile.

**What it does**:
- Scans directory for HEIC/HEIF files
- Converts to high-quality JPEG (95% quality)
- Applies sRGB color profile for consistency
- Removes PNG files (not suitable for stock photography)
- Normalizes file extensions to `.jpeg`

**Requirements**:
- Input: Images in `1_raw_export/` folder
- Supported formats: HEIC, HEIF, JPEG, JPG

**Command**:
```bash
python -m shutterstock_tagger.convert_images work_dir/1_raw_export
```

**Output**: Converted JPEG files in the same directory

---

### Step 1: Clean Files

**Module**: `clean_files.py`

**Purpose**: Remove images that don't meet stock photography requirements.

**What it does**:
- Checks image dimensions (must be ≥ 4 megapixels)
- Checks file size (must be ≤ 15MB for AWS Bedrock)
- Removes non-JPEG files
- Displays statistics before deletion

**Requirements**:
- Minimum resolution: 4 megapixels (e.g., 2000×2000)
- Maximum file size: 15MB
- Format: JPEG only

**Command**:
```bash
python -m shutterstock_tagger.clean_files work_dir/1_raw_export
```

**Output**: Filtered image set meeting requirements

---

### Step 2: Binary Classification

**Module**: `binary_classifier.py`

**Purpose**: Use AI to evaluate if images are suitable for stock photography.

**What it does**:
- Sends each image to AWS Bedrock
- Evaluates against stock photography criteria:
  - No recognizable faces
  - No trademarks or logos
  - No famous landmarks
  - Good composition and quality
  - No watermarks or timestamps
- Returns: YES/NO decision and LOW/MEDIUM/HIGH likelihood

**Requirements**:
- AWS credentials configured
- Access to AWS Bedrock
- Config files: `system_prompt_binary.txt`, `prompt_binary.txt`

**Command**:
```bash
python -m shutterstock_tagger.binary_classifier \
  --image_folder work_dir/1_raw_export \
  --output_folder work_dir/2_binary_output
```

**Output**: Text files with classification results (`*_binary_response.txt`)

**Example Output**:
```
Suitable for Upload: YES
Likelihood of Acceptance: HIGH
```

---

### Step 3: Organize Files

**Module**: `file_organizer.py`

**Purpose**: Sort images into folders based on classification results.

**What it does**:
- Reads classification results from Step 2
- Copies images to appropriate folders:
  - `yes/` - Suitable for upload
  - `no/` - Not suitable
  - `high/` - High likelihood of acceptance
  - `medium/` - Medium likelihood
  - `low/` - Low likelihood

**Command**:
```bash
python -m shutterstock_tagger.file_organizer \
  --source_dir work_dir/1_raw_export \
  --label_dir work_dir/2_binary_output \
  --results_dir work_dir/3_copied_dest
```

**Output**: Organized folders in `3_copied_dest/`

**Folder Structure**:
```
3_copied_dest/
├── yes/
├── no/
├── high/      ← Best images for upload
├── medium/
└── low/
```

---

### Step 4: Folder Cleanup

**Module**: `folder_cleanup.py`

**Purpose**: Remove temporary folders to save disk space.

**What it does**:
- Deletes `yes/`, `no/`, `low/`, `medium/` folders
- Deletes original `1_raw_export/` folder
- Keeps only `high/` folder with best images
- Requires user confirmation before deletion

**Command**:
```bash
python -m shutterstock_tagger.folder_cleanup --base_folder work_dir
```

**Output**: Cleaned directory structure

---

### Step 5: Generate Tags

**Module**: `tag_generator.py`

**Purpose**: Generate titles, keywords, and categories using AI.

**What it does**:
- Processes images in `high/` folder
- Uses AWS Bedrock to analyze each image
- Generates:
  - **Title**: Attractive, SEO-friendly (5-200 characters)
  - **Keywords**: 15-25 unique, comma-separated tags
  - **Category**: One of Shutterstock's official categories

**Requirements**:
- Config files: `system_prompt.txt`, `prompt.txt`
- Images in `3_copied_dest/high/`

**Command**:
```bash
python -m shutterstock_tagger.tag_generator \
  --image_folder work_dir/3_copied_dest/high \
  --output_folder work_dir/5_tag_output
```

**Output**: Text files with metadata (`*_response.txt`)

**Example Output**:
```
Title: Serene Mountain Lake at Sunset with Reflection
Keywords: mountain, lake, sunset, reflection, nature, landscape, scenic, peaceful, water, sky, clouds, outdoor, travel, wilderness, panorama
Category: Nature
```

---

### Step 6: Analyze Results

**Module**: `result_analyzer.py`

**Purpose**: Convert AI-generated tags into CSV format for Shutterstock upload.

**What it does**:
- Parses text files from Step 5
- Extracts title, keywords, and category
- Ensures unique keywords (removes duplicates)
- Adds required Shutterstock fields:
  - Editorial: no
  - Mature content: no
  - Illustration: no
- Creates CSV file matching Shutterstock's format

**Command**:
```bash
python -m shutterstock_tagger.result_analyzer \
  --folder_path work_dir/5_tag_output \
  --output_file 6_image_tags.csv
```

**Output**: `6_image_tags.csv` with all metadata

**CSV Format**:
```csv
Filename,Description,Keywords,Categories,Editorial,Mature content,illustration
image1.jpeg,"Title here","keyword1, keyword2, ...",Nature,no,no,no
```

---

### Step 7: Split into Batches

**Module**: `batch_splitter.py`

**Purpose**: Split images into batches of 100 for efficient uploading.

**What it does**:
- Reads master CSV file
- Creates batch folders (batch_1, batch_2, etc.)
- Copies 100 images per batch
- Creates individual CSV files for each batch
- Maintains metadata consistency

**Command**:
```bash
python -m shutterstock_tagger.batch_splitter \
  --single_output_folder work_dir/3_copied_dest/high \
  --tag_files work_dir/6_image_tags.csv \
  --batch_output_folder work_dir/7_batch_output
```

**Output**: Batch folders ready for upload

**Batch Structure**:
```
7_batch_output/
├── batch_1/
│   ├── image001.jpeg
│   ├── image002.jpeg
│   └── ... (100 images)
├── batch_1_tags.csv
├── batch_2/
│   └── ... (100 images)
├── batch_2_tags.csv
└── ...
```

---

## State Management

The workflow uses a `state.txt` file to track progress:

```
-1  → Step 0 pending (convert images)
 0  → Step 1 pending (clean files)
 1  → Step 2 pending (binary classification)
 2  → Step 3 pending (organize files)
 3  → Step 4 pending (cleanup folders)
 4  → Step 5 pending (generate tags)
 5  → Step 6 pending (analyze results)
 6  → Step 7 pending (split batches)
 7  → All steps completed
```

### Resuming from Interruption

If the workflow is interrupted, simply run it again:

```bash
python -m shutterstock_tagger.workflow --base_folder work_dir
```

The workflow will automatically resume from the last completed step.

### Resetting State

To start over from the beginning:

```bash
rm work_dir/state.txt
```

---

## Error Handling

### Error Logs

Errors are logged to `error_log.txt` in the work directory:

```
Error processing image123.jpeg: AWS Bedrock rate limit exceeded
No results file found for image456.jpeg
```

### Common Errors and Solutions

**AWS Credentials Error**:
```
Solution: Configure AWS CLI or set environment variables
aws configure
```

**Bedrock Access Denied**:
```
Solution: Request access to AWS Bedrock models in your region
Check IAM permissions for bedrock:InvokeModel
```

**Image Too Large**:
```
Solution: Images > 15MB are automatically removed in Step 1
Manually resize if needed before processing
```

**Missing Classification Results**:
```
Solution: Re-run Step 2 for missing images
Check error_log.txt for API failures
```

---

## Best Practices

### 1. Organize Input Images

Before starting:
- Review images manually
- Remove obvious rejects
- Ensure images are properly exposed and focused

### 2. Monitor Progress

- Check `error_log.txt` regularly
- Review classification results after Step 2
- Verify generated tags after Step 5

### 3. Customize Prompts

Edit config files to match your style:
- Add specific keywords for your niche
- Adjust tone of titles
- Emphasize certain categories

### 4. Batch Size Optimization

- Default: 100 images per batch
- Adjust based on your upload speed
- Smaller batches = more frequent uploads

### 5. Quality Control

Before uploading:
- Review a sample of generated tags
- Check for accuracy and relevance
- Verify categories are appropriate

### 6. Cost Management

AWS Bedrock charges per API call:
- Monitor usage in AWS Console
- Set billing alerts
- Consider processing in smaller batches

---

## Tips for Better Results

### Image Selection

✅ **Good candidates**:
- Clear, well-composed images
- Generic subjects with broad appeal
- Proper exposure and focus
- No visible defects

❌ **Poor candidates**:
- Blurry or poorly exposed
- Recognizable people or brands
- Niche subjects with limited appeal
- Images with watermarks

### Prompt Optimization

Customize prompts for your image style:
- **Nature photography**: Emphasize location types, weather, seasons
- **Food photography**: Focus on ingredients, cuisine types, occasions
- **Abstract**: Highlight colors, patterns, emotions
- **Business**: Emphasize concepts, industries, use cases

### Tag Quality

Good tags are:
- **Specific**: "golden retriever" vs "dog"
- **Varied**: Mix of specific and general terms
- **Relevant**: Directly related to image content
- **Searchable**: Terms people actually search for

---

## Troubleshooting Workflow

### Workflow Stuck?

1. Check `state.txt` to see current step
2. Review `error_log.txt` for errors
3. Manually run the next step to see detailed errors
4. Fix issues and resume workflow

### Unexpected Results?

1. Review AI-generated responses in output folders
2. Adjust prompts in `config/` directory
3. Re-run specific steps after changes
4. Consider manual review of edge cases

### Performance Issues?

1. Process smaller batches of images
2. Use a faster AWS region
3. Increase AWS Bedrock quotas
4. Run during off-peak hours

---

## Next Steps

After completing the workflow:

1. **Review Output**: Check `7_batch_output/` folders
2. **Quality Check**: Sample review of tags and images
3. **Upload**: Use Shutterstock's batch upload feature
4. **Track Results**: Monitor acceptance rates
5. **Iterate**: Adjust prompts based on feedback

---

For more information, see:
- [README.md](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guide
- [Configuration Guide](CONFIG_GUIDE.md) - Detailed configuration options

