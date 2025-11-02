# Migration Guide: v0.x to v1.0

This guide helps you migrate from the old numbered script structure to the new modular package structure.

## Overview of Changes

### Old Structure (v0.x)
```
shutterstock-image-tagger/
├── 0_convert_images.py
├── 1_clean_files.py
├── 2_bedrock_run_binary.py
├── 3_move_files.py
├── 4_delete_folders.py
├── 5_generate_tags.py
├── 6_result_analysis.py
├── 7_split_upload_batch.py
├── auto_work.py
├── prompt.txt
├── system_prompt.txt
├── prompt_binary.txt
└── system_prompt_binary.txt
```

### New Structure (v1.0)
```
shutterstock-image-tagger/
├── src/shutterstock_tagger/
│   ├── convert_images.py
│   ├── clean_files.py
│   ├── binary_classifier.py
│   ├── file_organizer.py
│   ├── folder_cleanup.py
│   ├── tag_generator.py
│   ├── result_analyzer.py
│   ├── batch_splitter.py
│   └── workflow.py
├── config/
│   ├── prompt.txt
│   ├── system_prompt.txt
│   ├── prompt_binary.txt
│   └── system_prompt_binary.txt
├── .env.example
└── setup.py
```

## Breaking Changes

### 1. Command Structure

**Old Commands:**
```bash
python 0_convert_images.py directory
python 1_clean_files.py directory
python auto_work.py --base_folder work_dir
```

**New Commands:**
```bash
python -m shutterstock_tagger.convert_images directory
python -m shutterstock_tagger.clean_files directory
python -m shutterstock_tagger.workflow --base_folder work_dir
```

### 2. Configuration

**Old:** Hardcoded AWS account ID in scripts
```python
# In 2_bedrock_run_binary.py
modelId="arn:aws:bedrock:ap-southeast-2:163666916622:inference-profile/..."
```

**New:** Environment variables
```bash
# In .env file
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

### 3. Prompt File Locations

**Old:** Root directory
```
prompt.txt
system_prompt.txt
```

**New:** Config directory
```
config/prompt.txt
config/system_prompt.txt
```

## Migration Steps

### Step 1: Backup Your Work

```bash
# Backup your current setup
cp -r shutterstock-image-tagger shutterstock-image-tagger-backup

