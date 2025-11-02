# Examples

This directory contains example usage and sample data for the Shutterstock Image Tagger.

## Quick Start Example

### 1. Basic Workflow

```bash
# Create a work directory
mkdir -p my_photos/1_raw_export

# Copy your images
cp /path/to/your/photos/*.jpg my_photos/1_raw_export/

# Run the complete workflow
python -m shutterstock_tagger.workflow --base_folder my_photos
```

### 2. Step-by-Step Execution

If you prefer to run each step individually:

```bash
# Step 0: Convert HEIC to JPEG
python -m shutterstock_tagger.convert_images my_photos/1_raw_export

# Step 1: Clean files
python -m shutterstock_tagger.clean_files my_photos/1_raw_export

# Step 2: Classify images
python -m shutterstock_tagger.binary_classifier \
  --image_folder my_photos/1_raw_export \
  --output_folder my_photos/2_binary_output

# Step 3: Organize files
python -m shutterstock_tagger.file_organizer \
  --source_dir my_photos/1_raw_export \
  --label_dir my_photos/2_binary_output \
  --results_dir my_photos/3_copied_dest

# Step 4: Cleanup (requires confirmation)
python -m shutterstock_tagger.folder_cleanup --base_folder my_photos

# Step 5: Generate tags
python -m shutterstock_tagger.tag_generator \
  --image_folder my_photos/3_copied_dest/high \
  --output_folder my_photos/5_tag_output

# Step 6: Create CSV
python -m shutterstock_tagger.result_analyzer \
  --folder_path my_photos/5_tag_output \
  --output_file 6_image_tags.csv

# Step 7: Split into batches
python -m shutterstock_tagger.batch_splitter \
  --single_output_folder my_photos/3_copied_dest/high \
  --tag_files my_photos/6_image_tags.csv \
  --batch_output_folder my_photos/7_batch_output
```

## Example Scenarios

### Scenario 1: Nature Photography

```bash
# Configure for nature photography
export AWS_REGION=us-east-1
export AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

# Process nature photos
python -m shutterstock_tagger.workflow --base_folder nature_photos/
```

**Expected Output**:
- Categories: Nature, Animals/Wildlife, Backgrounds/Textures
- Keywords: landscape, mountain, forest, wildlife, scenic, outdoor
- Titles: Descriptive and evocative

### Scenario 2: Food Photography

```bash
# Process food photos
python -m shutterstock_tagger.workflow --base_folder food_photos/
```

**Expected Output**:
- Categories: Food and drink
- Keywords: cuisine, ingredients, meal, restaurant, cooking, fresh
- Titles: Appetizing and descriptive

### Scenario 3: Business/Corporate

```bash
# Process business photos
python -m shutterstock_tagger.workflow --base_folder business_photos/
```

**Expected Output**:
- Categories: Business/Finance, People, Technology
- Keywords: office, meeting, teamwork, professional, corporate, business
- Titles: Professional and concept-focused

## Sample Output Structure

After running the workflow, your directory will look like:

```
my_photos/
├── 2_binary_output/
│   ├── IMG_001_binary_response.txt
│   ├── IMG_002_binary_response.txt
│   └── ...
├── 3_copied_dest/
│   └── high/
│       ├── IMG_001.jpeg
│       ├── IMG_002.jpeg
│       └── ...
├── 5_tag_output/
│   ├── IMG_001_response.txt
│   ├── IMG_002_response.txt
│   └── ...
├── 6_image_tags.csv
├── 7_batch_output/
│   ├── batch_1/
│   │   ├── IMG_001.jpeg
│   │   └── ... (100 images)
│   ├── batch_1_tags.csv
│   ├── batch_2/
│   └── batch_2_tags.csv
├── state.txt
└── error_log.txt
```

## Sample CSV Output

`batch_1_tags.csv`:
```csv
Filename,Description,Keywords,Categories,Editorial,Mature content,illustration
IMG_001.jpeg,"Serene Mountain Lake at Sunset","mountain, lake, sunset, reflection, nature, landscape, scenic, peaceful, water, sky",Nature,no,no,no
IMG_002.jpeg,"Fresh Organic Vegetables on Wooden Table","vegetables, organic, fresh, healthy, food, nutrition, farm, produce, colorful",Food and drink,no,no,no
```

## Customization Examples

### Custom Prompts

Edit `config/prompt.txt` for custom tag generation:

```
Please analyze this image and generate:
1. A creative title (max 150 characters)
2. 20-30 specific keywords focusing on [YOUR_NICHE]
3. The most appropriate category from Shutterstock's list

Emphasize: [YOUR_SPECIFIC_REQUIREMENTS]
```

### Custom Model Configuration

Use a different AWS Bedrock model:

```bash
export AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
python -m shutterstock_tagger.workflow --base_folder my_photos/
```

## Troubleshooting Examples

### Resume from Interruption

If the workflow is interrupted:

```bash
# Check current state
cat my_photos/state.txt

# Resume from where it stopped
python -m shutterstock_tagger.workflow --base_folder my_photos/
```

### Reprocess Specific Images

```bash
# Remove specific images from output
rm my_photos/5_tag_output/IMG_001_response.txt

# Rerun tag generation
python -m shutterstock_tagger.tag_generator \
  --image_folder my_photos/3_copied_dest/high \
  --output_folder my_photos/5_tag_output
```

### Check for Errors

```bash
# View error log
cat my_photos/error_log.txt

# Count errors
grep "Error" my_photos/error_log.txt | wc -l
```

## Performance Tips

### Batch Processing

For large collections (1000+ images):

```bash
# Process in smaller batches
mkdir batch1 batch2 batch3

# Split images
mv my_photos/1_raw_export/IMG_0001-IMG_0500* batch1/1_raw_export/
mv my_photos/1_raw_export/IMG_0501-IMG_1000* batch2/1_raw_export/
mv my_photos/1_raw_export/IMG_1001-IMG_1500* batch3/1_raw_export/

# Process each batch
for batch in batch1 batch2 batch3; do
  python -m shutterstock_tagger.workflow --base_folder $batch/
done
```

### Parallel Processing

Process multiple batches in parallel (requires multiple AWS accounts or high quotas):

```bash
# Terminal 1
python -m shutterstock_tagger.workflow --base_folder batch1/ &

# Terminal 2
python -m shutterstock_tagger.workflow --base_folder batch2/ &

# Terminal 3
python -m shutterstock_tagger.workflow --base_folder batch3/ &
```

## Cost Estimation

AWS Bedrock costs (approximate):

- **Nova Lite**: ~$0.0008 per image (2 API calls)
- **1000 images**: ~$0.80
- **10000 images**: ~$8.00

Actual costs may vary based on:
- Image size
- Response length
- AWS region
- Model selection

## Next Steps

After generating batches:

1. **Review**: Sample check tags for accuracy
2. **Upload**: Use Shutterstock's batch upload feature
3. **Track**: Monitor acceptance rates
4. **Optimize**: Adjust prompts based on results
5. **Scale**: Process more images with confidence

For more information, see:
- [Workflow Guide](../docs/WORKFLOW_GUIDE.md)
- [README](../README.md)
- [Contributing](../CONTRIBUTING.md)

