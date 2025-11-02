# Quick Reference Guide

A cheat sheet for common tasks and commands.

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/shutterstock-image-tagger.git
cd shutterstock-image-tagger

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Configure AWS
aws configure
cp .env.example .env
# Edit .env with your settings
```

## Basic Usage

### Complete Workflow
```bash
# Prepare directory
mkdir -p work_dir/1_raw_export
cp /path/to/images/* work_dir/1_raw_export/

# Run workflow
python -m shutterstock_tagger.workflow --base_folder work_dir

# Output: work_dir/7_batch_output/
```

## Individual Commands

### Convert Images
```bash
python -m shutterstock_tagger.convert_images DIRECTORY
```
Converts HEIC/HEIF to JPEG with sRGB profile.

### Clean Files
```bash
python -m shutterstock_tagger.clean_files DIRECTORY
```
Removes images < 4MP or > 15MB.

### Classify Images
```bash
python -m shutterstock_tagger.binary_classifier \
  --image_folder INPUT_DIR \
  --output_folder OUTPUT_DIR
```
AI classification for suitability.

### Organize Files
```bash
python -m shutterstock_tagger.file_organizer \
  --source_dir SOURCE \
  --label_dir LABELS \
  --results_dir RESULTS
```
Sorts images by quality.

### Cleanup Folders
```bash
python -m shutterstock_tagger.folder_cleanup --base_folder BASE_DIR
```
Removes temporary folders.

### Generate Tags
```bash
python -m shutterstock_tagger.tag_generator \
  --image_folder INPUT_DIR \
  --output_folder OUTPUT_DIR
```
Generates titles, keywords, categories.

### Analyze Results
```bash
python -m shutterstock_tagger.result_analyzer \
  --folder_path INPUT_DIR \
  --output_file OUTPUT.csv
```
Creates CSV from AI responses.

### Split Batches
```bash
python -m shutterstock_tagger.batch_splitter \
  --single_output_folder IMAGES_DIR \
  --tag_files TAGS.csv \
  --batch_output_folder OUTPUT_DIR
```
Splits into batches of 100.

## Environment Variables

```bash
# Required
export AWS_REGION=us-east-1
export AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

# Optional
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_PROFILE=default
```

## File Locations

```
work_dir/
├── 1_raw_export/          # Input images
├── 2_binary_output/       # Classification results
├── 3_copied_dest/
│   └── high/              # Best images
├── 5_tag_output/          # Generated tags
├── 6_image_tags.csv       # Master CSV
├── 7_batch_output/        # Upload-ready batches
│   ├── batch_1/
│   └── batch_1_tags.csv
├── state.txt              # Workflow state
└── error_log.txt          # Errors
```

## State Management

```bash
# Check current state
cat work_dir/state.txt

# Reset state (start over)
rm work_dir/state.txt

# Resume workflow
python -m shutterstock_tagger.workflow --base_folder work_dir
```

## Common Tasks

### Process New Batch
```bash
mkdir batch_nov_2025/1_raw_export
cp ~/Photos/new_batch/* batch_nov_2025/1_raw_export/
python -m shutterstock_tagger.workflow --base_folder batch_nov_2025
```

### Reprocess Failed Images
```bash
# Remove failed results
rm work_dir/5_tag_output/failed_image_response.txt

# Rerun tag generation
python -m shutterstock_tagger.tag_generator \
  --image_folder work_dir/3_copied_dest/high \
  --output_folder work_dir/5_tag_output
```

### Check for Errors
```bash
# View errors
cat work_dir/error_log.txt

# Count errors
grep -c "Error" work_dir/error_log.txt

# Find specific errors
grep "rate limit" work_dir/error_log.txt
```

### Customize Prompts
```bash
# Edit tag generation prompt
nano config/prompt.txt

# Edit classification prompt
nano config/prompt_binary.txt

# Test changes
python -m shutterstock_tagger.tag_generator \
  --image_folder test_images/ \
  --output_folder test_output/
```

## Troubleshooting

### AWS Credentials Error
```bash
aws configure
# or
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Module Not Found
```bash
pip install -e .
# or
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Config Files Not Found
```bash
ls config/
# Should show: prompt.txt, system_prompt.txt, etc.
```

### Workflow Stuck
```bash
# Check state
cat work_dir/state.txt

# Check errors
tail -n 20 work_dir/error_log.txt

# Reset if needed
rm work_dir/state.txt
```

## Performance Tips

### Batch Processing
```bash
# Process 500 images at a time
for i in {1..10}; do
  mkdir batch_$i/1_raw_export
  # Copy 500 images
  python -m shutterstock_tagger.workflow --base_folder batch_$i
done
```

### Parallel Processing
```bash
# Terminal 1
python -m shutterstock_tagger.workflow --base_folder batch1 &

# Terminal 2
python -m shutterstock_tagger.workflow --base_folder batch2 &
```

### Skip Steps
```bash
# Manually set state to skip steps
echo "4" > work_dir/state.txt  # Skip to step 5
python -m shutterstock_tagger.workflow --base_folder work_dir
```

## Cost Estimation

```bash
# Calculate costs
images=1000
cost_per_image=0.0008
total_cost=$(echo "$images * $cost_per_image" | bc)
echo "Estimated cost: \$$total_cost"
```

## Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Shutterstock Image Tagger aliases
alias st-workflow='python -m shutterstock_tagger.workflow --base_folder'
alias st-convert='python -m shutterstock_tagger.convert_images'
alias st-clean='python -m shutterstock_tagger.clean_files'
alias st-classify='python -m shutterstock_tagger.binary_classifier'
alias st-tag='python -m shutterstock_tagger.tag_generator'
alias st-analyze='python -m shutterstock_tagger.result_analyzer'
alias st-batch='python -m shutterstock_tagger.batch_splitter'

# Usage:
# st-workflow work_dir
# st-convert work_dir/1_raw_export
```

## Git Commands

```bash
# Check status
git status

# Stage all changes
git add .

# Commit
git commit -m "Processed batch of images"

# Push
git push origin main

# Create branch
git checkout -b feature/custom-prompts

# View changes
git diff
```

## Keyboard Shortcuts

When prompted for confirmation:
- `yes` or `y` - Confirm
- `no` or `n` - Cancel
- `Ctrl+C` - Abort

## File Patterns

```bash
# Find all JPEGs
find work_dir -name "*.jpeg"

# Count images
ls work_dir/1_raw_export/*.jpeg | wc -l

# Find large files
find work_dir -name "*.jpeg" -size +15M

# Find small images
find work_dir -name "*.jpeg" -exec identify -format '%w %h %i\n' {} \; | awk '$1*$2 < 4000000'
```

## CSV Operations

```bash
# View CSV
cat work_dir/6_image_tags.csv | column -t -s,

# Count rows
wc -l work_dir/6_image_tags.csv

# Extract specific column
cut -d',' -f2 work_dir/6_image_tags.csv

# Search CSV
grep "Nature" work_dir/6_image_tags.csv
```

## Backup Commands

```bash
# Backup work directory
tar -czf work_dir_backup_$(date +%Y%m%d).tar.gz work_dir/

# Backup config
cp -r config config_backup_$(date +%Y%m%d)

# Restore backup
tar -xzf work_dir_backup_20251102.tar.gz
```

## Monitoring

```bash
# Watch progress
watch -n 5 'ls work_dir/5_tag_output/*.txt | wc -l'

# Monitor errors
tail -f work_dir/error_log.txt

# Check disk space
du -sh work_dir/

# Monitor AWS costs
aws ce get-cost-and-usage --time-period Start=2025-11-01,End=2025-11-02 --granularity DAILY --metrics BlendedCost
```

## Quick Checks

```bash
# Verify installation
python -c "import shutterstock_tagger; print(shutterstock_tagger.__version__)"

# Check AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Count processed images
ls work_dir/7_batch_output/batch_*/batch_*.csv | wc -l
```

## Resources

- 📖 [Full Documentation](../README.md)
- 🔄 [Workflow Guide](WORKFLOW_GUIDE.md)
- 🚀 [Migration Guide](MIGRATION_GUIDE.md)
- 💡 [Examples](../examples/README.md)
- 🤝 [Contributing](../CONTRIBUTING.md)

## Support

- 🐛 [Report Bug](https://github.com/yourusername/shutterstock-image-tagger/issues)
- 💬 [Ask Question](https://github.com/yourusername/shutterstock-image-tagger/discussions)
- ⭐ [Star Project](https://github.com/yourusername/shutterstock-image-tagger)

---

**Tip**: Bookmark this page for quick reference!

