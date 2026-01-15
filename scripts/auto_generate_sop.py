#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Generate SOP - End-to-end automated image generation pipeline

This script implements a complete SOP (Standard Operating Procedure) for
generating AI images from natural language descriptions:

    Input -> Intent Parsing -> Element Selection -> Prompt Composition -> Image Generation

Usage:
    python scripts/auto_generate_sop.py "描述文字"
    python scripts/auto_generate_sop.py "电影级亚洲女性" --output output.png
    python scripts/auto_generate_sop.py "赛博朋克城市" --ratio 16:9 --resolution 4K
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from mcp_server.tools.intent_parser import parse_intent
from mcp_server.tools.image_generator import generate_image, format_result_json
from skill_library.intelligent_generator import IntelligentGenerator


class AutoGenerateSOP:
    """
    End-to-end automated image generation SOP.
    
    Workflow:
    1. Parse user intent from natural language
    2. Select matching elements from the database
    3. Compose the final prompt
    4. Generate the image using Gemini 3 Pro
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the SOP generator.
        
        Args:
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self.generator = IntelligentGenerator()
    
    def log(self, message: str, emoji: str = ""):
        """Print a log message if verbose mode is enabled."""
        if self.verbose:
            prefix = f"{emoji} " if emoji else ""
            print(f"{prefix}{message}")
    
    def parse_intent(self, description: str, domain: str = "auto") -> dict:
        """
        Phase 1: Parse user intent from natural language.
        
        Args:
            description: User's description in natural language
            domain: Domain hint (portrait/art/design/product/video/auto)
        
        Returns:
            Structured intent dictionary
        """
        self.log("Phase 1: Parsing user intent...", "📋")
        intent = parse_intent(description, domain)
        
        if self.verbose:
            print(json.dumps(intent, indent=2, ensure_ascii=False))
            print()
        
        return intent
    
    def adapt_intent(self, intent: dict) -> dict:
        """
        Adapt the parsed intent for IntelligentGenerator.
        
        The intent structure from parse_intent may need flattening for
        select_elements_by_intent.
        """
        adapted = intent.copy()
        
        # Flatten styling
        if 'styling' in intent:
            adapted['clothing'] = intent['styling'].get('clothing', 'modern')
            adapted['hairstyle'] = intent['styling'].get('hairstyle', 'modern')
        
        # Flatten scene/atmosphere
        if 'scene' in intent:
            adapted['era'] = intent['scene'].get('era', 'modern')
        
        # Flatten lighting
        if 'lighting' in intent and isinstance(intent['lighting'], dict):
            adapted['lighting'] = intent['lighting'].get('lighting_type', 'natural')
        
        return adapted
    
    def select_elements(self, intent: dict, user_request: str = "") -> list:
        """
        Phase 2: Select matching elements from the database.
        
        Args:
            intent: Parsed intent dictionary
            user_request: Original user request (for keyword injection)
        
        Returns:
            List of selected elements
        """
        self.log("Phase 2: Selecting elements...", "🔍")
        
        adapted_intent = self.adapt_intent(intent)
        elements = self.generator.select_elements_by_intent(adapted_intent)
        
        # Advanced: Manual keyword injection for specific terms
        extra_keywords = []
        
        if user_request:
            keyword_map = {
                ("侧脸", "侧面"): ["side profile"],
                ("微距",): ["macro", "extreme close up"],
                ("赛博朋克", "cyberpunk"): ["cyberpunk", "neon"],
                ("水墨", "ink"): ["ink wash", "sumi-e"],
            }
            
            for triggers, keywords in keyword_map.items():
                if any(trigger in user_request.lower() for trigger in triggers):
                    self.log(f"  Detected '{triggers[0]}', adding keywords: {keywords}", "🔍")
                    extra_keywords.extend(keywords)
        
        if extra_keywords:
            additional = self.generator.search_style_elements(
                extra_keywords, 
                domain=intent.get('domain', 'portrait')
            )
            for elem in additional:
                self.log(f"  + Added: {elem.get('chinese_name', elem['name'])} ({elem['name']})", "")
                elements.append(elem)
        
        if self.verbose:
            print(f"\n  Selected {len(elements)} elements:")
            for elem in elements:
                name = elem.get('chinese_name', elem.get('name', 'Unknown'))
                category = elem.get('category', elem.get('field_name', 'unknown'))
                print(f"    - {name} [{category}]")
            print()
        
        return elements
    
    def check_and_resolve_conflicts(self, elements: list) -> list:
        """
        Phase 2.5: Check consistency and resolve conflicts.
        
        Args:
            elements: List of selected elements
        
        Returns:
            Cleaned list of elements (conflicts resolved)
        """
        self.log("Phase 2.5: Checking consistency...", "⚙️")
        
        issues = self.generator.check_consistency(elements)
        
        if issues:
            self.log(f"  Found {len(issues)} conflict(s), resolving...", "⚠️")
            fixed_elements, fixes = self.generator.resolve_conflicts(elements, issues)
            for fix in fixes:
                self.log(f"    - {fix}", "")
            return fixed_elements
        else:
            self.log("  No conflicts found", "✅")
            return elements
    
    def compose_prompt(self, elements: list, mode: str = "auto") -> str:
        """
        Phase 3: Compose the final AI image prompt.
        
        Args:
            elements: List of selected elements
            mode: Composition mode (simple/auto/detailed)
        
        Returns:
            Complete prompt string
        """
        self.log("Phase 3: Composing prompt...", "✍️")
        
        prompt = self.generator.compose_prompt(elements, mode=mode)
        
        if self.verbose:
            print(f"\n  Generated prompt ({len(prompt.split())} words):")
            print("  " + "─" * 50)
            # Wrap long prompts for display
            words = prompt.split()
            line = "  "
            for word in words:
                if len(line) + len(word) > 80:
                    print(line)
                    line = "  " + word
                else:
                    line += " " + word if line.strip() else word
            if line.strip():
                print(line)
            print("  " + "─" * 50)
            print()
        
        return prompt
    
    def generate_image(
        self, 
        prompt: str, 
        output_path: Optional[str] = None,
        aspect_ratio: str = "1:1",
        resolution: str = "2K"
    ) -> dict:
        """
        Phase 4: Generate the image using Gemini 3 Pro.
        
        Args:
            prompt: The image generation prompt
            output_path: Path to save the image (optional)
            aspect_ratio: Image aspect ratio
            resolution: Image resolution
        
        Returns:
            Generation result dictionary
        """
        self.log("Phase 4: Generating image...", "🎨")
        
        result = generate_image(
            prompt=prompt,
            output_path=output_path,
            aspect_ratio=aspect_ratio,
            resolution=resolution
        )
        
        if result["status"] == "success":
            self.log(f"  Image saved: {result['path']}", "✅")
        else:
            self.log(f"  Generation failed: {result.get('error', 'Unknown error')}", "❌")
        
        return result
    
    def run(
        self,
        description: str,
        domain: str = "auto",
        output_path: Optional[str] = None,
        aspect_ratio: str = "1:1",
        resolution: str = "2K",
        mode: str = "auto",
        skip_image: bool = False
    ) -> dict:
        """
        Execute the complete SOP pipeline.
        
        Args:
            description: User's description in natural language
            domain: Domain hint
            output_path: Path to save the generated image
            aspect_ratio: Image aspect ratio
            resolution: Image resolution
            mode: Prompt composition mode
            skip_image: If True, skip the image generation phase
        
        Returns:
            Complete result dictionary with all phases
        """
        self.log("=" * 60, "")
        self.log("Auto Generate SOP - Starting Pipeline", "🚀")
        self.log("=" * 60, "")
        self.log(f"Input: {description}", "📝")
        print()
        
        result = {
            "input": description,
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        try:
            # Phase 1: Parse Intent
            intent = self.parse_intent(description, domain)
            result["phases"]["intent"] = intent
            
            # Phase 2: Select Elements
            elements = self.select_elements(intent, description)
            result["phases"]["elements_count"] = len(elements)
            result["phases"]["elements"] = [
                {"name": e.get("name"), "category": e.get("category", e.get("field_name"))}
                for e in elements
            ]
            
            # Phase 2.5: Check Consistency
            elements = self.check_and_resolve_conflicts(elements)
            
            # Phase 3: Compose Prompt
            prompt = self.compose_prompt(elements, mode)
            result["phases"]["prompt"] = prompt
            
            # Phase 4: Generate Image
            if not skip_image:
                image_result = self.generate_image(
                    prompt=prompt,
                    output_path=output_path,
                    aspect_ratio=aspect_ratio,
                    resolution=resolution
                )
                result["phases"]["image"] = image_result
                result["status"] = image_result["status"]
                if image_result["status"] == "success":
                    result["output_path"] = image_result["path"]
            else:
                self.log("  (Image generation skipped)", "⏭️")
                result["status"] = "prompt_only"
            
            self.log("=" * 60, "")
            self.log("Pipeline completed!", "🎉")
            self.log("=" * 60, "")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.log(f"Pipeline failed: {e}", "❌")
            import traceback
            traceback.print_exc()
        
        finally:
            self.generator.close()
        
        return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Auto Generate SOP - End-to-end AI image generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/auto_generate_sop.py "电影级的亚洲女性，张艺谋风格"
  python scripts/auto_generate_sop.py "赛博朋克未来城市" --ratio 16:9 --resolution 4K
  python scripts/auto_generate_sop.py "中国水墨画山水" --domain art --prompt-only
"""
    )
    
    parser.add_argument(
        "description",
        help="Natural language description of the image to generate"
    )
    parser.add_argument(
        "--domain", "-d",
        choices=["portrait", "art", "design", "product", "video", "auto"],
        default="auto",
        help="Domain hint (default: auto)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: auto-generated in outputs/)"
    )
    parser.add_argument(
        "--ratio", "-r",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        default="1:1",
        help="Aspect ratio (default: 1:1)"
    )
    parser.add_argument(
        "--resolution",
        choices=["2K", "4K"],
        default="2K",
        help="Image resolution (default: 2K)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["simple", "auto", "detailed"],
        default="auto",
        help="Prompt composition mode (default: auto)"
    )
    parser.add_argument(
        "--prompt-only", "-p",
        action="store_true",
        help="Only generate prompt, skip image generation"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode - minimal output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )
    
    args = parser.parse_args()
    
    # Run the SOP
    sop = AutoGenerateSOP(verbose=not args.quiet)
    result = sop.run(
        description=args.description,
        domain=args.domain,
        output_path=args.output,
        aspect_ratio=args.ratio,
        resolution=args.resolution,
        mode=args.mode,
        skip_image=args.prompt_only
    )
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.quiet:
        if result.get("status") == "success":
            print(result.get("output_path", result["phases"].get("prompt", "")))
        else:
            print(f"Error: {result.get('error', 'Unknown')}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