# Backup any custom prompts
cp prompt.txt prompt.txt.backup
cp system_prompt.txt system_prompt.txt.backup
```

### Step 2: Pull Latest Changes

```bash
cd shutterstock-image-tagger
git pull origin main
```

### Step 3: Install as Package

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

Add your configuration:
```bash
AWS_REGION=your-region
AWS_BEDROCK_MODEL_ID=your-model-id
```

### Step 5: Migrate Custom Prompts

If you customized the prompts:

```bash
# Copy your custom prompts to new location
cp prompt.txt.backup config/prompt.txt
cp system_prompt.txt.backup config/system_prompt.txt
```

### Step 6: Update Your Scripts

If you have scripts that call the old commands:

**Old script:**
```bash
#!/bin/bash
python 0_convert_images.py work_dir/1_raw_export
python 1_clean_files.py work_dir/1_raw_export
python auto_work.py --base_folder work_dir
```

**New script:**
```bash
#!/bin/bash
python -m shutterstock_tagger.convert_images work_dir/1_raw_export
python -m shutterstock_tagger.clean_files work_dir/1_raw_export
python -m shutterstock_tagger.workflow --base_folder work_dir
```

### Step 7: Test the Migration

```bash
# Test with a small batch
mkdir test_migration
mkdir test_migration/1_raw_export
cp sample_images/* test_migration/1_raw_export/

# Run the workflow
python -m shutterstock_tagger.workflow --base_folder test_migration
```

## Command Reference

### Complete Command Mapping

| Old Command | New Command |
|-------------|-------------|
| `python 0_convert_images.py DIR` | `python -m shutterstock_tagger.convert_images DIR` |
| `python 1_clean_files.py DIR` | `python -m shutterstock_tagger.clean_files DIR` |
| `python 2_bedrock_run_binary.py --image_folder A --output_folder B` | `python -m shutterstock_tagger.binary_classifier --image_folder A --output_folder B` |
| `python 3_move_files.py --source_dir A --label_dir B --results_dir C` | `python -m shutterstock_tagger.file_organizer --source_dir A --label_dir B --results_dir C` |
| `python 4_delete_folders.py --base_folder DIR` | `python -m shutterstock_tagger.folder_cleanup --base_folder DIR` |
| `python 5_generate_tags.py --image_folder A --output_folder B` | `python -m shutterstock_tagger.tag_generator --image_folder A --output_folder B` |
| `python 6_result_analysis.py --folder_path A --output_file B` | `python -m shutterstock_tagger.result_analyzer --folder_path A --output_file B` |
| `python 7_split_upload_batch.py --single_output_folder A --tag_files B --batch_output_folder C` | `python -m shutterstock_tagger.batch_splitter --single_output_folder A --tag_files B --batch_output_folder C` |
| `python auto_work.py --base_folder DIR` | `python -m shutterstock_tagger.workflow --base_folder DIR` |

## Configuration Migration

### AWS Credentials

**Old:** Hardcoded in scripts
```python
# In 2_bedrock_run_binary.py (line 58)
modelId="arn:aws:bedrock:ap-southeast-2:163666916622:inference-profile/apac.amazon.nova-lite-v1:0"
```

**New:** Environment variables or AWS CLI

Option 1 - Environment variables:
```bash
# In .env
AWS_REGION=ap-southeast-2
AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

Option 2 - AWS CLI:
```bash
aws configure
```

Option 3 - IAM Roles (recommended for EC2/ECS):
- No configuration needed
- Uses instance role automatically

### Region Configuration

**Old:** Hardcoded `ap-southeast-2`
```python
region = "ap-southeast-2"
```

**New:** Environment variable
```bash
export AWS_REGION=ap-southeast-2
# or in .env file
AWS_REGION=ap-southeast-2
```

## Troubleshooting

### Issue: Module not found

**Error:**
```
ModuleNotFoundError: No module named 'shutterstock_tagger'
```

**Solution:**
```bash
# Install the package
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Issue: AWS credentials not found

**Error:**
```
NoCredentialsError: Unable to locate credentials
```

**Solution:**
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Issue: Config files not found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'prompt.txt'
```

**Solution:**
```bash
# Ensure config files are in the right location
ls config/
# Should show: prompt.txt, system_prompt.txt, etc.

# If missing, copy from root
cp prompt.txt config/
cp system_prompt.txt config/
```

### Issue: Old state file incompatible

**Error:**
```
Workflow behaves unexpectedly
```

**Solution:**
```bash
# Remove old state file
rm work_dir/state.txt

# Start fresh
python -m shutterstock_tagger.workflow --base_folder work_dir
```

## Feature Comparison

| Feature | v0.x | v1.0 |
|---------|------|------|
| Modular structure | ❌ | ✅ |
| Environment variables | ❌ | ✅ |
| Package installation | ❌ | ✅ |
| Comprehensive docs | ❌ | ✅ |
| CI/CD | ❌ | ✅ |
| Security best practices | ❌ | ✅ |
| Type hints | ❌ | ✅ |
| Docstrings | Partial | ✅ |
| Examples | ❌ | ✅ |
| Contributing guide | ❌ | ✅ |

## Benefits of Upgrading

### 1. Security
- No hardcoded credentials
- Environment variable configuration
- Better secret management

### 2. Maintainability
- Modular code structure
- Better organization
- Easier to extend

### 3. Usability
- Proper Python package
- Better documentation
- More examples

### 4. Professional
- MIT License
- Contributing guidelines
- CI/CD integration

### 5. Community-Ready
- Open source best practices
- Clear project structure
- Welcoming to contributors

## Rollback Plan

If you need to rollback to the old version:

```bash
# Restore from backup
cd ..
mv shutterstock-image-tagger shutterstock-image-tagger-v1
mv shutterstock-image-tagger-backup shutterstock-image-tagger
cd shutterstock-image-tagger

# Use old commands
python auto_work.py --base_folder work_dir
```

## Getting Help

If you encounter issues during migration:

1. **Check Documentation**:
   - [README.md](../README.md)
   - [Workflow Guide](WORKFLOW_GUIDE.md)
   - [Examples](../examples/README.md)

2. **Search Issues**:
   - Check existing GitHub issues
   - Look for similar problems

3. **Ask for Help**:
   - Open a new GitHub issue
   - Include error messages
   - Describe what you tried

4. **Community Support**:
   - GitHub Discussions
   - Tag with "migration"

## Post-Migration Checklist

- [ ] Backup completed
- [ ] New version pulled
- [ ] Package installed
- [ ] Environment configured
- [ ] Custom prompts migrated
- [ ] Scripts updated
- [ ] Test run successful
- [ ] Old files cleaned up
- [ ] Documentation reviewed

## Next Steps

After successful migration:

1. **Explore new features**:
   - Try the examples
   - Customize prompts
   - Experiment with different models

2. **Optimize your workflow**:
   - Adjust batch sizes
   - Fine-tune prompts
   - Improve efficiency

3. **Contribute back**:
   - Share your improvements
   - Report bugs
   - Suggest features

---

**Need help?** Open an issue on GitHub or check the documentation.

**Found a bug?** Please report it so we can fix it for everyone.

**Have suggestions?** We'd love to hear your ideas!

