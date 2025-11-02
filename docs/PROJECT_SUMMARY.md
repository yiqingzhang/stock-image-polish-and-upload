# Project Summary

## Overview

**Shutterstock Image Tagger** is a professional, open-source tool for automating the preparation and tagging of images for stock photography platforms. This document provides a comprehensive overview of the project structure, features, and improvements made for open-source release.

## Project Status

- **Version**: 1.0.0
- **Status**: Production Ready
- **License**: MIT
- **Python**: 3.8+
- **Last Updated**: November 2, 2025

## Key Features

### 🤖 AI-Powered Automation
- AWS Bedrock integration for intelligent image analysis
- Automated suitability classification
- AI-generated titles, keywords, and categories
- Optimized for Shutterstock's requirements

### 🔄 Complete Workflow
- Image format conversion (HEIC/HEIF → JPEG)
- Quality filtering (resolution, file size)
- Binary classification (suitable/not suitable)
- File organization by quality level
- Batch splitting (100 images per batch)
- CSV generation for bulk upload

### 🔒 Security & Privacy
- No hardcoded credentials or personal information
- Environment variable configuration
- AWS credential management via CLI or IAM roles
- Comprehensive .gitignore for sensitive data
- Privacy-first design

### 📊 State Management
- Resumable workflows
- Progress tracking
- Error logging
- Step-by-step execution

## Project Structure

```
shutterstock-image-tagger/
├── src/
│   └── shutterstock_tagger/          # Main package
│       ├── __init__.py                # Package initialization
│       ├── workflow.py                # Workflow orchestrator
│       ├── bedrock_client.py          # AWS Bedrock API client
│       ├── convert_images.py          # Image conversion
│       ├── clean_files.py             # File filtering
│       ├── binary_classifier.py       # AI classification
│       ├── file_organizer.py          # File organization
│       ├── folder_cleanup.py          # Cleanup utilities
│       ├── tag_generator.py           # Tag generation
│       ├── result_analyzer.py         # Result analysis
│       └── batch_splitter.py          # Batch splitting
│
├── config/                            # Configuration files
│   ├── prompt.txt                     # Tag generation prompt
│   ├── prompt_binary.txt              # Classification prompt
│   ├── system_prompt.txt              # System prompt for tags
│   └── system_prompt_binary.txt       # System prompt for classification
│
├── docs/                              # Documentation
│   ├── WORKFLOW_GUIDE.md              # Detailed workflow guide
│   └── PROJECT_SUMMARY.md             # This file
│
├── examples/                          # Example usage
│   └── README.md                      # Example scenarios
│
├── .github/
│   └── workflows/
│       └── lint.yml                   # CI/CD for linting
│
├── .gitignore                         # Comprehensive gitignore
├── .env.example                       # Environment variable template
├── LICENSE                            # MIT License
├── README.md                          # Main documentation
├── CONTRIBUTING.md                    # Contribution guidelines
├── CHANGELOG.md                       # Version history
├── setup.py                           # Package setup
└── requirements.txt                   # Python dependencies
```

## Improvements for Open Source

### 1. Security Enhancements
- ✅ Removed hardcoded AWS account ID from code
- ✅ Implemented environment variable configuration
- ✅ Added .env.example template
- ✅ Enhanced .gitignore to prevent credential leaks
- ✅ Privacy-first design (no personal information)

### 2. Code Organization
- ✅ Restructured from numbered scripts to modular package
- ✅ Proper Python package structure (src/ layout)
- ✅ Separated concerns into individual modules
- ✅ Added comprehensive docstrings
- ✅ Improved code readability and maintainability

### 3. Documentation
- ✅ Professional README with badges and examples
- ✅ Detailed workflow guide
- ✅ Contributing guidelines
- ✅ Example scenarios and use cases
- ✅ Troubleshooting documentation
- ✅ Changelog for version tracking

### 4. Configuration Management
- ✅ Moved prompts to config/ directory
- ✅ Environment variable support
- ✅ Configurable AWS region and model
- ✅ Flexible configuration system

### 5. Development Infrastructure
- ✅ setup.py for easy installation
- ✅ GitHub Actions for CI/CD
- ✅ Automated linting and formatting checks
- ✅ Security scanning with bandit
- ✅ Professional project structure

### 6. User Experience
- ✅ Clear installation instructions
- ✅ Quick start guide
- ✅ Example workflows
- ✅ Error handling and logging
- ✅ Progress indicators

## Technical Architecture

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `workflow.py` | Orchestrates entire pipeline | `process_images()`, state management |
| `bedrock_client.py` | AWS Bedrock API integration | `call_bedrock_api()`, `encode_image()` |
| `convert_images.py` | Image format conversion | `convert_to_jpeg()`, color profile handling |
| `clean_files.py` | Quality filtering | `is_valid_jpeg()`, size validation |
| `binary_classifier.py` | AI suitability check | Classification logic |
| `file_organizer.py` | File organization | `move_files()`, folder creation |
| `folder_cleanup.py` | Cleanup operations | `delete_folder()`, confirmation prompts |
| `tag_generator.py` | Tag generation | AI-powered metadata creation |
| `result_analyzer.py` | CSV creation | `analyze_output_files()`, parsing |
| `batch_splitter.py` | Batch organization | `main()`, batch creation |

