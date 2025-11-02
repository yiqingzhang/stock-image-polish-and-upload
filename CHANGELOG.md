# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-02

### Added
- Initial release of Shutterstock Image Tagger
- Complete automated workflow for stock photography preparation
- AWS Bedrock integration for AI-powered image analysis
- Image format conversion (HEIC/HEIF to JPEG)
- Intelligent image filtering and quality checks
- Binary classification for image suitability
- AI-generated titles, keywords, and categories
- Batch organization (100 images per batch)
- State management for resumable workflows
- Comprehensive documentation and examples
- MIT License
- Contributing guidelines
- GitHub Actions CI/CD for linting

### Features
- **Image Processing**
  - Convert HEIC/HEIF to JPEG with sRGB color profile
  - Filter images by size (4MP minimum, 15MB maximum)
  - Automatic quality validation

- **AI Analysis**
  - Binary classification for upload suitability
  - Automated tag generation with 15-25 keywords
  - Category assignment from Shutterstock's official list
  - Attractive title generation

- **Organization**
  - Sort images by quality (high/medium/low)
  - Split into upload-ready batches
  - Generate CSV files with metadata
  - State tracking for workflow resumption

- **Security & Privacy**
  - Environment variable configuration
  - No hardcoded credentials
  - Comprehensive .gitignore
  - AWS credential management

### Documentation
- Professional README with badges and examples
- Detailed workflow guide
- Contributing guidelines
- Example scenarios and use cases
- Troubleshooting documentation

### Configuration
- Environment variable support (.env file)
- Customizable AI prompts
- Configurable AWS region and model
- Flexible batch sizes

### Development
- Modular architecture with separate modules
- Comprehensive docstrings
- Type hints throughout codebase
- GitHub Actions for automated linting
- Setup.py for easy installation

## [Unreleased]

### Planned Features
- Web UI for easier workflow management
- Support for additional AI models (OpenAI, Anthropic)
- Bulk tag editing capabilities
- Integration with other stock platforms (Adobe Stock, Getty Images)
- Docker containerization
- Automated testing suite
- Performance optimizations
- Multi-language support

### Known Issues
- None reported yet

---

## Release Notes

### Version 1.0.0

This is the first stable release of Shutterstock Image Tagger. The tool has been completely restructured for open-source release with:

- Clean, modular architecture
- Comprehensive documentation
- Security best practices
- Professional project structure
- CI/CD integration

**Migration from Pre-1.0 versions:**

If you were using the pre-release scripts (0_convert_images.py, 1_clean_files.py, etc.):

1. Install the new package structure:
   ```bash
   pip install -e .
   ```

2. Update your workflow commands:
   ```bash
   # Old: python 0_convert_images.py directory
   # New: python -m shutterstock_tagger.convert_images directory
   
   # Old: python auto_work.py --base_folder work_dir
   # New: python -m shutterstock_tagger.workflow --base_folder work_dir
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS configuration
   ```

4. Update prompt file locations:
   - Old: `prompt.txt`, `system_prompt.txt` in root
   - New: `config/prompt.txt`, `config/system_prompt.txt`

**Breaking Changes:**
- Module names changed from numbered scripts to descriptive names
- Configuration moved to `config/` directory
- Environment variables now required for AWS configuration
- Hardcoded AWS account IDs removed

**Upgrade Benefits:**
- Better security (no hardcoded credentials)
- Easier to use (proper Python package)
- Better documentation
- More maintainable code
- CI/CD integration
- Community-ready

---

For detailed information about each change, see the [commit history](https://github.com/yourusername/shutterstock-image-tagger/commits/main).

