# 📸 Shutterstock Image Tagger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent, automated workflow tool for preparing and uploading images to stock photography platforms like Shutterstock. This tool leverages AWS Bedrock AI to analyze images, generate metadata, and organize files for efficient batch uploading.

## ✨ Features

- 🔄 **Automated Image Processing**: Convert HEIC/HEIF to JPEG with sRGB color profiles
- 🧹 **Smart Filtering**: Remove images that don't meet stock photography requirements
- 🤖 **AI-Powered Analysis**: Use AWS Bedrock to evaluate image suitability
- 🏷️ **Intelligent Tagging**: Generate titles, keywords, and categories automatically
- 📦 **Batch Organization**: Split images into upload-ready batches of 100
- 💾 **State Management**: Resume interrupted workflows from where you left off
- 🔒 **Privacy-First**: No hardcoded credentials or personal information

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Workflow Steps](#-workflow-steps)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/shutterstock-image-tagger.git
cd shutterstock-image-tagger

# Install required packages
pip install -r requirements.txt
```

### AWS Setup

1. **Configure AWS CLI**:
   ```bash
   aws configure
   ```

2. **Enable AWS Bedrock**:
   - Ensure you have access to AWS Bedrock in your region
   - Request access to the Amazon Nova Lite model (or your preferred model)

3. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS configuration
   ```

## ⚡ Quick Start

1. **Prepare Your Images**:
   ```bash
   mkdir -p work_dir/1_raw_export
   # Copy your images to work_dir/1_raw_export/
   ```

2. **Run the Workflow**:
   ```bash
   python -m shutterstock_tagger.workflow --base_folder work_dir
   ```

3. **Upload to Shutterstock**:
   - Navigate to `work_dir/7_batch_output/`
   - Upload each batch folder with its corresponding CSV file

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

```bash
# AWS Region
AWS_REGION=us-east-1

# AWS Bedrock Model ID
AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

### Customizing Prompts

Edit the prompt files in the `config/` directory to customize AI behavior:

- `system_prompt.txt` - System instructions for tag generation
- `prompt.txt` - User prompt for tag generation
- `system_prompt_binary.txt` - System instructions for image classification
- `prompt_binary.txt` - User prompt for image classification

## 🔄 Workflow Steps

The automated workflow consists of 8 steps:

| Step | Module | Description |
|------|--------|-------------|
| 0 | `convert_images` | Convert HEIC/HEIF images to JPEG format |
| 1 | `clean_files` | Remove images < 4MP or > 15MB |
| 2 | `binary_classifier` | AI evaluation of image suitability |
| 3 | `file_organizer` | Sort images by classification results |
| 4 | `folder_cleanup` | Remove temporary folders |
| 5 | `tag_generator` | Generate titles, keywords, and categories |
| 6 | `result_analyzer` | Create CSV files with metadata |
| 7 | `batch_splitter` | Split into batches of 100 images |

### State Management

The workflow maintains state in `state.txt`, allowing you to:
- Resume from interruptions
- Skip completed steps
- Track progress across sessions

## 📖 Usage Examples

### Run Individual Steps

```bash
# Convert images only
python -m shutterstock_tagger.convert_images work_dir/1_raw_export

# Clean files only
python -m shutterstock_tagger.clean_files work_dir/1_raw_export

# Generate tags for specific folder
python -m shutterstock_tagger.tag_generator \
  --image_folder work_dir/3_copied_dest/high \
  --output_folder work_dir/5_tag_output
```

### Custom Batch Size

To modify the batch size, edit `src/shutterstock_tagger/batch_splitter.py`:

```python
batch_size = 50  # Change from default 100
```

## 📁 Project Structure

```
shutterstock-image-tagger/
├── src/
│   └── shutterstock_tagger/
│       ├── __init__.py
│       ├── workflow.py              # Main orchestrator
│       ├── bedrock_client.py        # AWS Bedrock API client
│       ├── convert_images.py        # Image format conversion
│       ├── clean_files.py           # File filtering
│       ├── binary_classifier.py     # AI suitability check
│       ├── file_organizer.py        # File organization
│       ├── folder_cleanup.py        # Cleanup utilities
│       ├── tag_generator.py         # AI tag generation
│       ├── result_analyzer.py       # CSV creation
│       └── batch_splitter.py        # Batch organization
├── config/
│   ├── prompt.txt                   # Tag generation prompt
│   ├── prompt_binary.txt            # Classification prompt
│   ├── system_prompt.txt            # Tag generation system prompt
│   └── system_prompt_binary.txt     # Classification system prompt
├── examples/                        # Example usage and data
├── docs/                           # Additional documentation
├── .github/
│   └── workflows/                  # CI/CD workflows
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── CONTRIBUTING.md
└── requirements.txt
```

## 🎯 Output Structure

After processing, your work directory will contain:

```
work_dir/
├── 1_raw_export/              # Original images (deleted after step 4)
├── 2_binary_output/           # Classification results
├── 3_copied_dest/
│   ├── high/                  # High-quality suitable images
│   ├── medium/                # Medium-quality images
│   └── low/                   # Low-quality images
├── 5_tag_output/              # AI-generated tags
├── 6_image_tags.csv           # Master CSV file
├── 7_batch_output/
│   ├── batch_1/               # 100 images
│   ├── batch_1_tags.csv       # Metadata for batch 1
│   ├── batch_2/
│   ├── batch_2_tags.csv
│   └── ...
├── state.txt                  # Workflow state
└── error_log.txt              # Error logs
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development setup
- Submitting pull requests
- Reporting bugs
- Suggesting enhancements

## 📝 Requirements

See `requirements.txt` for full dependencies:

- `boto3` - AWS SDK for Python
- `pandas` - Data manipulation and CSV handling
- `Pillow` - Image processing
- `pillow-heif` - HEIC/HEIF format support
- `tqdm` - Progress bars

## 🔒 Security & Privacy

- **No Hardcoded Credentials**: All AWS credentials are managed via environment variables or AWS CLI
- **Local Processing**: Images are processed locally; only base64-encoded data is sent to AWS Bedrock
- **Gitignore Protection**: Working directories and sensitive files are excluded from version control
- **Environment Variables**: Use `.env` file (never committed) for configuration

## 🐛 Troubleshooting

### Common Issues

**AWS Credentials Error**:
```bash
# Ensure AWS CLI is configured
aws configure
# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Bedrock Access Denied**:
- Verify you have access to AWS Bedrock in your region
- Check that your IAM role has `bedrock:InvokeModel` permissions

**Image Size Errors**:
- Images must be between 4MP and 15MB
- Use step 1 (clean_files) to filter automatically

## 📊 Roadmap

- [ ] Support for additional AI models (OpenAI, Anthropic)
- [ ] Web UI for easier workflow management
- [ ] Bulk editing of generated tags
- [ ] Integration with other stock platforms (Adobe Stock, Getty Images)
- [ ] Docker containerization
- [ ] Automated testing suite

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS Bedrock team for the AI models
- Shutterstock for their comprehensive tagging guidelines
- Open source community for the excellent Python libraries

## 📧 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/shutterstock-image-tagger/issues)
- 💬 [Discussions](https://github.com/yourusername/shutterstock-image-tagger/discussions)

---

**Made with ❤️ for photographers and content creators**
