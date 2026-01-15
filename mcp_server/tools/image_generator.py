#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Generator Tool - Generate images using Gemini 3 Pro API

This module provides a unified interface for generating images using Google's
Gemini 3 Pro image generation model.
"""

import sys
import os
import json
from datetime import datetime
from typing import Optional

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


def _get_gemini_client():
    """Get Gemini API client with API key from environment."""
    try:
        from google import genai
    except ImportError:
        raise ImportError("google-genai library not installed. Run: pip install google-genai")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    return genai.Client(api_key=api_key)


def generate_image(
    prompt: str,
    output_path: Optional[str] = None,
    aspect_ratio: str = "1:1",
    resolution: str = "2K"
) -> dict:
    """
    Generate an image using Gemini 3 Pro.
    
    Args:
        prompt: The image generation prompt
        output_path: Path to save the image (optional, auto-generated if not provided)
        aspect_ratio: Image aspect ratio - "1:1", "16:9", "9:16", "4:3", "3:4"
        resolution: Image resolution - "2K" or "4K"
    
    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - path: Path to saved image (if successful)
        - error: Error message (if failed)
        - prompt: The prompt used
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return {
            "status": "error",
            "error": "google-genai library not installed. Run: pip install google-genai",
            "prompt": prompt
        }
    
    # Validate aspect ratio
    valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4"]
    if aspect_ratio not in valid_ratios:
        aspect_ratio = "1:1"
    
    # Validate resolution
    if resolution not in ["2K", "4K"]:
        resolution = "2K"
    
    # Generate output path if not provided
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(PROJECT_ROOT, "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"generated_{timestamp}.png")
    else:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    
    try:
        client = _get_gemini_client()
        
        print(f"🎨 Generating image with Gemini 3 Pro...")
        print(f"   Aspect ratio: {aspect_ratio}")
        print(f"   Resolution: {resolution}")
        
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=resolution
                )
            )
        )
        
        # Extract and save the image
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                print(f"✅ Image saved: {output_path}")
                return {
                    "status": "success",
                    "path": output_path,
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "resolution": resolution
                }
        
        return {
            "status": "error",
            "error": "No image data received from API",
            "prompt": prompt
        }
        
    except ValueError as e:
        return {
            "status": "error",
            "error": str(e),
            "prompt": prompt
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Generation failed: {str(e)}",
            "prompt": prompt
        }


def format_result_json(result: dict) -> str:
    """Format the generation result as JSON string."""
    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Simple test
    test_prompt = "A beautiful sunset over the ocean, cinematic lighting, high quality"
    result = generate_image(test_prompt, aspect_ratio="16:9")
    print(format_result_json(result))
