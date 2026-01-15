#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.getcwd())

import mcp_server.tools.prompt_composer as pc
from mcp_server.tools.element_query import query_elements

# FORCE MANUAL MODE
pc.IntelligentGenerator = None

def main():
    description = "印象派风格的日落后的巴黎街道"
    # print(f"User Request: {description}")
    
    selected_elements = []
    
    # 1. Define Core Style Element
    impressionism_elem = {
        'element_id': 'custom_impressionism',
        'name': 'Impressionism',
        'chinese_name': '印象派',
        'template': 'Impressionist art style, oil painting, soft visible brushstrokes, vibrant colors, emphasizing light and atmosphere',
        'category': 'art_styles', 
        'reusability_score': 10.0
    }
    selected_elements.append(impressionism_elem)
    
    # 2. Search for specialized elements (Lighting)
    # We try to use DB if available, else fallback
    keywords = ["sunset", "dusk"]
    res = query_elements(domain='common', category='lighting_techniques', keywords=keywords, limit=2)
    if res:
        for r in res:
            r['category'] = 'lighting_techniques'
        selected_elements.extend(res)
    else:
        selected_elements.append({
            'element_id': 'manual_sunset',
            'name': 'Sunset',
            'template': 'warm golden hour lighting, long shadows, dramatic sky colors, soft dusk glow',
            'category': 'lighting_techniques'
        })

    # 3. Search for Atmosphere
    # Map to 'lighting_techniques' or 'art_styles' to ensure prompt composer picks it up
    res = query_elements(domain='common', category='atmospheres', keywords=["romantic", "Paris"], limit=1)
    if res:
        for r in res:
            r['category'] = 'art_styles' # Map to art_styles to be included in Technical/Style section
        selected_elements.extend(res)
    else:
        selected_elements.append({
             'element_id': 'manual_paris_vibe',
             'name': 'Parisian Atmosphere',
             'template': 'romantic parisian atmosphere, street ambience, nostalgic mood',
             'category': 'art_styles'
        })

    # 4. Compose
    final_prompt = pc.compose_prompt(
        selected_elements, 
        mode="detailed", 
        subject_desc="A bustling Paris street view after sunset, with street lamps reflecting on cobblestones"
    )
    
    print("✨ 生成的提示词 / Generated Prompt:")
    print("────────────────────────────────────────")
    print(final_prompt)
    print("────────────────────────────────────────")

if __name__ == "__main__":
    main()
