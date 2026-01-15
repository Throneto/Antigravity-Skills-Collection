#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.getcwd())

from mcp_server.tools.intent_parser import parse_intent
from mcp_server.tools.element_query import query_elements
from mcp_server.tools.prompt_composer import compose_prompt

def main():
    description = "黄山云海，苍松翠柏，传统留白技法"
    domain = "art"
    
    print(f"User Request: {description}")
    
    # 1. Parse Intent
    # print("\n--- 1. Parsing Intent ---")
    # intent = parse_intent(description, domain)
    # print(json.dumps(intent, indent=2, ensure_ascii=False))
    
    # 2. Manual Element Selection (Database missing ink wash elements)
    print("\n--- 2. Selecting Elements (Manual Injection) ---")
    selected_elements = []

    # A. Core Style: Chinese Ink Wash
    ink_wash_elem = {
        'element_id': 'custom_ink_wash',
        'name': 'Chinese Ink Wash Painting',
        'chinese_name': '中国水墨画',
        'template': 'Traditional Chinese ink wash painting style, shan shui, monochromatic ink tones, expressive brushwork, wet wash and dry brush contrast',
        'category': 'art_styles',
        'reusability_score': 10.0
    }
    selected_elements.append(ink_wash_elem)

    # B. Technique: Negative Space (Liubai)
    negative_space_elem = {
        'element_id': 'custom_negative_space',
        'name': 'Negative Space (Liubai)',
        'chinese_name': '留白',
        'template': 'Traditional liubai technique, heavy use of negative space, emptiness representing clouds and sky, breathability in composition',
        'category': 'art_styles' # Mapped to styles/technique
    }
    selected_elements.append(negative_space_elem)

    # C. Subject Elements: Pine & Mountain
    pine_elem = {
        'element_id': 'custom_pine',
        'name': 'Gnarled Pine Trees',
        'chinese_name': '苍松',
        'template': 'Ancient gnarled pine trees growing from cliffs, twisted branches, symbol of longevity',
        'category': 'art_scene_settings' 
    }
    selected_elements.append(pine_elem)

    mountain_elem = {
        'element_id': 'custom_huangshan',
        'name': 'Yellow Mountain Peaks',
        'chinese_name': '黄山',
        'template': 'Huangshan mountain peaks, granite cliffs, jagged rocks, shrouded in mist',
        'category': 'art_scene_settings'
    }
    selected_elements.append(mountain_elem)
    
    cloud_elem = {
        'element_id': 'custom_cloud_sea',
        'name': 'Sea of Clouds',
        'chinese_name': '云海',
        'template': 'Sea of clouds, misty atmosphere, ethereal fog',
        'category': 'art_scene_settings'
    }
    selected_elements.append(cloud_elem)


    for e in selected_elements:
        print(f" - [{e['element_id']}] {e['name']} ({e['chinese_name']})")


    # 3. Compose Prompt
    print("\n--- 3. Composing Prompt ---")
    # Using 'detailed' mode to ensure all elements are woven in, but we can also use 'simple' if we want less filler.
    # Subject desc covers the main scene.
    final_prompt = compose_prompt(
        selected_elements, 
        mode="detailed", 
        subject_desc="A majestic landscape of Huangshan with sea of clouds and ancient pines"
    )
    
    print("\n" + "="*40)
    print("🖌️ 水墨画提示词 (Ink Wash Prompt)")
    print("────────────────────────────────────────")
    print(final_prompt)
    print("────────────────────────────────────────")

if __name__ == "__main__":
    main()
