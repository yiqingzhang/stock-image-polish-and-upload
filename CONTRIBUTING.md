# Contributing to Shutterstock Image Tagger

First off, thank you for considering contributing to Shutterstock Image Tagger! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- AWS Account (for testing Bedrock integration)
- Familiarity with stock photography workflows is helpful but not required

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/shutterstock-image-tagger.git
   cd shutterstock-image-tagger
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/shutterstock-image-tagger.git
   ```

4. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

6. **Configure AWS credentials** (for testing):
   ```bash
   cp .env.example .env
   # Edit .env with your test AWS configuration
   ```

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs. actual behavior
- **Environment details** (OS, Python version, AWS region)
- **Error messages** or logs
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why would this be useful?
- **Proposed solution** or implementation ideas
- **Alternatives considered**

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Simple issues perfect for newcomers
- `help wanted` - Issues where we need community help
- `documentation` - Improvements to docs

### Pull Requests

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** following our commit guidelines

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## 💻 Development Setup

### Project Structure

```
src/shutterstock_tagger/
├── __init__.py              # Package initialization
├── workflow.py              # Main workflow orchestrator
├── bedrock_client.py        # AWS Bedrock integration
├── convert_images.py        # Image conversion
├── clean_files.py           # File filtering
├── binary_classifier.py     # AI classification
├── file_organizer.py        # File organization
├── folder_cleanup.py        # Cleanup utilities
├── tag_generator.py         # Tag generation
├── result_analyzer.py       # Result analysis
└── batch_splitter.py        # Batch splitting
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_bedrock_client.py

# Run with coverage
python -m pytest --cov=shutterstock_tagger
```

### Running Individual Modules

```bash
# Test image conversion
python -m shutterstock_tagger.convert_images test_images/

# Test tag generation
python -m shutterstock_tagger.tag_generator \
  --image_folder test_images/ \
  --output_folder test_output/
```

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Use double quotes for strings
- **Imports**: Group and sort imports (stdlib, third-party, local)

### Code Formatting

We use `black` for code formatting:

```bash
# Format all files
black src/

# Check formatting without changes
black --check src/
```

### Documentation

- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Comments**: Explain "why", not "what"
- **Type hints**: Use type hints where appropriate

Example:

```python
def process_image(image_path: str, output_dir: str) -> bool:
    """
    Process a single image and save results.
    
    Args:
        image_path (str): Path to the input image
        output_dir (str): Directory to save processed image
        
    Returns:
        bool: True if processing successful, False otherwise
        
    Raises:
        ValueError: If image_path doesn't exist
        IOError: If unable to write to output_dir
    """
    pass
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Clean up resources in `finally` blocks

### Security Best Practices

- **Never commit credentials** or API keys
- **Use environment variables** for sensitive configuration
- **Validate user input** to prevent injection attacks
- **Handle file paths safely** to prevent directory traversal

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(tag-generator): add support for custom categories

Add ability to specify custom categories in addition to
Shutterstock's default categories.

Closes #123
```

```
fix(bedrock-client): handle rate limiting errors

Add exponential backoff when AWS Bedrock rate limits are hit.
Improves reliability for large batch processing.

Fixes #456
```

## 🔄 Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests** for new features
3. **Update CHANGELOG.md** with your changes
4. **Ensure all tests pass** and code is formatted
5. **Request review** from maintainers
6. **Address feedback** promptly and professionally

### PR Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main branch
- [ ] PR description explains what and why

### Review Process

- Maintainers will review your PR within 1-2 weeks
- Address any requested changes
- Once approved, a maintainer will merge your PR
- Your contribution will be credited in the release notes

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority

- **Testing**: Increase test coverage
- **Documentation**: Improve guides and examples
- **Error Handling**: Better error messages and recovery
- **Performance**: Optimize image processing

### Medium Priority

- **UI/UX**: Web interface or GUI
- **Integration**: Support for other stock platforms
- **Features**: Bulk tag editing, preview mode
- **CI/CD**: Automated testing and deployment

### Nice to Have

- **Internationalization**: Support for multiple languages
- **Docker**: Containerization for easy deployment
- **Monitoring**: Better logging and metrics
- **Examples**: More example workflows and use cases

## 💬 Communication

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Shutterstock Image Tagger! 🎉

