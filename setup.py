"""Setup configuration for Shutterstock Image Tagger."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="shutterstock-image-tagger",
    version="1.0.0",
    author="Shutterstock Image Tagger Contributors",
    description="An automated workflow tool for preparing and uploading images to stock photography platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shutterstock-image-tagger",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "boto3>=1.26.0",
        "pandas>=1.5.0",
        "Pillow>=9.0.0",
        "pillow-heif>=0.10.0",
        "tqdm>=4.64.0",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=5.0.0",
            "pylint>=2.15.0",
            "mypy>=0.990",
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shutterstock-tagger=shutterstock_tagger.workflow:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.txt"],
    },
)

