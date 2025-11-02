"""
AWS Bedrock API client module.

Handles communication with AWS Bedrock for image analysis and tagging.
"""

import os
import json
import base64
import boto3
from pathlib import Path


def get_bedrock_model_id():
    """
    Get the AWS Bedrock model ID from environment variable or use default.
    
    Returns:
        str: The model ID or ARN to use for Bedrock API calls
    """
    # Try to get from environment variable first
    model_id = os.environ.get('AWS_BEDROCK_MODEL_ID')
    
    if model_id:
        return model_id
    
    # Default to Nova Lite model (without hardcoded account ID)
    # Users should set their own model ID in environment variables
    region = os.environ.get('AWS_REGION', 'us-east-1')
    return f"amazon.nova-lite-v1:0"


def get_aws_region():
    """
    Get AWS region from environment variable or use default.
    
    Returns:
        str: AWS region name
    """
    return os.environ.get('AWS_REGION', 'us-east-1')


def read_prompt(prompt_file):
    """
    Read prompt text from a file.
    
    Args:
        prompt_file (str): Path to the prompt file
        
    Returns:
        str: Content of the prompt file
    """
    with open(prompt_file, "r") as file:
        return file.read().strip()


def encode_image(image_path):
    """
    Read and encode image to base64.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode("utf-8")
        return base64_string


def call_bedrock_api(image_base64, system_prompt, prompt, region=None, model_id=None):
    """
    Call AWS Bedrock API with image and prompt.
    
    Args:
        image_base64 (str): Base64 encoded image
        system_prompt (str): System prompt for the AI
        prompt (str): User prompt for the AI
        region (str, optional): AWS region. Defaults to environment variable or us-east-1
        model_id (str, optional): Model ID. Defaults to environment variable or default model
        
    Returns:
        str: Response text from the API
    """
    if region is None:
        region = get_aws_region()
    
    if model_id is None:
        model_id = get_bedrock_model_id()
    
    client = boto3.client("bedrock-runtime", region_name=region)

    system_list = [{"text": system_prompt}]
    
    # Define a "user" message including both the image and a text prompt
    message_list = [
        {
            "role": "user",
            "content": [
                {
                    "image": {
                        "format": "jpeg",
                        "source": {"bytes": image_base64},
                    }
                },
                {"text": prompt},
            ],
        }
    ]

    # Configure the inference parameters
    inf_params = {
        "maxTokens": 300,
        "topP": 0.1,
        "topK": 50,
        "temperature": 0.3
    }

    native_request = {
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params,
    }
    
    # Invoke the model and extract the response body
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(native_request),
    )
    model_response = json.loads(response["body"].read())
    
    # Extract the text content
    content_text = model_response["output"]["message"]["content"][0]["text"]
    
    return content_text


def process_images(image_folder, output_folder, system_prompt, prompt, region=None):
    """
    Process all images in a folder with AWS Bedrock.
    
    Args:
        image_folder (str): Folder containing images to process
        output_folder (str): Folder to save API responses
        system_prompt (str): System prompt for the AI
        prompt (str): User prompt for the AI
        region (str, optional): AWS region
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    error_file = os.path.join(os.path.dirname(output_folder), "error_log.txt")

    # Process each image in the folder
    image_list = sorted(os.listdir(image_folder))
    total_size = len(image_list)
    print(f"Total images to process: {total_size}")

    for index, image_file in enumerate(image_list):
        # Show progress in percentage
        if index % 10 == 0:  # Print progress every 10 images
            progress_percentage = (index + 1) / total_size * 100
            print(f"Processing {index + 1}/{total_size} images ({progress_percentage:.2f}%)")

        # Check if file is an image
        if any(image_file.lower().endswith(ext) for ext in [".jpg", ".jpeg"]):
            image_path = os.path.join(image_folder, image_file)
            print(f"Processing {image_path}...")

            # Encode image
            image_base64 = encode_image(image_path)

            # Call Bedrock API
            try:
                response = call_bedrock_api(image_base64, system_prompt, prompt, region)
            except Exception as e:
                err_msg = f"Error processing {image_file}: {e}"
                print(err_msg)
                with open(error_file, "a") as ef:
                    ef.write(err_msg + "\n")
                continue

            # Determine output filename based on caller
            output_file = os.path.join(output_folder, f"{Path(image_file).stem}_response.txt")
            
            # Save response
            with open(output_file, "w") as f:
                json.dump(response, f, indent=2)

            print(f"Response saved to {output_file}")

