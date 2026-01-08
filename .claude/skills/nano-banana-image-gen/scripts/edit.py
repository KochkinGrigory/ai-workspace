#!/usr/bin/env python3
"""
Nano Banana Image Editor
Edit/modify existing images using configured model from config.py
Supports: image-to-image, multi-turn editing, reference images
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


def edit_image(
    source_image_path,
    instruction,
    reference_images=None,
    output_dir=None,
    image_size="2K",
    aspect_ratio=None
):
    """
    Edit an existing image using text instructions

    Args:
        source_image_path (str): Path to source image to edit
        instruction (str): Text instruction describing desired changes
        reference_images (list): Optional list of reference image paths (up to 14)
        output_dir (str): Directory to save edited image (default: telegram tmp)
        image_size (str): Image quality/size - "1K", "2K" (default), or "4K"
        aspect_ratio (str): Optional aspect ratio (e.g., "16:9", "1:1", "4:3")

    Returns:
        str: Path to edited image file
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
        if http_proxy:
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["HTTPS_PROXY"] = https_proxy

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Prepare content parts: source image + instruction
    parts = []

    # Add source image
    try:
        source_image_part = load_image_as_part(source_image_path)
        parts.append(source_image_part)
        print(f"[INFO] Loaded source image: {source_image_path}", file=sys.stderr)
    except Exception as e:
        raise ValueError(f"Failed to load source image: {e}")

    # Add reference images if provided
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

    # Add text instruction
    parts.append(types.Part.from_text(text=instruction))

    # Create content
    contents = [
        types.Content(
            role="user",
            parts=parts,
        ),
    ]

    # Configure generation
    image_config_params = {"image_size": image_size}
    if aspect_ratio:
        image_config_params["aspect_ratio"] = aspect_ratio

    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
        image_config=types.ImageConfig(**image_config_params),
    )

    # Set output directory
    if output_dir is None:
        output_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"

    os.makedirs(output_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"nano_banana_edited_{timestamp}"

    # Generate edited image (model from config.py)
    model = MODEL_ID
    file_index = 0
    generated_files = []

    print(f"[INFO] Generating edited image...", file=sys.stderr)

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
            print(f"[INFO] Saved edited image: {file_path}", file=sys.stderr)
        else:
            # Text response (if any)
            if hasattr(chunk, 'text'):
                print(f"[INFO] {chunk.text}", file=sys.stderr)

    if not generated_files:
        raise Exception("No images were generated")

    # Return path to first generated image
    return generated_files[0]


def multi_turn_edit(
    initial_image_path,
    instructions_list,
    output_dir=None,
    image_size="2K",
    aspect_ratio=None,
    save_intermediate=False
):
    """
    Perform multiple sequential edits on an image (multi-turn editing)

    Args:
        initial_image_path (str): Path to initial image
        instructions_list (list): List of text instructions to apply sequentially
        output_dir (str): Directory to save images
        image_size (str): Image quality/size
        aspect_ratio (str): Optional aspect ratio
        save_intermediate (bool): Save intermediate results (default: False)

    Returns:
        list: Paths to all generated images (or just final if save_intermediate=False)
    """
    if not instructions_list:
        raise ValueError("No instructions provided")

    current_image = initial_image_path
    all_results = []

    print(f"[INFO] Starting multi-turn editing with {len(instructions_list)} steps", file=sys.stderr)

    for i, instruction in enumerate(instructions_list, 1):
        print(f"[INFO] Step {i}/{len(instructions_list)}: {instruction[:50]}...", file=sys.stderr)

        result_path = edit_image(
            source_image_path=current_image,
            instruction=instruction,
            output_dir=output_dir,
            image_size=image_size,
            aspect_ratio=aspect_ratio
        )

        all_results.append(result_path)
        current_image = result_path  # Use result as input for next iteration

        # Clean up intermediate files if not saving them
        if not save_intermediate and i < len(instructions_list):
            # Don't delete the original input image
            if current_image != initial_image_path:
                pass  # We'll keep for now, user can clean up manually

    print(f"[INFO] Multi-turn editing complete", file=sys.stderr)

    if save_intermediate:
        return all_results
    else:
        return [all_results[-1]]  # Return only final result


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Nano Banana (Gemini 3 Pro Image Preview)"
    )

    # Subcommands for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Editing mode')

    # Single edit mode
    edit_parser = subparsers.add_parser('edit', help='Single image edit')
    edit_parser.add_argument(
        "source_image",
        type=str,
        help="Path to source image to edit"
    )
    edit_parser.add_argument(
        "instruction",
        type=str,
        help="Text instruction describing desired changes"
    )
    edit_parser.add_argument(
        "--reference-images",
        type=str,
        nargs='+',
        help="Paths to reference images (up to 14)"
    )
    edit_parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save edited image"
    )
    edit_parser.add_argument(
        "--image-size",
        type=str,
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Image quality/size"
    )
    edit_parser.add_argument(
        "--aspect-ratio",
        type=str,
        help="Aspect ratio (e.g., 16:9, 1:1, 4:3)"
    )

    # Multi-turn mode
    multi_parser = subparsers.add_parser('multi-turn', help='Multiple sequential edits')
    multi_parser.add_argument(
        "source_image",
        type=str,
        help="Path to initial image"
    )
    multi_parser.add_argument(
        "instructions",
        type=str,
        nargs='+',
        help="List of instructions to apply sequentially"
    )
    multi_parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save images"
    )
    multi_parser.add_argument(
        "--image-size",
        type=str,
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Image quality/size"
    )
    multi_parser.add_argument(
        "--aspect-ratio",
        type=str,
        help="Aspect ratio"
    )
    multi_parser.add_argument(
        "--save-intermediate",
        action='store_true',
        help="Save intermediate results"
    )

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    try:
        if args.mode == 'edit':
            # Single edit
            output_path = edit_image(
                source_image_path=args.source_image,
                instruction=args.instruction,
                reference_images=args.reference_images,
                output_dir=args.output_dir,
                image_size=args.image_size,
                aspect_ratio=args.aspect_ratio
            )
            print(output_path)

        elif args.mode == 'multi-turn':
            # Multi-turn editing
            results = multi_turn_edit(
                initial_image_path=args.source_image,
                instructions_list=args.instructions,
                output_dir=args.output_dir,
                image_size=args.image_size,
                aspect_ratio=args.aspect_ratio,
                save_intermediate=args.save_intermediate
            )

            # Print all results (or just final)
            for path in results:
                print(path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
