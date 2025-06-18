import os
import json
import base64
import boto3
from pathlib import Path


def read_prompt(prompt_file):
    """Read system prompt from a file."""
    with open(prompt_file, "r") as file:
        return file.read().strip()


def encode_image(image_path):
    """Read and encode image to base64."""

    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode("utf-8")

        return base64_string


def call_bedrock_api(image_base64, system_prompt, prompt, region):
    """Call AWS Bedrock API with image and prompt."""
    client = boto3.client("bedrock-runtime", region_name=region)

    system_list = [{"text": system_prompt}]
    # Define a "user" message including both the image and a text prompt.
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

    # Configure the inference parameters.
    inf_params = {"maxTokens": 300, "topP": 0.1, "topK": 50, "temperature": 0.3}
    # inf_params = {"maxTokens": 300, "topP": 0.9, "temperature": 0.3}

    native_request = {
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params,
    }
    # Invoke the model and extract the response body.
    response = client.invoke_model(
        modelId="arn:aws:bedrock:ap-southeast-2:163666916622:inference-profile/apac.amazon.nova-lite-v1:0",
        body=json.dumps(native_request),
    )
    model_response = json.loads(response["body"].read())
    # Pretty print the response JSON.
    # print("[Full Response]")
    # print(json.dumps(model_response, indent=2))
    # Print the text content for easy readability.
    content_text = model_response["output"]["message"]["content"][0]["text"]
    # print("\n[Response Content Text]")
    # print(content_text)

    return content_text


def process_images(image_folder, output_folder, system_prompt, prompt, region):
    """Process all images in a folder with AWS Bedrock."""
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # get error_log file
    error_log_file = os.path.join(output_folder, "error_log.txt")

    # Process each image in the folder
    image_list = sorted(os.listdir(image_folder))
    total_size = len(image_list)

    for index, image_file in enumerate(image_list):
        # show progress in percentage
        if index % 10 == 0:  # Print progress every 10 images
            # print progress in percentage approximately
            progress_percentage = (index + 1) / total_size * 100
            print(
                f"Processing {index + 1}/{total_size} images ({progress_percentage:.2f}%)"
            )

        # Check if file is an image (basic check, can be enhanced)
        if any(
            image_file.lower().endswith(ext)
            for ext in [".jpg", ".jpeg"]
        ):
            image_path = os.path.join(image_folder, image_file)
            print(f"Processing {image_path}...")

            # Encode image
            image_base64 = encode_image(image_path)

            # Call Bedrock API
            try:
                response = call_bedrock_api(image_base64, system_prompt, prompt, region)
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
                with open(error_log_file, "a") as error_log:
                    error_log.write(f"Error processing {image_file}: {e}\n")
                continue

            # Save response as JSON
            output_file = os.path.join(
                output_folder, f"{Path(image_file).stem}_response.txt"
            )
            with open(output_file, "w") as f:
                json.dump(response, f, indent=2)

            print(f"Response saved to {output_file}")

            # break


if __name__ == "__main__":
    import argparse

    system_prompt_file = "system_prompt.txt"  # Default system prompt file
    prompt_file = "prompt.txt"  # Default prompt file
    region = "ap-southeast-2"  # Default AWS region

    parser = argparse.ArgumentParser(description="Process images with AWS Bedrock")
    parser.add_argument(
        "--image_folder", required=True, help="Folder containing images"
    )
    parser.add_argument(
        "--output_folder", required=True, help="Folder to save responses"
    )

    args = parser.parse_args()

    system_prompt = read_prompt(system_prompt_file)
    prompt = read_prompt(prompt_file)

    process_images(args.image_folder, args.output_folder, system_prompt, prompt, region)