### Data Flow

```
Raw Images
    ↓
[Convert] → JPEG with sRGB
    ↓
[Clean] → Filter by size/quality
    ↓
[Classify] → AI suitability check
    ↓
[Organize] → Sort by quality (high/medium/low)
    ↓
[Cleanup] → Remove temporary files
    ↓
[Tag] → Generate metadata
    ↓
[Analyze] → Create CSV
    ↓
[Batch] → Split into groups of 100
    ↓
Upload-Ready Batches
```

### State Management

The workflow uses a state file to track progress:

- **State -1**: Initial state, ready to convert images
- **State 0**: Conversion complete, ready to clean
- **State 1**: Cleaning complete, ready to classify
- **State 2**: Classification complete, ready to organize
- **State 3**: Organization complete, ready to cleanup
- **State 4**: Cleanup complete, ready to generate tags
- **State 5**: Tags generated, ready to analyze
- **State 6**: Analysis complete, ready to batch
- **State 7**: All steps complete

## Dependencies

### Core Dependencies
- **boto3**: AWS SDK for Python (Bedrock API)
- **pandas**: Data manipulation and CSV handling
- **Pillow**: Image processing and manipulation
- **pillow-heif**: HEIC/HEIF format support
- **tqdm**: Progress bars for better UX

### Development Dependencies
- **black**: Code formatting
- **flake8**: Linting
- **pylint**: Code analysis
- **mypy**: Type checking
- **pytest**: Testing framework
- **bandit**: Security scanning

## Configuration

### Environment Variables

```bash
# Required
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

# Optional (if not using AWS CLI)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_PROFILE=default
```

### Customizable Prompts

All AI prompts are configurable via text files in `config/`:

1. **system_prompt.txt**: System instructions for tag generation
2. **prompt.txt**: User prompt for tag generation
3. **system_prompt_binary.txt**: System instructions for classification
4. **prompt_binary.txt**: User prompt for classification

## Usage Patterns

### 1. Complete Automated Workflow
```bash
python -m shutterstock_tagger.workflow --base_folder work_dir
```

### 2. Step-by-Step Execution
```bash
python -m shutterstock_tagger.convert_images work_dir/1_raw_export
python -m shutterstock_tagger.clean_files work_dir/1_raw_export
# ... etc
```

### 3. Individual Module Usage
```bash
python -m shutterstock_tagger.tag_generator \
  --image_folder images/ \
  --output_folder output/
```

## Performance Considerations

### Processing Speed
- **Image conversion**: ~1-2 seconds per image
- **AI classification**: ~2-3 seconds per image (AWS Bedrock)
- **Tag generation**: ~2-3 seconds per image (AWS Bedrock)
- **Total**: ~5-8 seconds per image

### Cost Estimation
- **AWS Bedrock (Nova Lite)**: ~$0.0008 per image
- **1000 images**: ~$0.80
- **10000 images**: ~$8.00

### Optimization Tips
1. Process in batches to manage costs
2. Use faster AWS regions (lower latency)
3. Increase AWS quotas for parallel processing
4. Cache results to avoid reprocessing

## Quality Assurance

### Code Quality
- ✅ Comprehensive docstrings
- ✅ Type hints throughout
- ✅ Consistent formatting (black)
- ✅ Linting (flake8)
- ✅ Security scanning (bandit)

### Testing Strategy
- Manual testing of all modules
- Integration testing of complete workflow
- Error handling verification
- Edge case coverage

### CI/CD
- Automated linting on push/PR
- Multiple Python version testing (3.8-3.11)
- Security scanning
- Code formatting checks

## Future Roadmap

### Short Term (v1.1)
- [ ] Automated testing suite
- [ ] Docker containerization
- [ ] Performance optimizations
- [ ] Better error messages

### Medium Term (v1.2-1.3)
- [ ] Web UI for workflow management
- [ ] Bulk tag editing
- [ ] Preview mode before upload
- [ ] Support for more AI models

### Long Term (v2.0+)
- [ ] Integration with other stock platforms
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Mobile app

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Pull request process
- Areas needing help

## Support

- 📖 [Documentation](../README.md)
- 🐛 [Issue Tracker](https://github.com/yourusername/shutterstock-image-tagger/issues)
- 💬 [Discussions](https://github.com/yourusername/shutterstock-image-tagger/discussions)

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Acknowledgments

- AWS Bedrock team for AI models
- Shutterstock for tagging guidelines
- Open source community for Python libraries
- Contributors and users

---

**Last Updated**: November 2, 2025  
**Maintainers**: Shutterstock Image Tagger Contributors  
**Status**: Production Ready ✅

