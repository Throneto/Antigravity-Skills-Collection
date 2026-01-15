#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp_server.tools.prompt_composer import compose_prompt
from mcp_server.tools.element_query import query_elements

def main():
    description = "印象派风格的日落后的巴黎街道"
    print(f"User Request: {description}")
    
    selected_elements = []
    
    # 1. Define Core Style Element (since DB might miss specific styles like Impressionism)
    # We construct it manually to ensure high quality
    impressionism_elem = {
        'element_id': 'custom_impressionism',
        'name': 'Impressionism',
        'chinese_name': '印象派',
        'template': 'Impressionist style, oil painting on canvas, visible brushstrokes, emphasis on light and its changing qualities, open composition',
        'category': 'art_styles',
        'reusability_score': 10.0
    }
    selected_elements.append(impressionism_elem)
    
    # 2. Search for specialized elements (Lighting, Atmosphere)
    # We try to find "sunset" or "warm" lighting
    keywords = ["sunset", "dusk", "warm", "golden hour"]
    
    # Try 'lighting_techniques' in 'common' or 'art'
    # We assume query_elements returns dicts without 'category', so we add it back.
    print("Querying lighting elements...")
    res = query_elements(domain='common', category='lighting_techniques', keywords=keywords, limit=2)
    if res:
        for r in res:
            r['category'] = 'lighting_techniques'
            # print(f" - Found lighting: {r['name']}")
        selected_elements.extend(res)
    else:
        # Fallback lighting if DB empty
        selected_elements.append({
            'element_id': 'manual_sunset',
            'name': 'Sunset',
            'template': 'warm sunset lighting, long shadows, golden hour glow, dramatic sky',
            'category': 'lighting_techniques'
        })
        
    # 3. Search for Atmosphere
    print("Querying atmosphere elements...")
    res = query_elements(domain='common', category='atmospheres', keywords=["romantic", "nostalgic", "Parisian"], limit=2)
    if res:
        for r in res:
            r['category'] = 'atmospheres' # prompt_composer manual mapping maps 'scene.atmosphere' -> 'atmospheres'
            # Check prompt_composer mappings: 'scene.atmosphere' -> 'atmospheres'
            # But line 113 of prompt_composer.py ONLY checks: 'lighting_techniques', 'lighting.lighting_type'
            # It DOES NOT check 'atmospheres' explicitly in manual mode!
            # It checks 'art_styles', 'camera_settings' in technical.
            # It does NOT seem to have a generic 'atmosphere' section.
            # So we might want to map atmosphere to 'lighting_techniques' or 'art_styles' to force inclusion.
            r['category'] = 'lighting_techniques' # Hack to ensure it appears
        selected_elements.extend(res)

    # 4. Compose
    # subject_desc will handle the main subject "Paris street"
    final_prompt = compose_prompt(
        selected_elements, 
        mode="detailed", 
        subject_desc="A bustling Paris street after sunset"
    )
    
    print("\n" + "="*40)
    print("🎨 艺术风格解析")
    print(f"- 类型: 印象派 (Impressionism)")
    print(f"- 主题: 巴黎街道 (Paris Street)")
    print(f"- 氛围: 日落 (Sunset)")
    print("\n✨ 最终提示词")
    print("────────────────────────────────────────")
    print(final_prompt)
    print("────────────────────────────────────────")

if __name__ == "__main__":
    main()
