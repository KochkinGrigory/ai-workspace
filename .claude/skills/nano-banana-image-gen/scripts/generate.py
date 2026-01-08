#!/usr/bin/env python3
"""
Nano Banana Image Generator
Generates images using configured model from config.py
"""

import base64
import mimetypes
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types

# Import model config
from config import MODEL_ID


def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path("/opt/ai-workspace/.env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    # Set env variable only if not already set
                    if key not in os.environ:
                        os.environ[key] = value


# Load .env file at module import time
load_env_file()


def save_binary_file(file_name, data):
    """Save binary data to file"""
    with open(file_name, "wb") as f:
        f.write(data)
    return file_name


def load_image_as_part(image_path):
    """Load image file and convert to API Part object"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image/'):
        raise ValueError(f"Invalid image file: {image_path}")

    # Read image data
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Create Part with inline_data
    return types.Part(
        inline_data=types.Blob(
            mime_type=mime_type,
            data=image_data
        )
    )


def load_style_preset(preset_name):
    """Load style preset from file"""
    preset_path = Path(__file__).parent.parent / "style-presets"

    # Search in all category folders
    for category_dir in preset_path.glob("*/"):
        preset_file = category_dir / f"{preset_name}.md"
        if preset_file.exists():
            with open(preset_file, 'r') as f:
                content = f.read()
                # Extract template from markdown
                # Format: ## Template\n[template text]
                if "## Template" in content:
                    template = content.split("## Template")[1].split("##")[0].strip()
                    return template
    return None


def enhance_prompt(prompt, style_preset=None):
    """Enhance prompt with style preset if provided"""
    if style_preset:
        template = load_style_preset(style_preset)
        if template:
            # Replace {prompt} placeholder in template
            return template.replace("{prompt}", prompt)
    return prompt


def generate_image(prompt, output_dir=None, style_preset=None, image_size="2K", reference_images=None):
    """
    Generate image using Gemini 3 Pro Image Preview

    Args:
        prompt (str): Text description of image to generate
        output_dir (str): Directory to save image (default: telegram tmp)
        style_preset (str): Name of style preset to apply
        image_size (str): Image quality/size - "2K" (default) or "4K"
        reference_images (list): Optional list of reference image paths (up to 14)

    Returns:
        str: Path to generated image file
    """
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    # Configure proxy if set (to bypass VPS blocking)
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")

    if http_proxy or https_proxy:
        print(f"[INFO] Using proxy for requests", file=sys.stderr)
        # Set proxy environment variables for the Google client
        if http_proxy:
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["HTTPS_PROXY"] = https_proxy

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Enhance prompt if style preset provided
    enhanced_prompt = enhance_prompt(prompt, style_preset)

    # Prepare content parts
    parts = []

    # Add reference images if provided (before the prompt)
    if reference_images:
        if len(reference_images) > 14:
            print("[WARNING] Maximum 14 reference images supported, using first 14", file=sys.stderr)
            reference_images = reference_images[:14]

        for ref_path in reference_images:
            try:
                ref_part = load_image_as_part(ref_path)
                parts.append(ref_part)
                print(f"[INFO] Loaded reference image: {ref_path}", file=sys.stderr)
            except Exception as e:
                print(f"[WARNING] Skipping reference image {ref_path}: {e}", file=sys.stderr)

    # Add text prompt
    parts.append(types.Part.from_text(text=enhanced_prompt))

    # Model and content configuration (from config.py)
    model = MODEL_ID
    contents = [
        types.Content(
            role="user",
            parts=parts,
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
        image_config=types.ImageConfig(
            image_size=image_size,
        ),
    )

    # Set output directory
    if output_dir is None:
        output_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"

    os.makedirs(output_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"nano_banana_{timestamp}"

    # Generate image
    file_index = 0
    generated_files = []

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        # Check for inline data (image)
        if (chunk.candidates[0].content.parts[0].inline_data and
            chunk.candidates[0].content.parts[0].inline_data.data):

            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)

            file_name = f"{base_filename}_{file_index}{file_extension}"
            file_path = os.path.join(output_dir, file_name)

            save_binary_file(file_path, data_buffer)
            generated_files.append(file_path)
            file_index += 1
        else:
            # Text response (if any)
            if hasattr(chunk, 'text'):
                print(f"[INFO] {chunk.text}", file=sys.stderr)

    if not generated_files:
        raise Exception("No images were generated")

    # Return path to first generated image
    return generated_files[0]


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana (Gemini 3 Pro Image Preview)"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save generated image (default: telegram tmp)"
    )
    parser.add_argument(
        "--style-preset",
        type=str,
        default=None,
        help="Name of style preset to apply (e.g., 'example-portrait')"
    )
    parser.add_argument(
        "--image-size",
        type=str,
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Image quality/size: 1K, 2K (default), or 4K"
    )
    parser.add_argument(
        "--reference-images",
        type=str,
        nargs='+',
        default=None,
        help="Paths to reference images (up to 14) for style/character consistency"
    )

    args = parser.parse_args()

    try:
        # Generate image
        output_path = generate_image(
            prompt=args.prompt,
            output_dir=args.output_dir,
            style_preset=args.style_preset,
            image_size=args.image_size,
            reference_images=args.reference_images
        )

        # Print path to stdout (for bash scripts to capture)
        print(output_path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
