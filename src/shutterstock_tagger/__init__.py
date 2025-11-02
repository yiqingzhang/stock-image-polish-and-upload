"""
Shutterstock Image Tagger

An automated workflow tool for preparing and uploading images to stock photography platforms.
"""

__version__ = "1.0.0"
__author__ = "Shutterstock Image Tagger Contributors"
__license__ = "MIT"

from .bedrock_client import (
    call_bedrock_api,
    encode_image,
    read_prompt,
    get_aws_region,
    get_bedrock_model_id,
)

__all__ = [
    "call_bedrock_api",
    "encode_image",
    "read_prompt",
    "get_aws_region",
    "get_bedrock_model_id",
]

